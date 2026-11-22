"""Released target prerequisites only. No ensurepip, downloads, activation or fallback."""
import hashlib
import importlib
import importlib.metadata as metadata
import importlib.util
import json
from pathlib import Path
import platform
import runpy
import site
import sys
import sysconfig
import zipfile

ROOT = Path(__file__).resolve().parents[2]
BASE = Path('/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection/extracted/python')
TASK = Path('/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation')
VENV = TASK / 'venv'
PIP = BASE / 'lib/python3.14/ensurepip/_bundled/pip-26.3-py3-none-any.whl'
WHEEL = Path('/Volumes/AIWorkspace/caches/releaselens/b1a-runtime/rfc8785-0.1.4-py3-none-any.whl')
PIP_HASH = 'f3b60b20ffaadd4415ed7957212a38ac63fa4c5fa375bd0f4a797777940fad13'
WHEEL_HASH = '520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48'


def require(condition):
    if not condition:
        raise RuntimeError('B1d prerequisite mismatch')


def verified(path, size, digest):
    require(path.is_file() and path.stat().st_size == size)
    require(hashlib.sha256(path.read_bytes()).hexdigest() == digest)


def identity(mode):
    in_venv = mode != 'base'
    prefix = VENV if in_venv else BASE
    executable = prefix / 'bin' / ('python' if in_venv else 'python3.14')
    require(tuple(sys.version_info[:3]) == (3, 14, 10) and sys.implementation.name == 'cpython')
    require(platform.machine() == 'arm64' and sys.maxsize == 2**63 - 1)
    require(sys._is_gil_enabled() is True and sysconfig.get_config_var('Py_GIL_DISABLED') == 0)
    require(hasattr(sys, '_jit') and sys._jit.is_enabled() is False)
    require(Path(sys.prefix) == prefix and Path(sys.exec_prefix) == prefix)
    require(Path(sys.base_prefix) == BASE and Path(sys.base_exec_prefix) == BASE)
    require(Path(sys.executable) == executable)
    require(Path(sys._base_executable).resolve() == BASE / 'bin/python3.14')
    require(sys.flags.isolated == 1 and sys.flags.ignore_environment == 1 and sys.dont_write_bytecode)
    require(site.ENABLE_USER_SITE is False and '' not in sys.path)
    require('sitecustomize' not in sys.modules and 'usercustomize' not in sys.modules)
    for entry in sys.path:
        path = Path(entry).resolve()
        require(path.is_relative_to(BASE) or (in_venv and path.is_relative_to(VENV)))
        if in_venv:
            require(not path.is_relative_to(BASE / 'lib/python3.14/site-packages'))
    # Concrete imports needed by the harness/bootstrap; no GUI or optional sweep.
    names = ['decimal', '_decimal', 'json', 'math', 'struct', 'hashlib', 'zipfile',
             'runpy', 'importlib.metadata', 'venv', 'typing', 're', 'io', 'contextlib']
    origins = {}
    for name in names:
        module = importlib.import_module(name)
        origin = module.__spec__.origin
        require(origin in ('built-in', 'frozen') or Path(origin).resolve().is_relative_to(BASE))
        origins[name] = origin
    inventory = sorted((d.metadata['Name'], d.version) for d in metadata.distributions())
    wanted = [('pip', '26.3')] if not in_venv else ([('rfc8785', '0.1.4')] if mode == 'installed' else [])
    require(inventory == wanted)
    if in_venv:
        configuration = (VENV / 'pyvenv.cfg').read_text()
        require('include-system-site-packages = false' in configuration)
        packages = VENV / 'lib/python3.14/site-packages'
        require(not list(packages.rglob('*.pth')))
        require(not list(packages.rglob('sitecustomize*')) and not list(packages.rglob('usercustomize*')))
    if mode == 'installed':
        verified(WHEEL, 9240, WHEEL_HASH)
        dist = metadata.distribution('rfc8785')
        require(Path(dist.locate_file('')).resolve() == VENV / 'lib/python3.14/site-packages')
        with zipfile.ZipFile(WHEEL) as archive:
            names = archive.namelist()
            for name in names:
                if name.endswith('/RECORD'):
                    continue  # pip necessarily rewrites RECORD; all payload members compared.
                require(dist.locate_file(name).read_bytes() == archive.read(name))
        allowed_extra = {'rfc8785-0.1.4.dist-info/INSTALLER', 'rfc8785-0.1.4.dist-info/REQUESTED',
                         'rfc8785-0.1.4.dist-info/direct_url.json'}
        actual_files = {str(p.relative_to(packages)) for p in packages.rglob('*') if p.is_file()}
        require(set(names) <= actual_files and actual_files <= set(names) | allowed_extra)
        require(not any(p.is_symlink() for p in packages.rglob('*')))
        candidate = importlib.import_module('rfc8785')
        require(candidate.__version__ == '0.1.4')
        require(Path(candidate.__file__) == packages / 'rfc8785/__init__.py')
        origins['rfc8785'] = candidate.__file__
    # Verify every loaded filesystem-backed module is within approved roots, except this script.
    for module in tuple(sys.modules.values()):
        file = getattr(module, '__file__', None)
        if file:
            path = Path(file).resolve()
            require(path == Path(__file__).resolve() or path.is_relative_to(BASE)
                    or (in_venv and path.is_relative_to(VENV)))
    print(json.dumps({'mode': mode, 'version': sys.version, 'executable': sys.executable,
                      'prefix': sys.prefix, 'base_prefix': sys.base_prefix, 'sys_path': sys.path,
                      'machine': platform.machine(), 'GIL': sys._is_gil_enabled(),
                      'JIT': sys._jit.is_enabled(), 'origins': origins, 'inventory': inventory}, sort_keys=True))


def install():
    identity('empty')
    verified(PIP, 1950951, PIP_HASH)
    verified(WHEEL, 9240, WHEEL_HASH)
    # Wheel tooling is put first only for this process; it is never installed into the venv.
    sys.path.insert(0, str(PIP))
    spec = importlib.util.find_spec('pip')
    require(spec is not None and spec.origin == str(PIP) + '/pip/__init__.py')
    print(json.dumps({'bootstrap_wheel': str(PIP), 'sha256': PIP_HASH}), flush=True)
    sys.argv = ['pip', '--isolated', '--disable-pip-version-check', '--no-input', 'install', '--no-index',
                '--no-deps', '--require-hashes', '--no-cache-dir', '--no-compile',
                '--only-binary=:all:', '-r', str(ROOT / 'fixtures/b1d/requirements.txt')]
    runpy.run_module('pip', run_name='__main__')


if __name__ == '__main__':
    try:
        if sys.argv[1:] == ['install']:
            install()
        else:
            require(len(sys.argv) == 2 and sys.argv[1] in ('base', 'empty', 'installed'))
            identity(sys.argv[1])
    except Exception:
        # No platform paths, hostile values or exception text in a successful diagnostic.
        print('{"prerequisite":"failed"}', file=sys.stderr)
        raise SystemExit(1)
