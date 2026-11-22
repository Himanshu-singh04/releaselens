"""One-shot B1c archive safety/extraction recipe; never execute archive contents."""

import gzip
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import stat
import tarfile
import unicodedata

CACHE = Path('/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection')
EVIDENCE = Path('/Volumes/AIWorkspace/projects/releaselens/artifacts/b1c')
ARCHIVE = CACHE / 'cpython-3.14.10+20261110-aarch64-apple-darwin-install_only.tar.gz'
SHA256 = '42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666'
LIMIT = 2 * 1024**3
EXPANSION_LIMIT = 512 * 1024**2
RESERVE = 64 * 1024**2


def require(condition, message):
    if not condition:
        raise ValueError(message)


def allocated():
    return sum(p.lstat().st_blocks * 512 for base in (CACHE, EVIDENCE)
               for p in [base, *base.rglob('*')])


def safe_name(name):
    require(name and len(name) <= 1024 and '\\' not in name
            and not any(ord(c) < 32 or ord(c) == 127 for c in name), 'invalid path')
    require(not name.startswith('/') and '..' not in PurePosixPath(name).parts,
            'absolute/traversing path')
    name = posixpath.normpath(name)
    require(name != '.', 'unexpected archive-root entry')
    return name


def inspect(members):
    names, folded, links = {}, {}, {}
    total = 0
    for m in members:
        name = safe_name(m.name)
        key = unicodedata.normalize('NFD', name).casefold()
        require(key not in folded, 'duplicate/case/normalization collision')
        folded[key] = m
        require(m.isdir() or m.isreg() or m.issym() or m.islnk(), 'special member')
        require(not m.sparse and not m.mode & 0o6000, 'sparse or privileged member')
        require(0 <= m.size <= EXPANSION_LIMIT, 'member size limit')
        total += m.size
        require(total <= EXPANSION_LIMIT, 'payload size limit')
        if m.issym() or m.islnk():
            require(m.linkname and not m.linkname.startswith('/'), 'absolute/empty link')
            target = posixpath.normpath(posixpath.join(posixpath.dirname(name), m.linkname)
                                       if m.issym() else m.linkname)
            target = safe_name(target)
            if m.islnk():
                require(target in names and names[target].isreg(), 'hardlink ordering/type')
            links[name] = target
        names[name] = m
    # No member or link target may traverse an archive-created link/non-directory.
    for name in [*names, *links.values()]:
        for parent in PurePosixPath(name).parents:
            key = unicodedata.normalize('NFD', str(parent)).casefold()
            if key in folded:
                require(folded[key].isdir(), 'non-directory/link ancestor')
    for name, target in links.items():
        seen = {name}
        while target in links:
            require(target not in seen, 'link cycle')
            seen.add(target)
            target = links[target]
        require(target in names and (names[target].isreg() or names[target].isdir()),
                'dangling/unsupported link target')
    return names, total


def self_check():
    def member(name, kind=tarfile.REGTYPE, link=''):
        m = tarfile.TarInfo(name)
        m.type, m.linkname = kind, link
        return m
    inspect([member('python', tarfile.DIRTYPE), member('python/bin', tarfile.DIRTYPE),
             member('python/bin/python3.14'), member('python/bin/python3', tarfile.SYMTYPE, 'python3.14')])
    bad = [[member('../escape')], [member('/absolute')], [member('fifo', tarfile.FIFOTYPE)],
           [member('a'), member('A')], [member('a', tarfile.SYMTYPE, '../escape')],
           [member('a', tarfile.SYMTYPE, 'b'), member('b', tarfile.SYMTYPE, 'a')],
           [member('a', tarfile.SYMTYPE, 'b'), member('a/child'), member('b')],
           [member('a', tarfile.SYMTYPE, 'b'), member('A/child'), member('b')],
           [member('a', tarfile.LNKTYPE, 'later'), member('later')]]
    for members in bad:
        try:
            inspect(members)
        except ValueError:
            continue
        raise AssertionError('unsafe synthetic archive accepted')


def main():
    self_check()
    require(hasattr(tarfile, 'data_filter'), 'safe stdlib extraction unavailable')
    require(ARCHIVE.stat().st_size == 27109898, 'archive size mismatch')
    with ARCHIVE.open('rb') as f:
        require(hashlib.file_digest(f, 'sha256').hexdigest() == SHA256, 'archive hash mismatch')
    raw, destination = CACHE / 'inspected.tar', CACHE / 'extracted'
    require(not os.path.lexists(raw) and not os.path.lexists(destination), 'existing output')
    require(allocated() + 2 * EXPANSION_LIMIT + RESERVE < LIMIT, 'insufficient task budget')
    expanded = 0
    with gzip.open(ARCHIVE, 'rb') as source, raw.open('xb') as output:
        while chunk := source.read(min(1024**2, EXPANSION_LIMIT - expanded + 1)):
            expanded += len(chunk)
            require(expanded <= EXPANSION_LIMIT, 'actual gzip expansion limit')
            output.write(chunk)
    with tarfile.open(raw, 'r:') as archive:
        members = []
        for m in archive:
            require(len(members) < 20000, 'archive member cap')
            members.append(m)
        names, total = inspect(members)
        block = os.statvfs(CACHE).f_frsize
        # Reserve file rounding and implicit parent directories before any extraction.
        parents = {str(p) for name in names for p in PurePosixPath(name).parents}
        budget = sum(((m.size + block - 1) // block + 1) * block for m in members)
        budget += len(parents) * block + RESERVE
        require(allocated() + budget < LIMIT, 'extraction allocation budget')
        inventory = [{'name':name, 'type':m.type.decode('ascii'), 'bytes':m.size,
                      'mode':oct(m.mode), 'link':m.linkname} for name, m in names.items()]
        (EVIDENCE / 'archive-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')
        destination.mkdir()
        for i, m in enumerate(members):
            archive.extract(m, destination, filter='data')
            if i % 100 == 0:
                require(allocated() + RESERVE < LIMIT, 'actual allocation limit')
    root = destination.resolve()
    for p in destination.rglob('*'):
        require(p.resolve().is_relative_to(root), 'post-extraction escape')
        require(stat.S_ISREG(p.lstat().st_mode) or p.is_dir() or p.is_symlink(), 'unexpected output')
    usage = allocated()
    require(usage + RESERVE < LIMIT, 'final allocation limit')
    result = {'members':len(members), 'actual_tar_bytes':expanded, 'declared_payload_bytes':total,
              'allocated_bytes':usage, 'reserve_bytes':RESERVE, 'safe_data_filter':True,
              'self_check':'one valid and nine rejected synthetic member lists',
              'execution':'none; stdlib data extraction only', 'destination':str(destination)}
    (EVIDENCE / 'extraction-result.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        (EVIDENCE / 'extraction-stop.json').write_text(
            json.dumps({'error_type':type(error).__name__, 'error':str(error),
                        'action':'STOP; retain task files; no extraction retry or repair'}, indent=2) + '\n')
        raise
