# B1a: bounded runtime/JCS acquisition and validation scope

Status: author draft; future permission proposal, not acquisition authority or tested pins.
2026-11-21; GPT-6 Astra (`gpt-6-astra`) / OpenCode, original persistent worker.
[Issue #22](https://github.com/Himanshu-singh04/releaselens/issues/22) fixes A1–A6.
Approved base: `541a8d3b14349a92068e320e6e3f4f58a7b26a94`, merged B1 PR #21.
Successful start: 2026-11-21 07:36:17 UTC; stop no later than 09:36:17 UTC.
Five public documents were retrieved; final limits/check evidence is recorded in the PR.

## Decision and authority

Recommend one future, separately assented task: acquire the two exact artifacts below,
inspect them, conditionally install standard-GIL CPython on the Mac with founder-admin
participation, then run a bounded research-only JSON/JCS validation on public synthetic data.
The current task produces only this packet. No founder decision is pending at dispatch.
The unavoidable choice is permission for the disclosed system-wide framework installation;
it is not pendrive-isolated. If those writes are unacceptable, stop; no alternate pin selected.

Original steering: “ok proceed with the further tasks”, plus continuing market-focused research.
[Authority record](https://github.com/Himanshu-singh04/releaselens/pull/21#issuecomment-7059346896)
limits this assignment to an acquisition/validation proposal, with no downloads or probes.
[B0d](005-adopted-policy-reconciliation.md) records separately adopted N1–N4 and the synthetic
sequence exception; its review-time status is historical following merged PR #19.
[Contract](../evidence-contract.md) and [testing](../testing.md) are the current requirements.
B1 [cases](../fixtures/mvp-cases.md) and [expectations](../fixtures/mvp-expectations.md) are
accepted source specifications after PR #21; no encoded B1 suite, executable schema or evaluator exists.
[B0b](003-json-conformance.md) reports 105 historical controls on CPython 3.13.4;
its lexical N2 and omitted aggregate accounting do not validate adopted replacement N2/N4.
Local 3.13.4, CI 3.14.4 and native observations are historical, not fresh host qualification.
Conditional CPython 3.14.10 / rfc8785 0.1.4 remains unqualified as a product stack.

The narrow gate is target identity plus strict parse/normalize/canonicalize/reparse evidence.
It can enable a later scoped pure-synthetic proposal; it does not close M0 or any M1–M4 exit.
D1–D4 remain unadopted. Customer Store/privacy/continuous identity/publication remain blocked;
noowners storage remains ineligible for customer evidence. No new storage target is selected.
The original 60-second comparison deadline still applies to the eventual demo; its terminal
I/O/scheduling enforcement remains unresolved, independently of the research tests below.

## Source ledger: five documents, retrieved 2026-11-21

Each URL below was read once as text/metadata; no linked package, signature, SBOM or binary
was fetched. Repository/issue authority is separate from this five-document external budget.
Published facts are not measurements of this Mac or verification of acquired bytes.

| ID | Primary document and exact locator | Verified claim / limit |
| --- | --- | --- |
| S1 | [Python 3.14.10 release](https://www.python.org/downloads/release/python-31410/), heading and Files/macOS row | Release dated 2026-10-25; macOS .pkg, 72.5 MB displayed, 10.15+, SHA-256 and Sigstore link. Not exact byte size or local compatibility. |
| S2 | [3.14.10 macOS guide](https://docs.python.org/release/3.14.10/using/mac.html), §§5.1.1, 5.5.1–2 | universal2 Apple Silicon/Intel; PSF Developer ID signed/notarized packages; admin/fixed paths; optional free-threaded build; customization. Updated 2026-10-25. |
| S3 | [rfc8785 0.1.4 PyPI JSON](https://pypi.org/pypi/rfc8785/0.1.4/json), info and urls wheel entry | Version, Python requirement, extras, wheel URL/size/hash, non-yanked state; licensing description. No target-runtime conformance evidence. |
| S4 | [3.14.10 license](https://docs.python.org/release/3.14.10/license.html), Terms and incorporated-software sections | PSF v2, retained notices, incorporated licenses; explicitly incomplete dependency-license list. Not a .pkg contents inventory. |
| S5 | [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html), §§3.1–3.2.4, Appendix B | Independent JCS ordering/escaping/number/UTF-8 oracle; informational RFC, not ReleaseLens numeric or bound policy. |

S1 returned an interactive-script fallback notice but its release text and file table were
readable; no browser or alternate transport was used. S4's long response was truncated after
the relevant licensing sections; no claim of reviewing every incorporated notice is made.
No additional primary-source lookup is needed for this bounded proposal; do not follow links.

## Exact acquisition facts and unresolved provenance

CPython release 3.14.10 is still published; this is not a claim it is the newest patch.
S1 artifact: `python-3.14.10-macos11.pkg`, macOS installer, displayed 72.5 MB.
URL: `https://www.python.org/ftp/python/3.14.10/python-3.14.10-macos11.pkg`.
Published SHA-256: `286c7018aa2730f6747ca433dccdc2b31be45f078a9ea0ffa44d5f06368fd2d7`.
S1 links the same URL plus `.sigstore`; the macOS SBOM cell is blank.
S2 says universal2 supports Apple Silicon/Intel and typically macOS 10.15 onward;
the `macos11` filename is not evidence that 10.15 is unsupported. S1 explicitly says 10.15+.
S2's general signed/notarized claim is not an observed signature of this specific .pkg.
No Sigstore identity/certificate chain or exact installer contents was inspected now.

S3 artifact: `rfc8785-0.1.4-py3-none-any.whl`, exactly 9240 published bytes.
URL: `https://files.pythonhosted.org/packages/4d/78/119878110660b2ad709888c8a1614fce7e2fab39080ab960656dc8605bf6/rfc8785-0.1.4-py3-none-any.whl`.
Published SHA-256: `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
Uploaded 2024-09-27T16:33:29.683421Z; yanked=false, requires_python `>=3.8`.
The wheel tag and pure-Python description imply no platform-specific wheel requirement;
they do not prove 3.14.10 compatibility. All requires_dist entries are optional extras.
Select none of dev/doc/lint/test; no mandatory dependency or source build is proposed.
S3 has_sig=false; do not interpret that legacy flag as proof that no attestations exist.
Publisher is described as Trail of Bits; no independent wheel signature/attestation verified.
The metadata vulnerabilities list is empty; that is not a security audit or safety guarantee.

Both hashes match the historical B0/B0b published values. No conflicting artifact fact found.
Neither artifact was acquired or rehashed here; cached historical bytes were not inspected.
Future permission should trust the exact published wheel hash over TLS plus archive inspection;
for CPython additionally require native package-signature/Gatekeeper verification before install.
Sigstore verification remains unperformed; do not download a verifier or claim it implicitly.

S4 licenses Python under PSF v2; retain its copyright/license and incorporated notices.
Its OpenSSL section covers Apache-2.0 for 3.0+; other bundled libraries have their own notices.
S2 mentions bundled Tk/OpenSSL; their exact versions/dependency closure await .pkg inspection.
S3's description/classifier says Apache-2.0 and attributes adapted Rundgren implementation;
license/license_expression/license_files metadata fields are null, not a waiver of obligations.
Retain actual wheel LICENSE and any NOTICE/attribution found after acquisition. No redistribution
or product packaging is requested. Review installer license text before founder-admin acceptance.

## One practical future path and affected locations

Use the official .pkg, standard GIL only, and explicit interpreter paths. No source build,
Homebrew, alternate distributor/runtime, Rosetta fallback or product build backend is proposed.
Names below are proposed destinations, not existing-path or free-space observations.

| Location | Proposed contents / scope |
| --- | --- |
| Mac `/Library/Frameworks/Python.framework/Versions/3.14/` | Target standard framework; interpreter `bin/python3.14`; system-wide, admin writes. |
| Mac framework root / Versions/Current | Installer may change shared framework links; inspect scripts and existing consumers before permission is exercised. |
| Mac `/Applications/Python 3.14/` | Installer resources if required; inspect selected component inventory, do not launch GUI/certificate helpers. |
| Mac `/var/db/receipts/` and installer logs | Normal installer bookkeeping; inventory exact receipts, not claimed names. |
| Pendrive `/Volumes/AIWorkspace/caches/releaselens/b1a-runtime/` | Fixed pkg/wheel files, extracted inspection copy, target venv, temporary data; outside Git. |
| Pendrive `/Volumes/AIWorkspace/projects/releaselens/artifacts/b1a/` | Ignored raw manifests, observations/results and logs; no secrets or customer evidence. |
| Future branch `experiments/b1a/`, `fixtures/b1a/`, `docs/decisions/` | Separately permitted research source, reviewed expectation manifest/recipes and results note; no files created now. |

S2 explicitly says installers cannot be relocated using installer -domain. Choosing a pendrive
venv/cache does not relocate the Mac framework or eliminate admin privilege/system effects.
Disable Shell profile updater, UNIX command-line tools and Free-threaded Python components;
omit optional documentation/apps if the actual package permits. Exact choice identifiers and
dependencies are unknown until inspected; do not copy the guide's beta/example identifiers.
No `/usr/local/bin` links, shell-profile/PATH edits, aliases, activation, service configuration,
`/usr/bin/python3` changes, PythonT framework, or replacement of an existing 3.14 install.
Preflight must establish selected framework scripts will not redirect any existing service
through shared links; if that cannot be established, stop before privileged installation.
Do not claim transaction rollback or an unaffected runtime solely because PATH was untouched.

Do not run `Install Certificates.command`: S2 says it downloads/installs certifi. The research
venv will operate offline; downloads use existing TLS-validating system tooling, not target pip.
Do not change certificate stores, trust settings, global environment or service runtimes.
Package inspection must expose any automatic network/postinstall action before founder-admin run.

Estimate only: <100 MB artifact transfer, up to 2 GiB pendrive working space and 2 GiB Mac
space reserved for install/staging; these are conservative planning allowances, not measurements.
Future read-only capacity check and installer estimate must fit; insufficient space means stop,
not deleting caches or expanding paths. Retain small logs; generate boundary inputs one at a time.

## Proposed action sequence after separate assent

1. Record exact authorization/revision and preflight target path absence, free space, OS/CPU,
   existing framework links/receipts and service interpreter bindings. No native storage probes.
2. Download-only: fetch only the exact S1 pkg and S3 wheel over verified HTTPS to the cache.
   Recheck S1/S3 metadata; use existing curl with `--fail --proto '=https'`, without following
   redirects or retry/insecure options. Require HTTP 200; any redirect stops before following.
   Record URLs, sizes and local SHA-256; reject mismatch, missing file or changed metadata.
   Network is limited to these python.org/PyPI/file-host requests; no package execution yet.
3. Inspect using existing `shasum -a 256`, `pkgutil --check-signature`, `spctl --assess --type install`,
   `pkgutil --expand`, installer choice/payload/script listings and read-only wheel ZIP listing.
   Require trusted PSF signing identity, valid assessment, expected destinations and inert wheel
   contents; absent verification capability or unexpected scripts/dependencies stops installation.
   Record actual signer chain/team identity; none is guessed here. Existing macOS trust assessment
   may contact Apple services: include that OS-managed verification in future assent, not TLS bypass.
4. Founder-admin alone performs the inspected customized installation through macOS Installer;
   worker does not request/store credentials or acquire broad sudo. Compare before/after inventory.
   Unexpected link/profile/service changes are failure, not an authorized automatic repair.
5. Invoke only `/Library/Frameworks/Python.framework/Versions/3.14/bin/python3.14`, with `-I -B`;
   verify version/build, arm64 execution and standard-GIL configuration before creating the venv.
   Create cache subdirectory `venv` via that interpreter's `-m venv --without-pip`; no activation.
6. Inspect and record the target's bundled pip wheel version/hash/license, using its existing
   ensurepip or configured bundled-wheel directory. No target pip/build-tool version is assumed.
   Permit only that bundled pip as bootstrap tooling; missing/ambiguous/incompatible wheel stops.
   Use its isolated invocation to install only the pinned local rfc8785 wheel into the new venv,
   with pip `--isolated` and `--no-index --no-deps --require-hashes --no-cache-dir`, using a
   one-entry exact-version/hash requirements file and the local wheel directory; no index/upgrade.
   Record installer identity separately from runtime dependency; inventory must show only rfc8785.
7. Run reviewed research checks offline through cache `venv/bin/python`, not host/default Python.
   Capture commands, exit codes, types/bytes/reasons, versions and evidence manifests, then stop.

The bootstrap helper itself needs explicit research-code permission; this packet supplies none.
All target imports and numeric/byte experiments belong to the future task, not preflight here.
No downloaded tool, pip upgrade, backend, compiler, signing utility or trust-store repair fallback.
Cleanup owner: worker removes only task-created cache/venv/scratch after retaining review evidence.
Founder-admin owns system cleanup using the captured install inventory; no blanket framework
removal, deleting old versions, or guessed shared-link restoration. On partial install, stop and
retain receipts/logs for coordinator/founder disposition; do not promise automatic rollback.

## Bounded independent validation and pass/stop evidence

Future research cap: one harness/manifest pair, at most 96 new named checks, plus unchanged
105 B0b controls as a separately labelled historical regression group; no fuzzing/download corpus.
The new harness includes the bootstrap adapter; legacy controls retain their own legacy adapter.
Do not feed adopted N2 normalization into lexical-N2 controls and relabel discrepancies as passes.
Independent coordinator reviews expectations/recipes before execution, with clause and source
locators. Literal RFC bytes/bit-pattern expectations come from S5, never candidate self-output.
Two executions maximum (initial plus identical confirmation); any mismatch stops qualification.
At most two working sessions / four worker hours after prerequisite admin work; no automatic reruns.
Limit generated raw test inputs to 25 MiB + 1 byte each; process one boundary recipe at a time.
Use standard-library parent-process timeout handling at 30 seconds per check; timeout is failure, with elapsed
time/termination recorded, not evidence for the product's harder 60-second completion obligation.
Any provider/quota/transport error stops without retry, alternate provider/model or allowance bypass.

| Group | Exact proposed oracle / retained evidence |
| --- | --- |
| Identity | Exact CPython 3.14.10, standard GIL, arm64, explicit framework/venv paths; record sys.version/build/config, OS, package inventory and artifact hashes. Other identity rejects this qualification. |
| Strict JSON | Reject duplicate decoded keys (including escaped spelling), invalid UTF-8, lone surrogate, BOM, malformed/trailing data and nonfinite tokens. Valid Unicode/string bytes retained; no normalization. Contract encoding/shared shapes; S5 §3.1/3.2.2.2. |
| JCS controls | S5 Appendix B 26 rows and §3.2.4 literal hex, plus §3.2.3 UTF-16 ordering, recursive object sort, unchanged array order and exact control escaping. Distinguish RFC-allowed large numbers from ReleaseLens N1 rejection. |
| N1 | Accept 9007199254740991; reject 9007199254740992, 9007199254740993e0, 1e30 and 9007199254740991.5. Check signed counterparts, exact decimal integral bound before float conversion and unsafe rounded integral/nonfinite result afterward. |
| N2 | 1/1.0/1e0 and 1.0000000000000001 normalize to exact integer 1; true remains boolean, never coerced. 1.5 remains finite non-Scalar. Verify type/value before and after JCS reparse, same canonical bytes/hash for numeric equivalents, distinct boolean bytes/type. |
| N3 | Reject nonzero 1e-400 underflow and signed counterpart; preserve nonzero ±5e-324; signed exact zero normalizes to integer 0 and canonical 0. Record accept/reject/type and round-trip result. |
| N4 raw | At-bound and one-byte-over 5 MiB suite, 25 MiB bundle, 1 MiB artifact content-value token; include quotes, escapes, internal whitespace, multibyte UTF-8. Measure original token spans before decoding. |
| N4 decoded | At-bound and one-byte-over 20 MiB independently for authoritative, baseline/candidate bundle and embedded suite artifact arrays; text UTF-8 versus JSON JCS bytes. Equal IDs never merge array budgets. |
| N4 depth | Root object/array depth 1, primitive 0; 32 accepts, 33 rejects; braces/escaped quotes inside strings do not add depth. BOM rejects, never stripped before accounting. |
| Diagnostics | Contract Diagnostic/Location and SDD error classes: fixed E_SCHEMA for parse/invalid required type, E_LIMIT for byte/depth bound. Known input location or null; no input values, hostile keys, paths, traceback or library exception text. No product exit-code claim. |

Use adopted [numeric/boundary oracles](../testing.md#adopted-numeric-and-boundary-oracles-unperformed)
and B1 paper annotations as independent policy references; do not edit B0b's lexical expectations.
N2 checks cover nested artifact content and representative expected/actual/subject/integer-field
type gates without implementing Suite/Bundle schemas or evaluator outcomes. Reject non-Scalar
expected/subject values; an observed wrong type would later be TYPE_MISMATCH, not coerced equality.
N4 tests separately exercise byte-accounting components and containing-input limits; a passing
component at 20 MiB does not mean an envelope violating another bound is valid. No false fit claim.
Short accounting oracle: quoted literal é is 4 raw bytes, quoted backslash-u00e9 is 8; decoded
text is 2, JSON-string JCS is 4. Outside-token whitespace counts only toward the input envelope.
MiB is exactly 1048576 bytes. Include same decoded text with larger escaped/raw spelling and
JSON internal whitespace: raw rejection must not be bypassed by re-encoding before measurement.
Schema count limits (1000 cases/20 assertions/200 events/2000 artifacts) remain later Contract
obligations; this accounting harness does not implement or qualify full schema/reference validation.
Diagnostic observations use fixed synthetic canaries and compare captured output to a reviewed
allowlist; research results are not a shipped CLI/Diagnostic implementation or T-* completion.

Minimal permitted future harness: token-span/duplicate/number adapter, normalization/type checks,
JCS call/reparse and per-array accounting against independently fixed recipes. Keep it under
research paths, with no product imports, Store, schema model, B1 encoding or reusable CLI/API.
Record every check's expected/actual and source; mismatch stays failure. Passing finite controls
supports only this target/finite scope, not universal JCS conformance or product readiness.

## Exact proposed authorization and remaining limits

Proposed single assent: permit the seven-step sequence and bounded harness above at $0 new spend,
for these two hashes and named paths, including founder-admin customized Mac framework install,
with reviewed expectations and the listed stop conditions; retain source/manifests/results for review.
Inputs: this reviewed packet, merged contract/testing/B1, unchanged B0b controls and S1–S5.
Output: one research PR plus outside-Git acquisition/install/validation record; no next-task dispatch.
Retain dated source URLs, download/local hashes, signature output, choice/payload/script inventory,
before/after system effects, license files, pip identity, expectation-review revision, harness SHA,
per-check expected/actual/type/bytes/reason, timing, exit codes and every failure; binaries stay out of Git.
Acceptance: verified bytes/signature/install boundary, exact target/bootstrap inventory, all
independently reviewed checks pass twice, reproducible evidence, no historical/control changes.
Any failed identity/check/limit, unexpected write/network/dependency, uncertain service impact,
changed artifact or inability to inspect selected installer behavior stops the affected step.
The smallest remaining empirical facts are installer choices/scripts/shared-link effects and
target bundled-pip identity; these require acquisition permission, not another broad stack study.
Do not install if customization cannot honor unchanged PATH/service runtimes; return the conflict.

Later B1 encoding requires separate permission after qualification; later pure Contract/Evaluator/
terminal renderer requires its own scoped acceptance and resolution of applicable deadline gates.
No customer/path imports, Store, persisted reports, release package, native ABI/probes, models,
AI integration, customer outreach/intake, or market-readiness claim follows. M0/M1–M4 stay open.
This task stops at independent review; the future permission above has not been granted.
