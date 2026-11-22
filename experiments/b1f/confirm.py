"""Confirmation-only host adapter. Import/data checks are safe; main needs coordinator release."""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'artifacts/b1f'
SCRATCH = Path('/Volumes/AIWorkspace/caches/releaselens/b1f-confirmation')
OUTPUT = EVIDENCE / 'execution'
BASELINE = 'beee491d61799e3bd756322fa0dfb503680e7eea'
EXECUTED = 'e83b191771eac3fc6b1825bff2268f1c4f78b4cb'
REFERENCE = ROOT / 'artifacts/b1e/execution/run1'
REFERENCE_HASH = 'ce8889f3aae3142c4eb9cb988e66a1495de99c465b8521d495b4499fa3ae654e'
RUNNER_HASH = 'dcfaa630ec1a5bec651208039f4624b9e28352fa11dee029e511ace8043bf53b'
EXTRA_MANIFESTS = {
    'b1e': ('98a9a52ec23b1266ffaff2a207b3f5f3fc69b0214e42e7aeaad516cabcdae6cd', EXECUTED),
    'b1e/session2': ('ef2e3a62d9bfa482e1a35f5a376476afe3e7b73e307614307bbb05cae6e408b8', BASELINE),
}
INHERITED = (
    'experiments/b1d/runner.py', 'experiments/b1d/bootstrap.py', 'experiments/b1d/harness.py',
    'experiments/b1e/test_runner.py', 'fixtures/b1d/oracle.json', 'fixtures/b1d/requirements.txt',
    'research/b0b/experiment.py', 'fixtures/b0b/vectors.json',
    'docs/decisions/010-offline-runtime-validation.md', 'docs/decisions/011-runner-accounting-repair.md',
)
ADDITIONS = ('experiments/b1f/confirm.py', 'experiments/b1f/test_confirm.py',
             'docs/decisions/012-confirmation-only.md')


def load_runner(name):
    path = ROOT / 'experiments/b1d/runner.py'
    if hashlib.sha256(path.read_bytes()).hexdigest() != RUNNER_HASH:
        raise RuntimeError('Reviewed runner changed')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


runner = load_runner('b1f_execution')
# Separate module instance reuses the exact accounting implementation on the new roots.
budget = load_runner('b1f_budget')
budget.TASK, budget.EVIDENCE, budget.BOUND = SCRATCH, EVIDENCE, 256 * 1024**2
retained_capacity = runner.capacity


def capacity():
    retained_capacity()
    budget.capacity()
    runner.require(runner.allocation() + budget.allocation() + runner.RESERVE < runner.BOUND,
                   'Combined retained and new allocation limit')


runner.capacity = capacity  # run() keeps its original process/stream/timeout/environment implementation.


def packet_hashes():
    hashes = {p: runner.sha(ROOT / p) for p in (*INHERITED, *ADDITIONS)}
    for p in INHERITED:
        original = runner.git('show', BASELINE + ':' + p)
        runner.require(hashes[p] == hashlib.sha256(original).hexdigest(), 'Immutable baseline file changed')
    return hashes


def preserved():
    counts = runner.preserved()
    for name, (digest, revision) in EXTRA_MANIFESTS.items():
        manifest = ROOT / 'artifacts' / name / 'evidence-manifest.json'
        runner.require(runner.sha(manifest) == digest, 'Prior manifest changed')
        entries = json.loads(manifest.read_text())['entries']
        for entry in entries:
            path = Path(entry['path'])
            relative = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else None
            if relative in INHERITED:
                actual = hashlib.sha256(runner.git('show', revision + ':' + relative)).hexdigest()
            else:
                actual = runner.sha(path)  # Raw/cache files never fall back to Git.
            runner.require(actual == entry['sha256'], 'Prior evidence or installed file changed')
        if name == 'b1e/session2':
            expected = {Path(e['path']) for e in entries if Path(e['path']).is_relative_to(runner.TASK)}
            actual = {p for p in runner.TASK.rglob('*') if not p.is_dir() or p.is_symlink()}
            runner.require(actual == expected, 'Extra or missing retained-cache file')
        counts[name] = len(entries)
    return counts


def reference():
    runner.require(runner.sha(REFERENCE / 'success.json') == REFERENCE_HASH, 'Initial result changed')
    original = json.loads((REFERENCE / 'success.json').read_text())
    oracle = json.loads((ROOT / 'fixtures/b1d/oracle.json').read_text())
    for path, digest in oracle['sources'].items():
        runner.require(runner.sha(ROOT / path) == digest, 'Independent source changed')
    corpus = json.loads((ROOT / 'fixtures/b0b/vectors.json').read_text())
    ids = ['RFC-' + row[0] for row in corpus['binary64']] + [c['id'] for c in oracle['checks']]
    runner.require(len(ids) == len(set(ids)) == 96, 'New inventory changed')
    outcome = original['outcome']
    runner.require(original['head'] == EXECUTED, 'Initial revision changed')
    runner.require([r['id'] for r in outcome['new']] == ids, 'Initial new inventory changed')
    runner.require([r['id'] for r in outcome['legacy']] == runner.legacy_ids(), 'Initial legacy inventory changed')
    runner.require(all(r['pass'] is True for r in outcome['new'] + outcome['legacy']), 'Initial failure')
    identity = json.loads((REFERENCE / 'identity.stdout').read_text())
    runner.require(identity == json.loads((REFERENCE / 'identity-after.stdout').read_text()), 'Initial identity differs')
    return outcome, identity, ids


