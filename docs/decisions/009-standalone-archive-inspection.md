# B1c: exact standalone archive inspection

Status: exact archive acquired and statically inspected; **runtime tests have not run**.
2026-11-22; GPT-6 Astra (`gpt-6-astra`) / OpenCode, original persistent worker.
[Issue #28](https://github.com/Himanshu-singh04/releaselens/issues/28), fixed A1–A6;
[founder assent](https://github.com/Himanshu-singh04/releaselens/pull/27#issuecomment-7078081060)
to the [complete permission](https://github.com/Himanshu-singh04/releaselens/pull/27#issuecomment-7077984175).
Base `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`; start 10:56:13 UTC, stop by 12:56:13 UTC.
Technical inspection completed 11:07:49 UTC; remaining work is checks/checkpoint delivery.

## Exact scope and trust

Only release 20261110 / ID 441136779, asset 733713948:
`cpython-3.14.10+20261110-aarch64-apple-darwin-install_only.tar.gz`, 27,109,898 bytes,
SHA-256 `42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666`.
Inspection-only trust: published GitHub metadata/hash over verified TLS, not an independent
attestation, PSF signature/notarization or runtime adoption. Prior .pkg trust does not transfer.
Up to three official support documents plus exact metadata recheck; <=100 MB response bodies.
At most three manually inspected HTTPS asset redirects, hosts exactly github.com or
release-assets.githubusercontent.com; no credentials/retries/unrestricted redirects.
Signed query values stay out of public records. Changed identity/bytes/hash stops acquisition.

No target invocation, imports, pip, install/startup code, admin/system/PATH/service/trust
change or binary patch occurred. This includes no `--version` call to the extracted Python.

## Preflight and exact transfer

Fresh cache `/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection/`;
ignored raw evidence `/Volumes/AIWorkspace/projects/releaselens/artifacts/b1c/`.
Both were absent before creation; no prior files overwritten. Read-only preflight: macOS
27.2.1 / 26B131, Apple M2 arm64; filesystem available 121,246,859,264 bytes at both task roots.
Existing host Python 3.13.4 provides `tarfile.data_filter`; curl/shasum/file/otool/codesign
were present. No new tool, compiler, target runtime or native storage probe was used.

[Exact release API](https://api.github.com/repos/astral-sh/python-build-standalone/releases/441136779)
returned HTTP 200/TLS verification 0; release and asset ID/name/size/hash/start URL matched
the approved metadata. Starting asset URL:
`https://github.com/astral-sh/python-build-standalone/releases/download/20261110/cpython-3.14.10%2B20261110-aarch64-apple-darwin-install_only.tar.gz`.
One GET returned HTTP 302 to HTTPS `release-assets.githubusercontent.com`, port default,
no userinfo/fragment. Host/path/query-key inspection preceded the separate redirected GET;
query values were passed through curl stdin and retained only in ignored private headers.
Final response HTTP 200/TLS verification 0: exactly **27,109,898 bytes**, SHA-256 above,
independently matched by host hashlib and native `shasum -a 256`. No credentials/retries/-L.
Total acquisition response bodies, including metadata and three docs: **29,295,022 bytes**.
Six requests total: one metadata, three documents, two asset hops; one redirect, below three.

## Official support evidence (three documents, retrieved 2026-11-22)

| Source / locator | Published statement and limit |
| --- | --- |
| [Project README](https://raw.githubusercontent.com/astral-sh/python-build-standalone/main/README.md), Highlights/Downloads | Portable, can be installed into any path; self-contained; use install_only for normal use. Moving main documentation, not proof of this artifact's runtime behavior. |
| [Running distributions](https://docs.astral.sh/python-build-standalone/running/), archive flavors, Extra Python Software, Licensing | install_only omits optimization labels and uses fastest available configuration; 3.13+ free-threaded filenames say freethreaded. pip preinstalled; setuptools only for <=3.11. Varied licenses, libedit rather than readline, _gdbm disabled; generic licensing-metadata claim does not establish this archive's complete inventory. |
| [Quirks](https://docs.astral.sh/python-build-standalone/quirks/), terminfo and References to Build-Time Paths | Build-time absolute paths persist in sysconfig/Makefiles; uv may patch them. No uv/sysconfigpatcher acquired or used. Generic own-libedit claim is narrower than observed system-library references below; do not assert universal dependency independence. |

All three returned HTTP 200/TLS result 0 (2,334 / 45,867 / 38,547 bytes); no source gaps,
extra document, linked signature/SBOM/dependency acquisition or provider/transport error.

## Archive safety and bounded extraction

Committed [one-shot recipe](../../experiments/b1c/inspect_archive.py) is inspection tooling,
not a runtime-validation harness. `python3 -I -B experiments/b1c/inspect_archive.py` ran once
with the existing host interpreter. It rechecks exact archive bytes/hash, caps actual streamed
gzip expansion at 512 MiB, then reads the entire bounded tar inventory before extraction.
It rejects absolute/traversing/control-character paths, case/normalization collisions,
special/sparse/privileged members, duplicate paths, link ancestors/cycles/dangling targets
and unsafe hardlink ordering. One valid and nine malicious synthetic member-list self-checks
passed. The actual archive has **1,736 members: 1,727 regular files and nine relative symlinks**;
no hardlinks or explicit directory entries. Symlink targets stay inside the extracted tree.

Actual tar expansion **71,396,864 bytes**; declared member content **70,050,103 bytes**.
The recipe reserves rounded file/implicit-directory allocation and 64 MiB log headroom,
uses existing stdlib `filter='data'`, checks allocation during extraction and checks every
resulting path's containment afterward. Fresh root `cache/extracted/python/`; scratch tar
and original archive retained. Inspection-completion task allocation **175,333,376 bytes**,
well below 2 GiB; final manifest/accounting in PR includes subsequent evidence records.
No package installer, postinstall, repacking, quarantine removal, link repair or cleanup.

## Static findings and unresolved facts

Paths below are relative to `cache/extracted/python/`; raw command arrays/results retained.

- **Identity declarations:** `include/python3.14/patchlevel.h` says 3.14.10; `pyconfig.h`
  leaves Py_GIL_DISABLED undefined. Literal-only AST parsing of `_sysconfigdata__darwin_darwin.py`
  gives Py_GIL_DISABLED=0, ABIFLAGS empty, aarch64-apple-darwin, no-framework and macOS 11.0.
  `lib/python3.14/build-details.json` agrees on CPython 3.14.10 and relative base/interpreter.
  These are static declarations, not executed version/GIL/prefix assertions.
- **Build differences:** configuration declares PGO/LTO, tail-call interpreter, mimalloc and
  experimental JIT `yes-off`; do not erase these facts or infer actual JIT state. Most stdlib
  modules are recorded as built in; package/module presence and import behavior are not proved
  by config entries. Old `/install` and temporary build paths remain in sysconfig as documented.
- **Native files:** magic-byte enumeration found ten Mach-O files; native `file` and `otool`
  `-hv/-L/-l` report arm64 for all ten, minimum macOS 11.0, SDK 15.0. Main `bin/python3.14`
  loads Apple CoreFoundation/SystemConfiguration and system libSystem/z/libedit/ncurses/panel;
  no load of shared Python.framework or separate libpython is recorded for that executable.
  Its RPATH is `@executable_path/../lib`. Bundled libpython/Tcl/Tk and two extension bundles
  use system references and/or @rpath; extension RPATH `@loader_path/../..` reaches local lib.
  Tcl/Tk load versions show 9.0.4, itcl 4.3.8 and thread 3.0.6. No native load command names
  `/Library/Frameworks/Python`; this is not dynamic/transitive dependency completeness.
- **Trust:** `codesign --display --verbose=4 bin/python3.14` exited 0: ad-hoc, linker-signed,
  TeamIdentifier not set. Display is not signature verification or notarization assessment;
  no PSF/Apple publisher acceptance is claimed or inherited. No trust setting was changed.
- **Bootstrap:** only pip 26.3 dist-info in site-packages, requires Python >=3.10, MIT, no
  Requires-Dist. Vendored dependency versions/licenses and pip's own CycloneDX BOM are retained;
  they are not a whole-runtime SBOM. Vendored setuptools 70.3.0 is not installed setuptools.
  Bundled `lib/python3.14/ensurepip/_bundled/pip-26.3-py3-none-any.whl`: **1,950,951 bytes**,
  SHA-256 **`f3b60b20ffaadd4415ed7957212a38ac63fa4c5fa375bd0f4a797777940fad13`**;
  ZIP inventory 513 members / 6,187,545 uncompressed bytes. Metadata/license read as data;
  installed pip direct_url hash agrees. No pip/ensurepip import, bootstrap or installation.
- **Hooks:** bin pip/pydoc/idle/config wrappers resolve sibling python3.14 via shell realpath;
  none invoked. No `.pth`, sitecustomize/usercustomize filename or install/pre/postinstall
  hook name found. Standard site/venv/ensurepip code remains and would run only in a later
  authorized invocation. Filename scans and script inspection are not a malicious-code audit.
- **Licenses/inventory limits:** 42 license/copyright/notice-named files inventoried and hashed;
  CPython LICENSE covers PSF v2 and historical notices, pip MIT and vendored notices retained.
  No `PYTHON.json` or complete mapping of statically linked native dependency versions/licenses
  found in this install-only archive. Some notices can live inside source files; absence from
  the filename inventory is not absence of rights or all notices. Full dependency/license
  closure, runtime linking, relocation behavior, OS execution acceptance and conformance remain unknown.

## Recommendation and next boundary

**GO for coordinator consideration of a separately authorized, offline research-only identity/
bootstrap/finite-validation phase**, with the above inventory/trust gaps explicit. Support:
exact acquired bytes, bounded safe paths, documented portability, matching static identity,
relative native paths and identified local pip wheel. This is not runtime qualification,
product/distribution approval or a request to execute now. Independent review comes first.

A later concrete scope would use only this manifest-bound `extracted/python/bin/python3.14`,
an isolated fresh cache venv without activation, the exact local pip wheel above and retained
B1a `rfc8785-0.1.4-py3-none-any.whl` (9,240 bytes; SHA-256
`520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`). No new downloads or pip upgrade.
First prove exact version, arm64, GIL enabled, JIT disabled, private prefix/sys.path and needed
imports with isolated explicit invocation; then separately reviewed bootstrap code may use
offline/no-index/no-deps/hash-pinned installation. Retain actual bootstrap/runtime identities.
Do not patch sysconfig, acquire compilers/native packages, enable JIT/GUI/Tcl, repair linking
or bypass OS trust on failure. Any wrong identity, dependency/network/system write, unexpected
startup effect, budget/check failure or provider error stops; missing facts stay unknown.
Review expectations before any numeric/JSON/JCS/bound tests under original caps; no harness
prepared here. A future execution decision must explicitly address ad-hoc/hash-based trust
and incomplete distribution-wide inventory; this inspection's permission cannot supply it.

## Evidence and criterion disposition

`*.request.json`, private headers, document bodies/text, `metadata-identity.json`,
`archive-inventory.json`, `extraction-result.json`, `native-inspection.json`,
`linkage-summary.json`, `codesign-display.json`, `static-inventory.json`, `static-summary.json`
and `inspection-complete.json` retain findings. Private signed headers remain outside Git;
public provenance is redacted. Final evidence manifest hash and exact check/CI outcomes are
in the PR timeline. No acquisition/native/static command failure occurred.

A1 authority/preflight preserved; A2 exact identity/transfer verified; A3 bounded safe extraction
passed; A4 static findings supported with inventory/trust/runtime gaps; A5 later-phase proposal
only; A6 checks/preservation/full attribution/exact-head CI and literal Sourcery in PR.
**Runtime tests have not run.** Stop for independent review; no approval/merge/self-dispatch.

#25/#27, stopped records and all prior evidence remain preserved. B1a-I1 remains open;
D1–D4 unadopted; M0/M1–M4/privacy/customer storage/deadline gates open. Original oracle-before-
execution, 96-new/105-legacy/two-run requirements remain future scope, not tests run here.
