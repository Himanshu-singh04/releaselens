"""Host-only adapter tests against retained record shapes. No subprocess dispatch."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOST = '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'
if sys.executable != HOST or sys.version_info[:2] != (3, 13):
    raise RuntimeError('Use the approved host Python3.13 -I -B')
spec = importlib.util.spec_from_file_location('b1f_confirm', ROOT / 'experiments/b1f/confirm.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class ConfirmationTests(unittest.TestCase):
    def setUp(self):
        # Retain synthetic fixtures until after their verdicts are sealed; no cleanup needed.
        self.root = Path(tempfile.mkdtemp(prefix='host-test-', dir=adapter.SCRATCH))
        self.output = self.root / 'execution'
        self.original, self.identity, self.ids = adapter.reference()
        self.records = copy.deepcopy(self.original)
        self.calls = []
        for obj, name, value in [(adapter, 'OUTPUT', self.output)]:
            mock = patch.object(obj, name, value)
            mock.start()
            self.addCleanup(mock.stop)
        mock = patch.object(adapter.runner.subprocess, 'Popen', side_effect=AssertionError('No child allowed'))
        mock.start()
        self.addCleanup(mock.stop)

    def dispatch(self, args, directory, label, deadline, legacy=False):
        self.calls.append(([str(a) for a in args], label, legacy))
        self.assertEqual(directory, self.output)
        if label.startswith('identity'):
            return json.dumps(self.identity).encode()
        if legacy:
            return self.records['legacy']
        return json.dumps(next(r for r in self.records['new'] if r['id'] == label)).encode()

    def confirm(self):
        self.output.mkdir()
        with patch.object(adapter.runner, 'run', self.dispatch):
            return adapter.confirm(self.original, self.identity, self.ids, 123)

    def test_actual_record_shapes_identical_and_exact_commands(self):
        self.assertEqual(self.confirm(), self.original)
        packet = json.loads((ROOT / 'artifacts/b1e/preparation-packet.json').read_text())
        self.assertEqual([c[0] for c in self.calls], packet['run1_children'])
        self.assertEqual(len(self.calls), 99)
        self.assertTrue(json.loads((self.output / 'comparison.json').read_text())['equal'])
        # JCS-utf16 has actual.bytes.hex; no optional actual.hex display assumption.
        row = next(r for r in self.original['new'] if r['id'] == 'JCS-utf16')
        self.assertIn('hex', row['actual']['bytes'])
        self.assertNotIn('hex', row['actual'])

    def test_same_pass_counts_but_changed_semantic_outcome_fails(self):
        self.records['new'][0]['actual']['sha256'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'Confirmation differs'):
            self.confirm()
        comparison = json.loads((self.output / 'comparison.json').read_text())
        self.assertFalse(comparison['equal'])
        self.assertEqual(comparison['original'], self.original)

    def test_changed_identity_stops_before_any_check(self):
        self.output.mkdir()
        changed = dict(self.identity, inventory=[])
        with patch.object(adapter.runner, 'run', return_value=json.dumps(changed).encode()) as run:
            with self.assertRaisesRegex(RuntimeError, 'identity differs'):
                adapter.confirm(self.original, self.identity, self.ids, 123)
        self.assertEqual(run.call_count, 1)

    def test_failed_row_stops_without_later_dispatch(self):
        self.records['new'][0]['pass'] = False
        with self.assertRaisesRegex(RuntimeError, 'Oracle mismatch'):
            self.confirm()
        self.assertEqual([c[1] for c in self.calls], ['identity', self.ids[0]])

    def test_changed_after_identity_is_fatal(self):
        self.output.mkdir()

        def dispatch(*args, **kwargs):
            if args[2] == 'identity-after':
                return json.dumps(dict(self.identity, inventory=[])).encode()
            return self.dispatch(*args, **kwargs)

        with patch.object(adapter.runner, 'run', dispatch):
            with self.assertRaisesRegex(RuntimeError, 'identity changed'):
                adapter.confirm(self.original, self.identity, self.ids, 123)

    def test_stop_and_exclusive_slot_no_retry(self):
        release = self.root / 'release.json'
        release.write_text('{}')
        prepared = ({'remaining_worker_seconds': 60}, {}, {}, self.original, self.identity, self.ids)
        with patch.object(adapter, 'prepare', return_value=prepared), \
                patch.object(sys, 'argv', ['confirm', '1' * 40, str(release)]), \
                patch.object(adapter, 'confirm', side_effect=RuntimeError('synthetic failure')) as dispatch:
            with self.assertRaisesRegex(RuntimeError, 'synthetic failure'):
                adapter.main()
            stop = (self.output / 'STOP.json').read_bytes()
            self.assertTrue((self.output / 'started.json').exists())
            self.assertFalse((self.output / 'success.json').exists())
            with self.assertRaises(FileExistsError):
                adapter.main()
            self.assertEqual(dispatch.call_count, 1)
            self.assertEqual((self.output / 'STOP.json').read_bytes(), stop)

    def test_retained_and_new_allocation_limits(self):
        task = self.root / 'scratch'
        evidence = self.root / 'evidence'
        task.mkdir()
        evidence.mkdir()
        (task / 'payload').write_bytes(b'x' * 8192)
        with patch.object(adapter.budget, 'TASK', task), patch.object(adapter.budget, 'EVIDENCE', evidence):
            used = adapter.budget.allocation()
            with patch.object(adapter, 'retained_capacity') as old:
                adapter.capacity()
                old.assert_called_once()
            with patch.object(adapter.budget, 'BOUND', used + adapter.budget.RESERVE):
                with self.assertRaisesRegex(RuntimeError, 'Task allocation limit'):
                    adapter.capacity()
            with patch.object(adapter.runner, 'BOUND', adapter.runner.allocation() + used + adapter.runner.RESERVE):
                with self.assertRaisesRegex(RuntimeError, 'Combined retained and new allocation limit'):
                    adapter.capacity()
            task.rename(self.root / 'removed-scratch')
            with self.assertRaises(FileNotFoundError):
                adapter.capacity()

    def test_changed_preparation_evidence_is_fatal(self):
        entry = self.root / 'sealed-record'
        entry.write_text('original')
        manifest = self.root / 'evidence-manifest.json'
        manifest.write_text(json.dumps({'entries': [{'path': str(entry), 'sha256': adapter.runner.sha(entry)}]}))
        digest = adapter.runner.sha(manifest)
        with patch.object(adapter, 'EVIDENCE', self.root):
            adapter.preparation_evidence(digest)
            entry.write_text('changed')
            with self.assertRaisesRegex(RuntimeError, 'Preparation evidence changed'):
                adapter.preparation_evidence(digest)

    def test_wrong_release_packet_is_rejected_before_dispatch(self):
        head = '1' * 40
        release = self.root / 'release.json'
        release.write_text(json.dumps({'head': head, 'issue': 33,
            'authorization': 'https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-synthetic',
            'remaining_worker_seconds': 60, 'reference_sha256': adapter.REFERENCE_HASH, 'files': {}}))
        with patch.object(adapter, 'EVIDENCE', self.root), \
                patch.object(adapter.runner, 'git', side_effect=[head.encode(), b'']), \
                patch.object(adapter, 'packet_hashes', return_value={'file': 'expected'}), \
                patch.object(adapter, 'preserved') as preserved:
            with self.assertRaisesRegex(RuntimeError, 'Release inputs differ'):
                adapter.prepare(head, release)
            preserved.assert_not_called()

    def test_added_retained_cache_file_is_fatal(self):
        cache = self.root / 'retained'
        cache.mkdir()
        original = cache / 'installed'
        original.write_text('original')
        manifest = self.root / 'artifacts/b1e/session2/evidence-manifest.json'
        manifest.parent.mkdir(parents=True)
        manifest.write_text(json.dumps({'entries': [{'path': str(original), 'sha256': adapter.runner.sha(original)}]}))
        with patch.object(adapter, 'ROOT', self.root), \
                patch.object(adapter.runner, 'TASK', cache), \
                patch.object(adapter.runner, 'preserved', return_value={}), \
                patch.object(adapter, 'EXTRA_MANIFESTS', {'b1e/session2': (adapter.runner.sha(manifest), adapter.BASELINE)}):
            adapter.preserved()
            (cache / 'unexpected.pth').write_text('synthetic extra')
            with self.assertRaisesRegex(RuntimeError, 'Extra or missing retained-cache file'):
                adapter.preserved()


if __name__ == '__main__':
    unittest.main(verbosity=2)
