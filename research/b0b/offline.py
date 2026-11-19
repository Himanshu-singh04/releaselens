"""Verify the reviewed wheel, create a fresh local venv, install offline, run vectors.

Usage: python3 -I -B research/b0b/offline.py WHEEL NEW_TASK_DIRECTORY
No downloads. NEW_TASK_DIRECTORY must not exist; all tool state is placed there.
"""
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import zipfile
from email.parser import BytesParser


def main():
    wheel, task = (Path(p).resolve() for p in sys.argv[1:])
    expected = "520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48"
    if wheel.name != "rfc8785-0.1.4-py3-none-any.whl":
        raise SystemExit("Unexpected artifact name")
    if wheel.stat().st_size != 9240 or hashlib.sha256(wheel.read_bytes()).hexdigest() != expected:
        raise SystemExit("Artifact integrity mismatch")
    with zipfile.ZipFile(wheel) as archive:
        names = archive.namelist()
        if any(n.endswith((".pth", "entry_points.txt")) or ".data/" in n for n in names):
            raise SystemExit("Unexpected install/startup script mechanism")
        metadata = BytesParser().parsebytes(archive.read("rfc8785-0.1.4.dist-info/METADATA"))
        if metadata["Name"] != "rfc8785" or metadata["Version"] != "0.1.4":
            raise SystemExit("Unexpected package identity")
        license_bytes = archive.read("rfc8785-0.1.4.dist-info/LICENSE")
        if hashlib.sha256(license_bytes).hexdigest() != "0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594":
            raise SystemExit("Unexpected license")
    task.mkdir(parents=True, exist_ok=False)
    for part in ("home", "config", "cache", "tmp"):
        (task / part).mkdir()
    env = {
        "PATH": os.defpath, "HOME": str(task / "home"),
        "XDG_CONFIG_HOME": str(task / "config"), "XDG_CACHE_HOME": str(task / "cache"),
        "TMPDIR": str(task / "tmp"), "TEMP": str(task / "tmp"), "TMP": str(task / "tmp"),
        "PIP_CONFIG_FILE": os.devnull, "PIP_DISABLE_PIP_VERSION_CHECK": "1",
        "PYTHONDONTWRITEBYTECODE": "1", "LC_ALL": "C",
    }

    def run(args):
        subprocess.run(args, env=env, check=True, stdout=sys.stderr)

    # No ensurepip subprocess: retain -I/-B while running the interpreter's bundled pip.
    run([sys.executable, "-I", "-B", "-m", "venv", "--without-pip", str(task / ".venv")])
    python = str(task / ".venv" / "bin" / "python")
    bootstrap = '''
import ensurepip, hashlib, pathlib, runpy, sys, sysconfig
configured=sysconfig.get_config_var("WHEEL_PKG_DIR")
directory=pathlib.Path(configured) if configured else pathlib.Path(ensurepip.__file__).parent / "_bundled"
wheels=list(directory.glob("pip-*.whl"))
if len(wheels) != 1: raise SystemExit("Expected one interpreter-provided pip wheel")
wheel=wheels[0]
print("Installer:",wheel.name,hashlib.sha256(wheel.read_bytes()).hexdigest(),file=sys.stderr)
sys.path.insert(0,str(wheel))
sys.argv=["pip",*sys.argv[1:]]
runpy.run_module("pip",run_name="__main__")
'''
    pip = [python, "-I", "-B", "-c", bootstrap, "--isolated", "--disable-pip-version-check"]
    run([*pip,
         "install", "--no-index", "--find-links", str(wheel.parent), "--only-binary=:all:",
         "--require-hashes", "--no-deps", "--no-compile", "--no-cache-dir",
         "-r", str(Path(__file__).with_name("requirements.txt"))])
    run([*pip, "check"])
    # Compare every wheel member (except RECORD, rewritten by pip) before candidate import.
    check = '''
import hashlib, importlib.metadata as m, json, pathlib, sys, zipfile
d=m.distribution("rfc8785")
with zipfile.ZipFile(sys.argv[1]) as z:
    for name in z.namelist():
        if name.endswith("/RECORD"): continue
        if d.locate_file(name).read_bytes() != z.read(name):
            raise SystemExit("Installed member mismatch")
print(json.dumps({"inventory": sorted((x.metadata["Name"],x.version) for x in m.distributions()),
 "distribution_root":str(d.locate_file("")), "wheel_members_equal":True}))
'''
    run([python, "-I", "-B", "-c", check, str(wheel)])
    subprocess.run([python, "-I", "-B", str(Path(__file__).with_name("experiment.py"))],
                   env=env, check=True)


if __name__ == "__main__":
    main()
