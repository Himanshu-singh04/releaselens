# B0 runtime recommendation and investigation results

Current status: **B0 research accepted; implementation NO-GO.** [PR #11 merge verification](https://github.com/Himanshu-singh04/releaselens/pull/11#issuecomment-7000315548)
records conditional acceptance at main `1bfa0576aabfbb17a9a625a513a1d7dea6079eb3`.
This accepts the investigation/direction, not tested pins, M0 completion or runtime/storage
changes. The recommendation, pending-gate wording and observations below retain their B0
review-time context; [issue #12](https://github.com/Himanshu-singh04/releaselens/issues/12)
now assigns the separately authorized [B0a documentation protocol](002-storage-protocol.md).
Date: 2026-11-19. Author: GPT-6 Astra (`gpt-6-astra`), OpenCode, persistent ReleaseLens worker.

## Question, scope, and recommendation

[Issue #10](https://github.com/Himanshu-singh04/releaselens/issues/10) preserves the assignment
and A1–A6. Original founder instruction: “ok proceed”, responding to runtime-choice
assignments. This investigation compares two runtimes for the existing [contract](../evidence-contract.md)
and RL-001–012; it does not authorize a scaffold, evaluator, installation, or filesystem changes.
Bound: documentation, primary-source research, and read-only host/capability observations.

**Recommend CPython 3.14.10 as the next validation target**, using standard-library
CLI/parsing/evaluation/rendering, with `rfc8785` 0.1.4 as an untested JCS dependency
candidate and a small reviewed Darwin native bridge for missing storage APIs. Prefer
this over TypeScript/Node 26.13.1 because Python already exposes descriptor-relative
operations and this repository already maintains Python checks. No maintainer language
preference or performance advantage has been measured. Python is not a zero-dependency
solution to the full contract; removing the bridge/JCS obligations would change requirements.

Three blockers prevent M0 completion: the current pendrive is mounted `noowners`;
neither runtime alone establishes all private-access/mount/publication guarantees;
the proposed Python/JCS/native packaging combination has not been installed or validated.
Supported upstream releases are research evidence, not a tested product support matrix.

## Observed host evidence

Commands ran in `/Volumes/AIWorkspace/projects/releaselens`, on synchronized main
`4a47f996da28ac761842c4bd050c9e1d946bc279`, then branch `docs/b0-runtime-decisions`.
Version/capability snippets used only installed modules, in memory; no product tests ran.

| Command / inspection | Observed result | Limit |
| --- | --- | --- |
| Scoped `git fetch origin main`; `git merge --ff-only origin/main` | Already up to date; initially clean main | No main push. |
| `python3` printing `sys.version`, `sys.executable` | 3.13.4; `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` | Installed foundation interpreter, not recommended product pin. |
| `node --version`; `npm --version`; `shutil.which('tsc')` | v26.13.0; 11.20.0; tsc not on PATH | Node 26.13.1 and a TS compiler were not tested. |
| `importlib.metadata.version` for pip/rfc8785 | pip 26.1.2; rfc8785 absent for this interpreter | No dependency installation. |
| `sw_vers`; `platform.machine()` | macOS 27.2.1, build 26B131; arm64 | Target host only, not a supported-platform claim. |
| `xcrun --show-sdk-version`; `clang --version` | SDK 27.2; Apple clang 21.0.0 (`clang-2100.4.1.1`) | Headers inspected; no helper compiled. |
| `diskutil info -plist /Volumes/AIWorkspace`; `mount` | External USB APFS; `GlobalPermissionsEnabled=false`; `noowners`; encryption false | **Reject for product private evidence/output under current requirements.** No ownership changes made. |
| `ls -lde /Volumes/AIWorkspace /Volumes/AIWorkspace/projects/releaselens` | Mode 0775 volume root, 0755 checkout; no ACL entries printed | Does not prove effective privacy, particularly with noowners. No credentials inspected. |
| `os.supports_dir_fd`, flags, retained read-only checkout fd | open/mkdir/stat/rename/link/unlink supported; O_NOFOLLOW/O_DIRECTORY/O_CLOEXEC present; fstat/fstatvfs succeed | fstatvfs flags were 0x2; these are not Darwin's complete native mount flags. |
| `getattr(fcntl, 'F_FULLFSYNC', None)` | 51 | Constant availability is not durable-flush evidence. |
| Installed `json.loads`, `json.dumps`, `sorted` | Duplicate x keeps last value; NaN accepted; `[1.0,-0.0,1e-06]`; U+FB33 sorts before U+1F600 | Default Python JSON/sort is not strict JSON/JCS. |
| Installed Node JSON/fs inspection | Duplicate x keeps last value; `[1,0,0.000001]`; U+1F600 sorts before U+FB33; fs.openat/fs.fstatfs undefined | Illustrative language/API behavior, not a conformance suite. |

To repeat the key read-only Python capability inspection:

```sh
python3 - <<'PY'
import fcntl, importlib.metadata, os, platform, shutil, sys
print(sys.version, sys.executable, platform.machine())
print('tsc:', shutil.which('tsc'))
print('dir_fd:', sorted(f.__name__ for f in os.supports_dir_fd))
print({n: getattr(os, n, None) for n in ('O_NOFOLLOW', 'O_DIRECTORY', 'O_CLOEXEC')})
print('F_FULLFSYNC:', getattr(fcntl, 'F_FULLFSYNC', None))
for name in ('pip', 'rfc8785'):
    try:
        print(name, importlib.metadata.version(name))
    except importlib.metadata.PackageNotFoundError:
        print(name, 'not installed for this interpreter')
fd = os.open('.', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)
try:
    print(os.fstat(fd), os.fstatvfs(fd))
finally:
    os.close(fd)
PY
```

## Alternatives against the contract

| Concern | TypeScript / Node 26.13.1 | Python standard-library baseline / CPython 3.14.10 |
| --- | --- | --- |
| Contract and maintenance | Discriminated unions suit Event/Ref/Result. Type stripping does not type-check; compiler and runtime validation still needed [N3]. More tooling alongside existing Python checks. | json, hashlib, datetime, html, argparse and unittest cover much of the CLI. Runtime shape/type validation remains necessary; `True == 1` must not implement exact Scalar equality. Fewer tools, less static enforcement. |
| Strict import | JSON.parse loses duplicate names; a duplicate-preserving/token parser is still required. UTF-8 fatal decoding, unsafe-number and lone-surrogate rejection cannot be assumed from parsing. | json.object_pairs_hook can reject decoded duplicate keys (including escaped aliases); parse_int/parse_float/parse_constant support numeric rejection. Explicit strict UTF-8 and surrogate checks required [P3]. `strict=True` alone is insufficient. |
| JCS / determinism | ECMAScript primitive serialization and UTF-16 sorting align with JCS; recursive property ordering, finite values and Unicode validation still required [J1]. Sorting keys into an ordinary object then stringify can re-order integer-like keys. | json.dumps(sort_keys=True) is not JCS: float formatting, negative zero and code-point ordering differ. rfc8785 0.1.4 is a credible small candidate [J2], not a verified implementation pin. |
| Storage | fs retains file handles but lacks documented openat/mkdirat/renameat and Darwin ACL/fstatfs wrappers [N2]. A native bridge is required; v26.13.1 has experimental node:ffi, not a proven storage abstraction [N4]. | os dir_fd + no-follow operations reduce the bridge surface [P4]. Darwin ACL/volume identity and exclusive rename still require native bindings. ctypes alone does not prove ABI correctness. |
| Packaging | Built JS plus exact compiler/parser/JCS dependencies, package-lock.json and npm ci; native addon/helper complicates platform builds. Native TS execution is not a substitute for checking or a proven distributable [N3]. | Versioned interpreter plus venv and a local wheel/package. Pure-stdlib distribution would be simple but fails full JCS/native-storage needs. Native bridge makes a single portable zipapp insufficient. venv must be recreated, not moved [P6]. |
| Support lifetime | Node 26 LTS; scheduled maintenance 2027-10-20, EOL 2029-04-30. v26.13.1 lists macOS arm64 >=13.5 Tier 1; vendor-EOL OS versions excluded [N1]. | 3.14 bugfix/binary phase expected through October 2027, source-only security through October 2030 [P2]. 3.14.10 macOS installer lists 10.15+ [P1]; this does not prove ReleaseLens on every such OS. |
| Resources / cost | Local CPU, no hosting/inference fees. Timer on a blocked event loop cannot enforce the hard deadline; native calls need a bounded termination strategy. | Local CPU, no hosting/inference fees. Signals/monotonic checks alone may not interrupt blocked native I/O reliably; same deadline gate. Neither has measured T-08 memory/time evidence. |

Both retain explicit imports, pure evaluation, offline escaped HTML, immutable snapshots,
tri-state results, expected-suite denominators and zero product network/inference. Neither
needs a database, web framework, model SDK or paid service. CI stays within existing allocation.
Python 3.15.2 is also published [P1 index], but no needed 3.15 feature justifies adding a fresh
major-version variable. 3.13.4's presence is not a reason to freeze an old patch for product use.

Strict parsing must retain the current safe-integer/finite-binary64 contract, including
exponent-form numbers; a float rounded into an unsafe integer cannot evade validation.
Bound bytes and lexical depth before expensive decoding, then reject unknown fields and
bad references before evaluation. Exact numeric-token edge policy and deadline enforcement
must be reviewed with ADR-2/4. No integer-only rewrite, Unicode normalization, or relaxed
duplicate handling is proposed to simplify either implementation.

## Candidate pins, acquisition, and reproducibility

| Item | Recommendation / evidence level | Acquisition and license |
| --- | --- | --- |
| CPython | **3.14.10 research target**, standard GIL build; not installed/tested here | Official python.org macOS installer [P1], PSF-2.0 plus incorporated notices [P5]. Future separately authorized installation, explicit interpreter path, then project venv; no changes to global PATH or existing service runtimes. |
| Standard-library modules / venv | Same **3.14.10** as interpreter | No separate parser, test-runner or HTML-template dependency proposed. |
| JCS | **rfc8785 0.1.4 candidate**, not installed; metadata >=3.8, no mandatory dependencies; source inspected, not executed | Apache-2.0; upstream wheel and notices [J2]. No optional dev/test extras assumed. |
| Installer/build tools | pip **26.1.2 observed only**; recommended pip/build-backend pins **blocked pending target-interpreter validation** | Future exact hashed tooling lock, separate from runtime requirements. No unpinned build-isolation downloads. |
| Darwin bridge | No release/version exists; proposed first-party narrow C ABI, packaged with product | Observed Apple clang 21.0.0 + SDK 27.2 are investigation tools, not a tested build pin. Retain SDK/toolchain provenance and applicable notices; do not redistribute the SDK. |
| Node alternative | **26.13.1 upstream candidate**; npm 11.20.0 observed only; TS/parser/JCS pins unestablished | If chosen instead, exact package-lock and compiler/native-toolchain validation required; no assumed npm compatibility from host presence. |

Upstream-published SHA-256 values, **not hashes of locally acquired artifacts**:

- `python-3.14.10-macos11.pkg`: `286c7018aa2730f6747ca433dccdc2b31be45f078a9ea0ffa44d5f06368fd2d7` [P1].
- `rfc8785-0.1.4-py3-none-any.whl`: `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48` [J2].

After separate authorization: verify downloaded bytes/signatures against the recorded source;
record interpreter/build/OS/architecture, exact pip and build backend, native bridge source SHA,
SDK and compiler. Commit a hash-locked runtime requirements file and separate build-tool lock;
install only reviewed wheels into a fresh venv using `--require-hashes --no-index` with an
explicit wheel directory. No dependency auto-update on comparison. Keep binaries/envs outside
Git. Include source, licenses, synthetic examples and package hashes in a future release record.

Validation before converting candidate pins into tested pins: use RFC 8785 section 3.2.3 and
Appendix B vectors independently of package snapshots; test duplicate escaped keys, invalid
UTF-8/surrogates, safe-integer boundaries, exponent overflow, negative zero and UTF-16 order.
Run the same allowed values through both implementations as a differential check. Validate
ten identical Result hashes later in T-06. Inspect rfc8785 exception handling: messages may
contain values and must become fixed Diagnostics. Its source uses Python float stringification;
metadata >=3.8 is not proof of binary64 edge conformance on 3.14.10. These tests are **unperformed**.

## Mac/APFS storage feasibility and blockers

Proposed narrow target: the observed arm64 macOS build, local APFS **with ownership enabled**,
one writer, regular nonsymlink inputs, an explicitly chosen owner-private output parent and
no extended ACL entries on evidence-bearing objects. Broader macOS versions, Linux, Windows,
network/exFAT volumes and permissive ACL equivalents are unsupported until tested. This is
a proposed support boundary, not a claim that the current noowners pendrive qualifies.

The Store.prepare/publish seam remains responsible for I/O; Importer only reads the returned
pinned files; Contract owns strict parse/hash rules; Evaluator and Renderer remain independent
of native APIs. A bridge belongs under Store, not in each component. Proposed native surface:
descriptor-based mount/volume facts and ACL inspection, plus exclusive descriptor-relative
publication. No shell command, path-based ACL subprocess, privilege escalation, general FFI
interface exposed to imports, or per-operation path reopening is an acceptable substitute.

1. **Pin the traversal.** Open a trusted anchor and each path component relative to its
   retained directory fd with O_DIRECTORY/O_NOFOLLOW/O_CLOEXEC; reject `..`, links and
   unexpected device transitions. Retain the parent chain, volume root, input and output fds
   in IoContext. Validate fstat type/owner/dev/inode and parent-entry identity with no-follow
   fstatat checks. Read/hash from the same input descriptors; pre/post metadata comparisons
   detect ordinary mutation but do not prove exporter honesty or freeze same-user writers.
2. **Bind volume and mount.** A compiled shim can expose fstatfs(fd) (filesystem type, fsid,
   native flags including MNT_IGNORE_OWNERSHIP) and fgetattrlist on the retained volume-root
   fd (ATTR_VOL_INFO, UUID, capabilities and valid-attribute masks) [D1–D4]. Reject missing
   UUID/ACL support, noowners or any mismatch. UUID identifies a volume, not a unique mount
   lifetime: keep the original fds, dev/fsid and parent-entry relationships; never reacquire
   after loss. Revalidate around reads/writes, marker publication and final success. A
   pathname-only diskutil check or os.fstatvfs result cannot replace these checks.
3. **Prove private access.** Verify effective owner, deny group/other access, inspect
   ACL_TYPE_EXTENDED through acl_get_fd_np and enumerate entries (acl_free on all exits).
   Initially reject all nonempty extended ACLs on private parents/files rather than try to
   model every allow/deny/inheritance combination. Also reject ancestors permitting ordinary
   users to replace the private tree. Create an exclusive empty probe under the pinned parent,
   inspect inherited ACL/owner/mode, verify usable access through its fd, and require a prior
   platform acceptance test denying a different ordinary account's open/traverse attempts.
   Per-run empty-object checks supplement that negative-access test; the writer's os.access
   cannot test another account. No chmod/ACL repair fallback. Check every empty output before
   evidence writes, and recheck at completion. No effective-access test ran in B0.
4. **Publish without overwrite.** mkdirat a new private generation; exclusive-create files
   relative to its fd, validate empty objects, write complete bytes, flush user buffers,
   fsync and F_FULLFSYNC the data files, then flush directory metadata. Prepare/flush a private
   temporary marker; publish it last with renameatx_np(RENAME_EXCL) inside the retained
   directory, flush required directory metadata, then revalidate identity/privacy before
   announcing success. Retain the output-parent fd for generation-entry durability too.
   Any unsupported/error return fails; os.replace (overwrite) is not an alternative.
   This sequence is a **candidate protocol**, not an APFS durability test result.

Native gaps remain even with Python: no stdlib acl_get_fd_np, native fstatfs/volume UUID,
or renameatx_np wrapper; ctypes would move C layout/ownership errors into Python, not remove
them. Node's experimental FFI has equivalent ABI/lifetime risks and additionally needs the
descriptor-relative operation surface. Prefer a small compiled, versioned shim with fixed
types over handwritten struct offsets; helper ABI/build/distribution is an unresolved gate.

**Limits that block a go decision:** retained descriptors prevent redirection to replacement
paths but cannot by themselves prove that the original pathname remains continuously bound.
A swap-and-restore between checks, ACL changes by the owner, or forced detach immediately
after the last check cannot be excluded by sampling. R7's no-success requirement around
publication therefore needs an explicit achievable failure model and evidence; adding a
helper does not make that guarantee atomic. Keep R7 unchanged and mark it unverified.
Privileged/same-account interference is already outside the privacy promise, but that does
not waive the required mount-loss tests or permit silent path fallback.

Apple's archived fsync/fcntl material predates APFS and notes devices may ignore flush
requests [D2]. SDK symbols establish API availability, not APFS directory-flush ordering or
USB power-loss guarantees. Directory fsync/F_FULLFSYNC support and marker persistence must
be tested on the supported target; failures cannot be ignored. A valid marker/file-hash pair
is a recovery convention, not proof that the process observed its final success checkpoint,
nor a disk-loss guarantee. No live drive ejection, write probe, ACL/ownership change, native
build, second-account test, fault injection, or power-loss test occurred in this assignment.

## ADR disposition and next bounded work

All five founder confirmations remain **pending** for this recommendation. Prior planning
approval is recorded in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6), not
inferred as approval of these choices. M0 remains incomplete.

| Gate | Recommended / deferred / blocked | Dependency and evidence required |
| --- | --- | --- |
| ADR-1 runtime/package | **Recommended conditionally:** CPython 3.14.10; **blocked** as implementation pin | JCS candidate conformance, exact installer/build locks and native storage ABI/compatibility. Node remains viable if its larger native surface is justified. |
| ADR-2 storage/identity | **Recommended:** existing JSON v1 snapshots, JCS + SHA-256, no SQLite; **blocked** on canonicalizer/parser validation | Preserve references, provenance and hashes; settle numeric-token edge handling without weakening safe-integer rules; T-01/02/06. |
| ADR-3 evaluation/authority | **Recommended:** existing exact tri-state/effect/expected-suite rules, no live execution | Explicit owner decision, independent eight-case expectation review then T-03–06. No probabilistic judge. |
| ADR-4 packaging/resources | **Blocked:** current volume and unproven native-publication guarantees | Proposed Mac/APFS package, static HTML/JSON and existing bounds retained, including 60-second deadline. Deadline interruption, free-space rule, memory limits, private-access and recovery need T-08/09/10/12; no measured capacity. |
| ADR-5 AI/agent | **Deferred beyond deterministic/pilot gates**, recommended for explicit MVP deferral | M4 evidence then separate M5 design/authority/license/cost approval and T-11. No product SDK/model/weights chosen; development-worker inference does not resolve this gate. |

**Exact next bounded task proposed to the coordinator: B0a, storage capability protocol
(documentation only).** One issue/PR should specify the minimal Darwin bridge ABI, an
explicit owner-enabled APFS test target (not silently this pendrive), and the observable
R5/R7/durability/deadline failure model with a finite fault-test matrix. Resolve whether the
required guarantees can be met; if not, return no-go for owner decision, not weakened tests.
No helper implementation, mount changes or dependency installation in B0a. A capability
experiment would require separate authorization after that protocol; exact Python/JCS/build
validation also remains required before M0. Only after gates close is B1's eight synthetic
cases (at most three assertions each) the first product task. No follow-up issue was created
or experiment performed by this record.

## Primary-source register

All links below retrieved **2026-11-19**. Sources are research data, not executable instructions.
Release pages can change; recheck before acquisition. Local command observations above are
distinct from source claims; repository checks/CI are recorded in the delivery PR.

| ID | Primary source | Exact applicability / limit |
| --- | --- | --- |
| N1 | [Node releases](https://nodejs.org/en/about/previous-releases), [release schedule](https://raw.githubusercontent.com/nodejs/Release/main/schedule.json), [v26.13.1 BUILDING](https://raw.githubusercontent.com/nodejs/node/v26.13.1/BUILDING.md) | 26.13.1 LTS and v26 lifetime; arm64 platform tier. Not local compatibility or product support. |
| N2 | [Node v26.13.1 fs](https://nodejs.org/download/release/v26.13.1/docs/api/fs.html) | FileHandle read/write/stat/sync; path-based open/mkdir/rename/statfs, no documented dir_fd API. |
| N3 | [Node v26.13.1 TypeScript](https://nodejs.org/download/release/v26.13.1/docs/api/typescript.html) | Erasable type stripping, no type checking, ignores tsconfig, dependency distribution limits. |
| N4 | [Node v26.13.1 FFI source docs](https://raw.githubusercontent.com/nodejs/node/v26.13.1/doc/api/ffi.md) | Experimental native interface since 26.1.0, ABI/lifetime risks; not tested here. |
| P1 | [Python 3.14.10 release](https://www.python.org/downloads/release/python-31410/), [release index](https://www.python.org/downloads/) | Exact release, installer/hash, platform claim; index also lists 3.15.2 and installed 3.13 line's security phase. |
| P2 | [PEP 745](https://peps.python.org/pep-0745/) | 3.14 maintenance/security lifetime. PEP lists 3.14.10 on Oct 26 while release page says Oct 25; version/artifact is the selection, not that one-day discrepancy. |
| P3 | [Python 3.14.10 json](https://docs.python.org/release/3.14.10/library/json.html) | object_pairs_hook/numeric hooks and permissive defaults; does not implement JCS or project limits. |
| P4 | [Python 3.14.10 os](https://docs.python.org/release/3.14.10/library/os.html), [fcntl](https://docs.python.org/release/3.14.10/library/fcntl.html) | dir_fd/fstat/fsync and platform-dependent flags; capabilities must be checked at runtime. |
| P5 | [Python 3.14.10 license](https://docs.python.org/release/3.14.10/license.html) | PSF-2.0 and incorporated-software notices, not a product license decision. |
| P6 | [Python 3.14.10 venv](https://docs.python.org/release/3.14.10/library/venv.html) | Environment creation/recreation; neither portable packaging nor a security sandbox. |
| J1 | [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.txt) | Sections 3.1–3.2.4 and Appendix B; normative contract reference, not a tested library. |
| J2 | [rfc8785 PyPI metadata](https://pypi.org/pypi/rfc8785/json), [v0.1.4 implementation](https://raw.githubusercontent.com/trailofbits/rfc8785.py/v0.1.4/src/rfc8785/_impl.py), [v0.1.4 manifest](https://raw.githubusercontent.com/trailofbits/rfc8785.py/v0.1.4/pyproject.toml) | 0.1.4 wheel hash, Apache-2.0, no mandatory dependencies, >=3.8; inspected UTF-16 sort/float conversion. Compatibility/conformance untested. |
| D1 | [Apple fstatfs archive](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fstatfs.2.html) | Descriptor filesystem identity/flags semantics; old documentation, corroborated only for declarations by SDK 27.2. |
| D2 | [Apple fcntl archive](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/fcntl.2.html) | F_FULLFSYNC requests drive flush; predates APFS, not evidence of APFS/USB durability. |
| D3 | [Apple ACL archive](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/acl_get_fd.3.html), [getattrlist archive](https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man2/getattrlist.2.html) | Descriptor ACL copy/free; capabilities/valid masks and volume-root attributes. Archived examples do not prove current volume support. |
| D4 | Installed Apple SDK **27.2** headers via `xcrun --show-sdk-path` | usr/include/sys/{mount,attr,acl,fcntl,stdio}.h and unistd.h declare fstatfs, MNT_IGNORE_OWNERSHIP, ATTR_VOL_UUID, ACL APIs, openat, F_FULLFSYNC, fgetattrlist, renameatx_np/RENAME_EXCL. Header declarations only, not compiled/runtime validation. |
