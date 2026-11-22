"""Host-only synthetic runner regressions; never import bootstrap or target harness."""
import importlib.util
import errno
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
HOST = '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'
SYNTHETIC = Path('/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation')
if sys.executable != HOST or sys.version_info[:2] != (3, 13):
    raise RuntimeError('Run only with the approved host Python 3.13 -I -B')
spec = importlib.util.spec_from_file_location('b1e_runner', ROOT / 'experiments/b1d/runner.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class AllocationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='host-regression-', dir=SYNTHETIC)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.task = self.root / 'task'
        self.evidence = self.root / 'evidence'
        self.task.mkdir()
        self.evidence.mkdir()
        for name, value in [('TASK', self.task), ('EVIDENCE', self.evidence),
                            ('OUTPUT', self.evidence / 'execution')]:
            mock = patch.object(runner, name, value)
            mock.start()
            self.addCleanup(mock.stop)

    def test_stable_count(self):
        nested = self.task / 'nested'
        nested.mkdir()
        (nested / 'payload').write_bytes(b'x' * 8192)
        (self.evidence / 'report').write_bytes(b'y')
        expected = sum(p.lstat().st_blocks * 512 for base in (self.task, self.evidence)
                       for p in [base, *base.rglob('*')])
        self.assertEqual(runner.allocation(), expected)

    def test_disappearing_child_at_lstat(self):
        child = self.task / 'temporary'
        child.write_bytes(b'x' * 8192)
        original = Path.lstat
        removed = []

        def cleanup(path, *args, **kwargs):
            if path == child and not removed:
                child.unlink()  # Real listed file disappears immediately before real lstat.
                removed.append(True)
            return original(path, *args, **kwargs)

        with patch.object(Path, 'lstat', cleanup):
            actual = runner.allocation()
        self.assertEqual(removed, [True])
        self.assertEqual(actual, sum(p.lstat().st_blocks * 512 for p in (self.task, self.evidence)))

    def test_disappearing_directory_before_scan(self):
        child = self.task / 'temporary-directory'
        child.mkdir()
        original = os.scandir
        removed = []

        def cleanup(path):
            if Path(path) == child:
                child.rmdir()
                removed.append(True)
            return original(path)

        with patch.object(runner.os, 'scandir', cleanup):
            actual = runner.allocation()
        self.assertEqual(removed, [True])
        self.assertGreaterEqual(actual, runner.allocation())  # Already sampled directory may be overcounted.

    def test_missing_and_non_directory_roots(self):
        for root in (self.task, self.evidence):
            with self.subTest(root=root.name):
                root.rmdir()
                with self.assertRaises(FileNotFoundError):
                    runner.allocation()
                root.write_bytes(b'not a directory')
                with self.assertRaises(NotADirectoryError):
                    runner.allocation()
                root.unlink()
                root.symlink_to(self.root, target_is_directory=True)
                with self.assertRaises(NotADirectoryError):
                    runner.allocation()
                root.unlink()
                root.mkdir()

    def test_root_loss_during_scan(self):
        original = os.scandir

        def cleanup(path):
            if Path(path) == self.evidence:
                self.task.rmdir()  # First root disappears while second is being enumerated.
            return original(path)

        with patch.object(runner.os, 'scandir', cleanup), self.assertRaises(FileNotFoundError):
            runner.allocation()

    def test_root_replacement_during_scan(self):
        original = os.scandir

        def replace(path):
            if Path(path) == self.evidence:
                self.task.rename(self.root / 'original-task')
                self.task.mkdir()
            return original(path)

        with patch.object(runner.os, 'scandir', replace), self.assertRaisesRegex(RuntimeError, 'identity changed'):
            runner.allocation()

    def test_non_enoent_lstat_errors_are_fatal(self):
        child = self.task / 'payload'
        child.touch()
        original = Path.lstat
        for number in (errno.EACCES, errno.EIO, errno.ENOTDIR):
            def fail(path, *args, **kwargs):
                if path == child:
                    raise OSError(number, 'private-message', str(path))
                return original(path, *args, **kwargs)
            with self.subTest(errno=number), patch.object(Path, 'lstat', fail):
                with self.assertRaises(OSError) as caught:
                    runner.allocation()
                self.assertEqual(caught.exception.errno, number)

    def test_unreadable_directory_is_not_empty(self):
        child = self.task / 'directory'
        child.mkdir()
        original = os.scandir
        for number in (errno.EACCES, errno.EIO, errno.ENOTDIR):
            def fail(path):
                if Path(path) == child:
                    raise OSError(number, 'private-message', str(path))
                return original(path)
            with self.subTest(errno=number), patch.object(runner.os, 'scandir', fail):
                with self.assertRaises(OSError) as caught:
                    runner.allocation()
                self.assertEqual(caught.exception.errno, number)

    def test_child_symlink_not_followed(self):
        outside = self.root / 'outside'
        outside.mkdir()
        (outside / 'payload').write_bytes(b'x' * 65536)
        link = self.task / 'link'
        link.symlink_to(outside, target_is_directory=True)
        self.assertEqual(runner.allocation(), sum(p.lstat().st_blocks * 512
                                                 for p in (self.task, self.evidence, link)))

    def test_real_capacity_boundary_and_free_space(self):
        (self.task / 'payload').write_bytes(b'x' * 8192)
        used = runner.allocation()
        with patch.object(runner, 'BOUND', used + runner.RESERVE + 1):
            runner.capacity()
        with patch.object(runner, 'BOUND', used + runner.RESERVE):
            with self.assertRaisesRegex(RuntimeError, 'Task allocation limit'):
                runner.capacity()
        with patch.object(runner.os, 'statvfs', return_value=os.statvfs_result((0,) * 10)):
            with self.assertRaisesRegex(RuntimeError, 'Insufficient remaining space'):
                runner.capacity()
        with patch.object(runner.os, 'statvfs', side_effect=OSError(errno.EIO, 'private')):
            with self.assertRaises(OSError):
                runner.capacity()

    def host_run(self, code, fails=False, deadline=None):
        directory = self.evidence / 'records'
        directory.mkdir()
        processes = []
        original = subprocess.Popen

        def spawn(args, **kwargs):
            self.assertEqual(args[:4], [HOST, '-I', '-B', '-c'])
            process = original(args, **kwargs)
            processes.append(process)
            return process

        with patch.object(runner.subprocess, 'Popen', spawn):
            if fails:
                with self.assertRaisesRegex(RuntimeError, 'Child failed; no retry'):
                    runner.run([HOST, '-I', '-B', '-c', code], directory, 'host', deadline or time.time() + 10)
            else:
                runner.run([HOST, '-I', '-B', '-c', code], directory, 'host', deadline or time.time() + 10)
        self.assertTrue(all(p.poll() is not None for p in processes))
        return json.loads((directory / 'host.json').read_text())

    def test_host_child_success(self):
        record = self.host_run('print("host-only")')
        self.assertEqual(record['exit_code'], 0)
        self.assertIsNone(record['stop_reason'])
        self.assertIsNone(record['parent_error'])

    def test_disappearing_child_through_live_capacity_caller(self):
        child = self.task / 'temporary'
        child.write_bytes(b'x' * 8192)
        original = Path.lstat
        removed = []

        def cleanup(path, *args, **kwargs):
            if path == child and not removed:
                child.unlink()
                removed.append(True)
            return original(path, *args, **kwargs)

        with patch.object(Path, 'lstat', cleanup):
            record = self.host_run('print("host-only")')
        self.assertEqual(removed, [True])
        self.assertEqual(record['exit_code'], 0)
        self.assertIsNone(record['stop_reason'])

    def test_allocation_cap_terminates_and_reaps_host_child(self):
        with patch.object(runner, 'BOUND', runner.allocation() + runner.RESERVE):
            record = self.host_run('import time; time.sleep(5)', fails=True)
        self.assertEqual(record['stop_reason'], 'parent-RuntimeError')
        self.assertEqual(record['parent_error']['operation'], 'capacity')
        self.assertIn('SIGTERM', record['termination'])
        self.assertIsNotNone(record['exit_code'])

    def test_allocation_error_evidence_is_bounded_and_redacted(self):
        child = self.task / ('SECRET-CANARY-' + 'x' * 150)
        child.touch()
        original = Path.lstat

        def fail(path, *args, **kwargs):
            if path == child:
                raise PermissionError(errno.EACCES, 'SECRET-CANARY-message', str(path))
            return original(path, *args, **kwargs)

        with patch.object(Path, 'lstat', fail):
            record = self.host_run('import time; time.sleep(5)', fails=True)
        diagnostic = record['parent_error']
        self.assertEqual(diagnostic['errno'], errno.EACCES)
        self.assertEqual(diagnostic['operation'], 'capacity')
        self.assertEqual(diagnostic['location']['root'], 'task')
        self.assertEqual(diagnostic['location']['relative'], '<redacted>')
        self.assertIn('allocation', [site['function'] for site in diagnostic['sites']])
        self.assertNotIn('SECRET-CANARY', json.dumps(diagnostic))
        self.assertNotIn(str(self.root), json.dumps(diagnostic))
        self.assertLess(len(json.dumps(diagnostic)), 1024)

    def test_process_start_failure_is_recorded(self):
        directory = self.evidence / 'records'
        directory.mkdir()
        with patch.object(runner.subprocess, 'Popen', side_effect=OSError(errno.EIO, 'SECRET-CANARY')):
            with self.assertRaisesRegex(RuntimeError, 'Child failed; no retry'):
                runner.run([HOST, '-I', '-B', '-c', 'pass'], directory, 'host', time.time() + 10)
        record = json.loads((directory / 'host.json').read_text())
        self.assertIsNone(record['exit_code'])
        self.assertEqual(record['termination'], [])
        self.assertEqual(record['parent_error']['operation'], 'process-start')
        self.assertEqual(record['parent_error']['errno'], errno.EIO)
        self.assertNotIn('SECRET-CANARY', json.dumps(record))

    def test_pipe_error_terminates_host_child(self):
        original = os.read

        def fail(fd, count):
            if count == 8192:  # Real runner pipe-read seam, not Popen's exec-error pipe.
                raise OSError(errno.EIO, 'SECRET-CANARY')
            return original(fd, count)

        with patch.object(runner.os, 'read', fail):
            record = self.host_run('import time; print("ready", flush=True); time.sleep(5)', fails=True)
        self.assertEqual(record['parent_error']['operation'], 'pipe-read')
        self.assertEqual(record['parent_error']['errno'], errno.EIO)
        self.assertIn('SIGTERM', record['termination'])

    def test_original_output_cap(self):
        self.assertEqual(runner.STREAM_CAP, 262144)
        record = self.host_run('import os,time; os.write(1,b"x"*262145); time.sleep(5)', fails=True)
        self.assertEqual(record['stdout_bytes'], 262144)
        self.assertEqual(record['stop_reason'], 'output-cap')
        self.assertIn('SIGTERM', record['termination'])

    def test_deadline_stops_and_reaps_host_child(self):
        record = self.host_run('import time; time.sleep(5)', fails=True, deadline=time.time() - 1)
        self.assertEqual(record['parent_error']['operation'], 'execution-deadline')
        self.assertIn('SIGTERM', record['termination'])

    def test_original_thirty_second_timeout(self):
        with patch.object(runner.time, 'monotonic', side_effect=[0, 31, 32, 33]):
            record = self.host_run('import time; time.sleep(5)', fails=True)
        self.assertEqual(record['stop_reason'], 'per-check-timeout')
        self.assertTrue(record['timeout'])
        self.assertIn('SIGTERM', record['termination'])

    def test_phase_stop_latch_blocks_further_dispatch(self):
        # Synthetic release/repository; run() is mocked, so no target command is launched.
        repo = self.root / 'synthetic-repo'
        names = ['fixtures/b1d/oracle.json', 'docs/decisions/010-offline-runtime-validation.md',
                 'experiments/b1e/test_runner.py', 'docs/decisions/011-runner-accounting-repair.md']
        for name in names:
            path = repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{"sources":{}}' if name.endswith('.json') else 'synthetic')
        hashes = {name: runner.sha(repo / name) for name in names}
        head = '1' * 40
        release = self.evidence / 'release.json'
        release.write_text(json.dumps({'head': head, 'issue': 32,
                                      'authorization': 'https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-synthetic',
                                      'remaining_worker_seconds': 60, 'files': hashes}))
        runner.OUTPUT.mkdir()
        (runner.OUTPUT / 'bootstrap').mkdir()
        (runner.OUTPUT / 'bootstrap/success.json').write_text('{}')
        (runner.OUTPUT / 'session.json').write_text(json.dumps({
            'head': head, 'files': hashes, 'release_sha256': runner.sha(release),
            'deadline_epoch': time.time() + 60}))

        def git(*args):
            self.assertIn(args, [('rev-parse', 'HEAD'), ('status', '--porcelain')])
            return head.encode() if args[0] == 'rev-parse' else b''

        with patch.object(runner, 'ROOT', repo), patch.object(runner, 'git', git), \
                patch.object(runner, 'preserved', return_value={}), \
                patch.object(sys, 'argv', ['runner', 'run1', head, str(release)]), \
                patch.object(runner, 'run', side_effect=OSError(errno.EIO, 'SECRET-CANARY')) as dispatch:
            with self.assertRaises(OSError):
                runner.main()
            stop_path = runner.OUTPUT / 'STOP.json'
            stopped = stop_path.read_bytes()
            record = json.loads(stopped)
            self.assertEqual(record['parent_error']['errno'], errno.EIO)
            self.assertNotIn('SECRET-CANARY', stopped.decode())
            self.assertTrue((runner.OUTPUT / 'run1/started.json').exists())
            self.assertFalse((runner.OUTPUT / 'run1/success.json').exists())
            with self.assertRaisesRegex(RuntimeError, 'Prior failure; no automatic retry'):
                runner.main()
            self.assertEqual(dispatch.call_count, 1)
            self.assertEqual(stop_path.read_bytes(), stopped)


if __name__ == '__main__':
    unittest.main(verbosity=2)
