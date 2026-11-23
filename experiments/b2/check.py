"""B2-only host supervisor: retained-runtime tests, immutable attempt evidence.

Run with approved host Python -I -B: check.py LABEL encode|test [session2].
Final correction session also permits mode probe for the fixed coordinator probe.
This never invokes a historical research runner or repairs an environment.
"""
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import selectors
import shutil
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = ROOT / 'artifacts/b2'
SCRATCH = Path('/Volumes/AIWorkspace/caches/releaselens/b2-contract')
HOST = '/Library/Frameworks/Python.framework/Versions/3.13/bin/python3'
TARGET = '/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python'
CEILING = 300
CAP = 1048576


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def allocation():
    total = 0
    for root in (EVIDENCE, SCRATCH):
        assert root.is_dir() and not root.is_symlink()
        for p in [root, *root.rglob('*')]:
            total += p.lstat().st_blocks * 512
    return total


def capacity():
    assert allocation() + 2 * CAP < 256 * 1048576, 'B2 allocation bound'
    assert os.statvfs(EVIDENCE).f_bavail * os.statvfs(EVIDENCE).f_frsize > 32 * 1048576


def retained():
    entries = json.loads((EVIDENCE / 'preflight.json').read_text())['retained_cache']
    expected = {Path(e['path']) for e in entries}
    cache = Path(TARGET).parents[2]
    assert {p for p in cache.rglob('*') if not p.is_dir() or p.is_symlink()} == expected
    for e in entries:
        assert sha(Path(e['path'])) == e['sha256']
    base = Path('/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection/extracted/python')
    manifest = ROOT / 'artifacts/b1c/evidence-manifest.json'
    assert sha(manifest) == '663b31469f22c7160f26a80940d4f5a23d59252e1e193f06daf80817b3d25541'
    expected = set()
    for e in json.loads(manifest.read_text())['entries']:
        p = Path(e['path'])
        if p.is_relative_to(base):
            expected.add(p)
            if 'sha256' in e:
                assert sha(p) == e['sha256']
            if 'link' in e:
                assert os.readlink(p) == e['link']
    assert {p for p in base.rglob('*') if not p.is_dir() or p.is_symlink()} == expected


def main():
    assert sys.executable == HOST
    label, mode, *session = sys.argv[1:]
    assert session in ([], ['session2'])
    assert label.isascii() and label.replace('-', '').isalnum()
    assert mode in (('test', 'probe') if session else ('encode', 'test'))
    records = EVIDENCE / 'session2' if session else EVIDENCE
    task = SCRATCH / 'session2' if session else SCRATCH
    clock = records / 'start.json'
    deadline = datetime.fromisoformat(json.loads(clock.read_text())['deadline_utc']).timestamp()
    assert deadline - time.time() >= CEILING + 300, 'Reserve closing delivery; no late suite'
    capacity()
    retained()
    directory = records / label
    directory.mkdir()
    paths = set()
    for pattern in ('releaselens/*.py', 'tests/*.py', 'fixtures/b2/*.json', 'experiments/b2/*.py'):
        paths.update(ROOT.glob(pattern))
    paths.add(ROOT / '.github/workflows/ci.yml')
    probe = EVIDENCE / 'coordinator-review-3bfc7a/probe_contract.py'
    if mode == 'probe':
        assert sha(probe) == json.loads((records / 'preflight.json').read_text())['probe_sha256']
        paths.add(probe)
    files = {}
    for p in sorted(paths):
        relative = p.relative_to(ROOT)
        destination = directory / 'source' / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(p, destination)
        files[str(relative)] = sha(p)
    script = probe if mode == 'probe' else ROOT / 'tests' / (
        'fixture_source.py' if mode == 'encode' else 'test_contract.py')
    command = [HOST if mode == 'encode' else TARGET, '-I', '-B', str(script)]
    environment = {'PATH': os.defpath, 'HOME': str(task / 'home'), 'TMPDIR': str(task / 'tmp'),
                   'TMP': str(task / 'tmp'), 'TEMP': str(task / 'tmp'),
                   'XDG_CACHE_HOME': str(task / 'cache'), 'XDG_CONFIG_HOME': str(task / 'config'),
                   'PYTHONDONTWRITEBYTECODE': '1', 'LC_ALL': 'C', 'PIP_CONFIG_FILE': os.devnull,
                   'PIP_DISABLE_PIP_VERSION_CHECK': '1'}
    record = {'utc': datetime.now(timezone.utc).isoformat(), 'argv': command, 'cwd': str(ROOT),
              'environment': environment, 'files': files, 'head': subprocess.check_output(
                  ['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
              'session_remaining_seconds': deadline - time.time(), 'ceiling_seconds': CEILING,
              'stream_cap_bytes': CAP, 'mode': mode, 'clock_path': str(clock), 'clock_sha256': sha(clock)}
    (directory / 'started.json').write_text(json.dumps(record, indent=2) + '\n')
    process = None
    reason = None
    streams = {'stdout': bytearray(), 'stderr': bytearray()}
    start = time.monotonic()
    signals = []
    try:
        process = subprocess.Popen(command, cwd=ROOT, env=environment, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
        with selectors.DefaultSelector() as selector:
            for name, pipe in (('stdout', process.stdout), ('stderr', process.stderr)):
                os.set_blocking(pipe.fileno(), False)
                selector.register(pipe, selectors.EVENT_READ, name)
            while selector.get_map():
                capacity()
                if time.monotonic() - start >= CEILING or time.time() >= deadline - 300:
                    reason = 'deadline'
                    break
                for key, _ in selector.select(0.1):
                    chunk = os.read(key.fileobj.fileno(), 8192)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    remaining = CAP - len(streams[key.data])
                    streams[key.data].extend(chunk[:remaining])
                    if len(chunk) > remaining:
                        reason = 'stream-cap'
                        break
                if reason:
                    break
            if reason is None:
                process.wait(timeout=max(0.001, CEILING - (time.monotonic() - start)))
    except Exception as error:
        reason = type(error).__name__
    finally:
        if process is not None:
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(process.pid, sig)
                    signals.append(signal.Signals(sig).name)
                except ProcessLookupError:
                    pass
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    pass
            process.stdout.close()
            process.stderr.close()
        for name, data in streams.items():
            (directory / name).write_bytes(data)
        record.update({'elapsed_seconds': time.monotonic() - start,
                       'exit_code': process.returncode if process else None, 'stop_reason': reason,
                       'signals': signals, 'stdout_bytes': len(streams['stdout']),
                       'stderr_bytes': len(streams['stderr']), 'new_allocation_bytes': allocation()})
        (directory / 'result.json').write_text(json.dumps(record, indent=2) + '\n')
    retained()
    capacity()
    assert reason is None and record['exit_code'] == 0, 'Retained attempt failed; inspect evidence before edits'
    print(json.dumps({k: v for k, v in record.items() if k not in ('files', 'environment')}, indent=2))


if __name__ == '__main__':
    main()