def commands(ids):
    identity = [runner.PYTHON, '-I', '-B', runner.BOOTSTRAP, 'installed']
    return [identity, *[[runner.PYTHON, '-I', '-B', runner.HARNESS, i] for i in ids],
            [runner.PYTHON, '-I', '-B', runner.HARNESS, 'legacy'], identity]


def confirm(original, identity, ids, deadline):
    planned = commands(ids)
    before = json.loads(runner.run(planned[0], OUTPUT, 'identity', deadline))
    runner.require(before == identity, 'Installed identity differs from initial run')
    rows = []
    for identifier, command in zip(ids, planned[1:-2], strict=True):
        row = json.loads(runner.run(command, OUTPUT, identifier, deadline))
        runner.require(row['id'] == identifier and row['pass'] is True, 'Oracle mismatch')
        rows.append(row)
    legacy = runner.run(planned[-2], OUTPUT, 'legacy', deadline, legacy=True)
    after = json.loads(runner.run(planned[-1], OUTPUT, 'identity-after', deadline))
    runner.require(before == after == identity, 'Installed identity changed')
    outcome = {'new': rows, 'legacy': legacy}
    runner.write(OUTPUT / 'comparison.json', {'original': original, 'confirmation': outcome,
                                            'equal': original == outcome})
    runner.require(outcome == original, 'Confirmation differs; no target retry')
    return outcome


def preparation_evidence(digest):
    manifest = EVIDENCE / 'evidence-manifest.json'
    runner.require(runner.sha(manifest) == digest, 'Preparation manifest changed')
    for entry in json.loads(manifest.read_text())['entries']:
        runner.require(runner.sha(Path(entry['path'])) == entry['sha256'], 'Preparation evidence changed')


def prepare(head, release_path):
    runner.require(len(head) == 40 and runner.git('rev-parse', 'HEAD').decode().strip() == head, 'Unreviewed head')
    runner.require(not runner.git('status', '--porcelain'), 'Dirty checkout')
    runner.require(release_path.resolve() == EVIDENCE / 'release.json', 'Wrong release path')
    release = json.loads(release_path.read_text())
    runner.require(release['issue'] == 33 and release['head'] == head, 'Wrong release binding')
    runner.require(release['authorization'].startswith('https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-'),
                   'Missing coordinator release locator')
    runner.require(0 < release['remaining_worker_seconds'] <= 3600, 'Execution budget')
    hashes = packet_hashes()
    runner.require(release['files'] == hashes and release['reference_sha256'] == REFERENCE_HASH, 'Release inputs differ')
    # Coordinator pins the sealed preparation evidence too; new session records are separate.
    preparation_evidence(release['preparation_manifest_sha256'])
    before = preserved()
    original, identity, ids = reference()
    planned = [[str(a) for a in command] for command in commands(ids)]
    packet = json.loads((ROOT / 'artifacts/b1e/preparation-packet.json').read_text())
    runner.require(planned == packet['run1_children'] and runner.environment() == packet['child_environment'],
                   'Initial commands or environment changed')
    capacity()
    return release, hashes, before, original, identity, ids


def main():
    runner.require(len(sys.argv) == 3, 'Expected reviewed head and coordinator release')
    head, path = sys.argv[1:]
    release, hashes, before, original, identity, ids = prepare(head, Path(path))
    OUTPUT.mkdir()  # Existing slot, including interruption/failure, is fatal; no restart.
    deadline = time.time() + release['remaining_worker_seconds']
    runner.write(OUTPUT / 'started.json', {'head': head, 'files': hashes, 'deadline_epoch': deadline,
                                         'release_sha256': runner.sha(Path(path)), 'preservation_before': before})
    try:
        outcome = confirm(original, identity, ids, deadline)
        after = preserved()
        preparation_evidence(release['preparation_manifest_sha256'])
        runner.require(packet_hashes() == hashes and not runner.git('status', '--porcelain'), 'Packet/checkout changed')
        runner.require(time.time() < deadline, 'Execution deadline exhausted')
        capacity()
        runner.write(OUTPUT / 'success.json', {'head': head, 'files': hashes, 'outcome': outcome,
                                              'equal_to_B1e_run1': True, 'reference_sha256': REFERENCE_HASH,
                                              'preservation_after': after, 'new_allocation_bytes': budget.allocation()})
    except BaseException as error:
        runner.write(OUTPUT / 'STOP.json', {'error': runner.parent_error(error, 'B1f-confirmation'),
                                         'action': 'STOP; retain records, no target retry or repair'})
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print(json.dumps({'STOP': runner.parent_error(error, 'B1f-main')}), file=sys.stderr)
        raise SystemExit(1)
