# B1d: offline validation preparation

Status: **released bootstrap failed; qualification stopped before either suite run**.

## Second-session execution result (2026-11-22)

[Preparation verification / B1d-P1 resolution](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7078858636)
and [controlling execution release](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7078860431)
authorized only reviewed execution revision **`6d758d11b164fcd22530e23003a57891dbe3b3b6`**.
The coordinator-created release file matched the published six-file map, issue, head and URL;
SHA-256 **`846051c31aa9824d6f912a46dbe3fe778dae37c1ee4bdff7a5251b18cd0a0ab1`**.
It was not regenerated or edited. All six files stayed unchanged throughout execution.
This subsequent update changes only this results note; executable/oracle/requirement files
remain byte-identical to the execution revision. Old note-manifest entries are verified against
that preserved Git blob, not rewritten to match this results revision.

Second/final worker session started **12:06:14.931025 UTC**, with **1699.398429 seconds**
previously charged and **12700.601571 seconds** remaining. Absolute worker deadline:
**15:37:55.532596 UTC**; reporting/delivery also count. The reviewed runner began its separate
7200-second sequence at **12:06:55.944251 UTC**, deadline **14:06:55.944251 UTC**. Neither clock
was reset. STOP record was persisted at **12:07:00.608388 UTC** (filesystem timestamp).
Final cumulative elapsed/remainder, including delivery, is retained in session2 evidence/PR.

Preflight checked clean exact head, explicit existing host Python 3.13.4, all six packet hashes,
release binding, empty task cache/absent execution output, and **121,047,654,400 bytes available**
at both task roots. Prior manifests and **63 + 13 + 7 + 1,773 + 9 + 16 entries** verified;
B1c tracked entries used exact #29 Git blobs, other entries direct disk before note editing.

Only this released host command was invoked, once, from
`/Volumes/AIWorkspace/projects/releaselens`:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py bootstrap 6d758d11b164fcd22530e23003a57891dbe3b3b6 /Volumes/AIWorkspace/projects/releaselens/artifacts/b1d/continuation/release.json
```

It exited **1**. Four runner-managed target children were invoked:

| Prerequisite | Observed outcome | Elapsed seconds | Child exit |
| --- | --- | ---: | ---: |
| 1: base identity | Passed reviewed identity/import/origin/path checks; inventory pip 26.3 | 0.818475 | 0 |
| 2: fresh copied venv, --without-pip | Command completed with empty stdout/stderr | 1.989367 | 0 |
| 3: empty venv identity | Passed reviewed checks; distribution inventory empty | 0.435306 | 0 |
| 4: local wheel tooling/install | Parent recorded **parent-FileNotFoundError**, sent SIGTERM and reaped child | 1.113622 | -15 |
| 5: installed payload/origin/inventory | **Not reached** | — | — |

Actual base and empty-venv identity records report **CPython 3.14.10**, build
`3.14.10 (main, Nov 11 2026, 00:14:32) [Clang 23.1.3 ]`, **arm64, GIL=true, JIT=false**.
Base prefix is the retained B1c private tree. Venv prefix is the new B1d private venv; its
sys.path excludes base site-packages, retaining the private stdlib/lib-dynload and local venv
site-packages. Needed modules resolved to built-in/frozen or retained-tree files. These
observations support only those prerequisite assertions, not numeric/JCS qualification.

Prerequisite 4 first repeated empty identity successfully and identified the exact pip wheel
hash. Its stdout then reported processing the retained rfc8785 wheel and
**“Successfully installed rfc8785-0.1.4”**. That text is not a verified installation result:
the parent failed and terminated the process, and prerequisite 5 never compared installed
payload/origins/inventory. Preserve the venv and all partial state; no cleanup or repair.

The parent recorded the exception class but not the missing pathname or originating stack
site. The reviewed allocation walk overlaps transient installer files, a possible mechanism
visible from source, **not an established or reproduced cause**. No diagnostic target command,
retry, source/oracle change, fallback or trust repair was attempted. No timeout/output-cap
failure was recorded; all four stderr streams were empty. Recorded stdout sizes were
2,292 / 0 / 2,229 / 2,734 bytes; prerequisite 4 termination list was `["SIGTERM"]`.

The STOP latch and all command/environment/identity/elapsed/exit/termination records remain
under `artifacts/b1d/continuation/execution/`. Runner's failure preservation rechecked
**63 + 13 + 7 + 1,773 + 9 entries**, with new-task allocation **79,253,504 bytes** at that point.
Additional read-only result/preservation/manifest/clock records use `artifacts/b1d/session2/`;
the final manifest/accounting and required repository/attribution/CI outcomes are in the PR.

**Run1 and run2 were not invoked. Zero of 96 new checks and zero of 105 historical controls
ran on the target; no confirmation or finite qualification result exists.** Ordinary unchanged
baseline delivery CI remains separate. No new acquisition, admin/system/PATH/service/trust/
quarantine change, package/compiler fallback, customer/product/native-storage work or bypass.

A1 exact release/input preservation verified; A2 independently reviewed oracle unchanged but
unexecuted; A3 base/empty-venv prerequisites passed, bootstrap installation validation blocked;
A4 bounded parent recorded a real failure and stopped, suite behavior unverified; A5 stop rule
honored without run1/run2; A6 results-only delivery for independent review. This is a blocked
execution outcome, not A1–A6 qualification completion, runtime adoption or product readiness.
Second session ends at the results handoff; remaining clock does not authorize a retry/new
session. No approval/merge or next-task self-dispatch. B1a-I1 and all existing gates remain.

## Frozen preparation record (execution revision above)

The following records the earlier preparation state and prospective recipe. Its statements
about unexecuted commands or an absent release file describe that checkpoint; the results
above supersede those temporal claims without changing the reviewed code or expectations.

2026-11-22; original GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode worker.
[Issue #30](https://github.com/Himanshu-singh04/releaselens/issues/30), fixed A1–A6;
[complete briefing](https://github.com/Himanshu-singh04/releaselens/pull/29#issuecomment-7078385272),
[recorded assent](https://github.com/Himanshu-singh04/releaselens/pull/29#issuecomment-7078440901),
[B1c independent review](https://github.com/Himanshu-singh04/releaselens/pull/29#issuecomment-7078383985).
Founder said “ok proceed”; this dispatch is preparation only. Coordinator exact-revision
code/oracle review and release must precede execution under that existing assent.
No self-release; a changed scope/trust/artifact needs a new concrete decision.

Approved base `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`;
preserved B1c `c47d0bb716ad2ad4762dbe0fabcd1520badd9a97`.
Successful start **11:27:42.902752 UTC**, first-session deadline **13:27:42.902752 UTC**.
Four worker hours/two sessions total; preparation and corrections count, review waiting does
not. At least two hours reserved for the later session. Final elapsed/remaining clock in PR.

Before switching, all B1a/B1b/R1/B1c manifest entries (63/13/7/1,773) verified on disk;
manifest hashes unchanged. After switching, B1c's two tracked-file entries are checked using
exact #29 Git blobs; cache/raw entries remain direct disk checks. No old manifest rewritten.
Fresh paths: `/Volumes/AIWorkspace/caches/releaselens/b1d-offline-validation/` and ignored
`artifacts/b1d/`; absent before start, >2 GiB free. No prior data deletion.

Prepared one research harness/oracle pair and necessary offline bootstrap/runner under
`experiments/b1d/` and `fixtures/b1d/`: <=96 new named checks plus 105 unchanged B0b controls;
two later complete executions maximum, 30 seconds/check, <=25 MiB+1 raw bytes/input,
bounded output/process handling and <=2 GiB new allocation. Independent retained sources
define expectations. Coverage, identity/bootstrap and exact commands follow below; none ran.

No archive Python, venv/pip/target import, new experiment on any runtime, local legacy experiment,
target CI, local download, admin/system/PATH/service/trust change, product code or B1 encoding
authorized here. Unchanged existing baseline CI runs historical controls and pinned downloads.
Hash/TLS and ad-hoc trust is accepted only for later released local synthetic research;
incomplete native inventory remains disclosed. B1a-I1 and product/privacy/storage/deadline
gates remain open. A1 preservation verified; A2–A4 prepared but execution-unverified;
A5 preparation gate active; A6 final delivery/check evidence in PR. No empirical qualification claim.

## B1d-P1 correction and continuation

The initial dispatch conflicted with required unchanged CI: three automatic runs executed
105 historical controls on runner Python 3.14.4 (45017484210, 45017509454, 45017522093).
The second was cancelled after controls; the third failed final PR attribution after Sourcery
appended its summary. These remain literal-dispatch deviations, not target qualification or
target two-run budget usage. Worker discovered the workflow behavior after pushing and stopped;
the workflow should have been inspected first. No local/target experiment occurred.

[Controlling clarification](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7078516832)
and [fixed-issue addendum](https://github.com/Himanshu-singh04/releaselens/issues/30#issuecomment-7078518274)
permit only unchanged existing baseline CI automatically triggered by normal delivery, including
its pinned wheel/tool downloads. No workflow/base-file edits, manual research reruns or target
release. Stopped commit/evidence preserved; stopped manifest SHA-256
`d7187641b47337da594b7501bcd40ddda1e1975d77ba6281f14324d512b91e0f` and nine entries unchanged.
New records use `artifacts/b1d/continuation/`.

Original charge including posting: **209.989248 seconds**. Resume same first session at
**11:34:31.574819 UTC**, remaining **6990.010752 seconds**, absolute preparation deadline
**13:31:01.585571 UTC**. Original total remainder at resumption **14190.010752 seconds**.
Coordinator waiting excluded; no reset. Final elapsed/remaining record will include delivery.

## Fixed oracle and coverage

One [oracle](../../fixtures/b1d/oracle.json), one [harness](../../experiments/b1d/harness.py),
necessary [bootstrap](../../experiments/b1d/bootstrap.py) and host [runner](../../experiments/b1d/runner.py).
The [one-entry requirement](../../fixtures/b1d/requirements.txt) identifies the sole runtime package.
All are research additions, outside product modules and CI discovery. No B1 cases encoded.

The oracle pins eight retained source files by SHA-256: accepted decision 006, contract,
testing, SDD, B1 source/expectation documents, and original B0b corpus/adapter. Named locators
identify adopted N1–N4 and Diagnostic clauses. The already independently reviewed B0b RFC
transcription retains all Appendix B bit-pattern/literal rows and §3.2.4 published output hex;
it is independent source evidence, not output generated from this candidate. No RFC retrieval
or candidate-output golden generation occurred. Expected hashes derive from those fixed literal
bytes/recipes using SHA-256, not independent cryptographic test vectors.

Exactly **96 new uniquely named checks**, each selected in a fresh child process:

| Group | Count | Independently specified assertions |
| --- | ---: | --- |
| RFC-B01–B26 | 26 | Exact Appendix B bits → literal bytes; NaN/infinity require canonicalization errors. Direct JCS domain, deliberately distinct from ReleaseLens N1. |
| JCS-* | 6 | Published §3.2.4 hex; UTF-16 sorting; recursive objects with preserved array order; control/quote/slash escaping; composed/decomposed Unicode unchanged; sample's 1e30 rejected through N1. |
| JSON-* | 14 | Nested escaped and astral duplicate keys; three invalid UTF-8 forms; lone value/key surrogates; BOM; NaN/±Infinity; malformed hostile value, trailing data, overflow. |
| N1-* | 10 | Both safe endpoints; signed unsafe integer, exact exponent, large integral exponent and fractional rounded-unsafe cases. |
| N2-* | 6 | 1, 1.0, 1e0, 1.0000000000000001, true, 1.5: exact root/nested types, bytes/hash, pre/post reparse, required Scalar/integer gates, observed actual compatibility. Numeric-looking text remains text; null remains null. |
| N3-* | 6 | ±underflow rejects; ±subnormal stays nonzero; signed/exponent exact zero becomes int 0 and canonical 0. |
| N4 raw | 8 | Suite 5 MiB/bundle 25 MiB at/over including whitespace and UTF-8; artifact 1 MiB at/over for escaped text and separately internal JSON whitespace. Re-encoding cannot evade raw rejection. |
| N4 aggregates | 10 | At/over 20 MiB in each of five independent arrays: authoritative, baseline/candidate and each embedded suite. Both text UTF-8 and JSON JCS accounting; raw token <=1 MiB. Component and containing byte limits reported separately. |
| N4 depth | 4 | Array/object depth 32/33; escaped quotes/braces in leaf strings ignored. Root primitive depth zero also covered by numeric controls. |
| N4 spans | 3 | Literal é: raw 4/text 2/JCS 4; escaped é: raw 8/text 2/JCS 4; internal-whitespace/escaped-quote array: raw 14/JCS 10. Original offsets exclude surrounding whitespace. |
| N4 independent arrays | 1 | Five separate 6 MiB array components with reused IDs; no cross-array sum/deduplication. Suite/embedded envelope still exceeds 5 MiB; bundle raw envelope fits 25 MiB. |
| Diagnostic injections | 2 | Fixed E_SCHEMA for ValueError at known candidate root; E_INTERNAL for RuntimeError with null location; injected canary/path/exception text cannot appear in a passing diagnostic. |
| **Total** | **96** | No omitted required group or implicit extra corpus. |

Each named row can assert several properties of its fixed input (e.g. type, value, bytes and
reparse); it is not fuzzing or a data-dependent test expansion. Boundary recipes are generated
only in that row's future child, never eagerly across the corpus. The five-array independence
row processes one array at a time. Synthetic accounting envelopes are not valid Suite/Bundle
schemas. At 20 MiB a component can pass while a suite envelope fails; embedded cases additionally
check the minimally wrapped containing bundle's raw limit. No schema/reference/count/evaluator
or 60-second product-deadline qualification follows. Wrong observed actual type is recorded as
incompatible with integer one, not an implemented TYPE_MISMATCH outcome.

The fixed research diagnostic allowlist is in the oracle: E_SCHEMA “Invalid research input.”,
E_LIMIT “Research input limit exceeded.”, E_INTERNAL “Internal research failure.” Locations are
known suite/candidate roots, known required-field pointers, or null. Parse/numeric/raw-limit
rejections compare the entire diagnostic and require zero serializer calls. Aggregate JSON
accounting necessarily calls the serializer before its decoded-total decision. Exceptions are
never copied into these diagnostics. This does not establish a shipped Diagnostic/CLI.

## Historical controls remain separate and unchanged

Original source revision `af36427eccaab43fb49a6abb13ce738d57ef2493`:

- `research/b0b/experiment.py`: SHA-256
  `70872703b65a6ccdfb330b74e0cd7dafbde7aa4a69508e219abd4b9970cfa581`.
- `fixtures/b0b/vectors.json`: SHA-256
  `cec1d004789a52cf49cccb451d4c88b004e4f036eade9bf1cac67f3e4c87ea3f`.

Both current files were statically compared byte-for-byte to that Git revision. The oracle
lists all **105** original IDs/groups: 48 P rows, 26 B rows, two sample rows, nine raw bounds,
six depths, two UTF-8 lengths, six default-runtime controls, exact-type, three hash relations
and two injected diagnostics. Original lexical-N2 P37/P38 still reject float/exponent Scalar.

Future `harness.py legacy` loads that unchanged module and calls its unchanged `main()`.
It does not call the legacy acquisition/bootstrap helper. A profile observer reports each
original `record` return (same pass/observed/details), aborting immediately on false. Original
full report goes to bounded stderr; parent verifies its rows equal the observed rows and its
inventory is exactly 105. The observer does not replace parsing, N2, fixtures or expected values.
Parent timers cover intervals between records, including generation/startup before each record;
first interval includes interpreter startup, final report gets another bounded completion interval.
Per-row elapsed/timeout is retained; exit status is explicitly the shared legacy-process status.
This is instrumentation of historical controls, not a reinterpretation or fresh historical claim.

## Exact artifacts, startup and bootstrap boundary

Only B1c's manifest-bound tree is eligible. Archive SHA-256
`42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666`, 27,109,898 bytes.
Let these fixed absolute paths abbreviate the command table below:

| Symbol | Exact path |
| --- | --- |
| T | `/Volumes/AIWorkspace/caches/releaselens/b1c-standalone-inspection/extracted/python/bin/python3.14` |
| V | `/Volumes/AIWorkspace/caches/releaselens/b1d-offline-validation/venv` |
| P | `/Volumes/AIWorkspace/caches/releaselens/b1d-offline-validation/venv/bin/python` |
| B | `/Volumes/AIWorkspace/projects/releaselens/experiments/b1d/bootstrap.py` |
| H | `/Volumes/AIWorkspace/projects/releaselens/experiments/b1d/harness.py` |

T is 19,580,280 bytes, SHA-256
`89becc2608603543736d7f0cf890f3edc52928e488fa5a54fddc96a30abb9054`.
Pip tooling is only B1c tree `lib/python3.14/ensurepip/_bundled/pip-26.3-py3-none-any.whl`,
1,950,951 bytes, SHA-256 `f3b60b20ffaadd4415ed7957212a38ac63fa4c5fa375bd0f4a797777940fad13`.
Runtime wheel is only `/Volumes/AIWorkspace/caches/releaselens/b1a-runtime/rfc8785-0.1.4-py3-none-any.whl`,
9,240 bytes, SHA-256 `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
ZIP members/metadata/license/source inspected as data: seven files, no .pth/entry point/.data
script/native object, no mandatory dependency; only unselected extras. rfc8785 source imports
math/re/typing/io and defines serializer functions/classes; no top-level acquisition or install hook.

| Order | Exact argument array after substituting fixed paths above |
| --- | --- |
| 1 | `[T, "-I", "-B", B, "base"]` |
| 2 | `[T, "-I", "-B", "-m", "venv", "--without-pip", "--copies", V]` |
| 3 | `[P, "-I", "-B", B, "empty"]` |
| 4 | `[P, "-I", "-B", B, "install"]` |
| 5 | `[P, "-I", "-B", B, "installed"]` |
| Each later suite | `[P, "-I", "-B", B, "installed"]`, then `[P, "-I", "-B", H, ID]` for each of the fixed 96 IDs, then `[P, "-I", "-B", H, "legacy"]`, then installed identity again |

Base identity requires CPython 3.14.10, native arm64/64-bit, GIL enabled/config disabled=0,
JIT disabled, exact executable/base/prefix, isolated/no-bytecode/no-user-site flags, no custom
startup modules, only private sys.path roots and expected installed pip 26.3 metadata. Explicit
needed imports are decimal/_decimal/json/math/struct/hashlib/zipfile/runpy/importlib.metadata/
venv/typing/re/io/contextlib; origins must be built-in/frozen or under the retained tree. All
loaded filesystem-backed modules must be in allowed roots (except the reviewed script).
No GUI/Tcl/optional sweep. Parent first checks tree inventory as well as every manifest entry,
rejecting added files/symlinks including startup hooks before any invocation.

Venv is fresh, copied, without pip/system packages. Stdlib venv creates only its task-local
configuration, interpreter copies, directories and activation scripts/SCM ignore file; activation
scripts are never invoked. Its inspected source guards ensurepip behind with_pip, false here;
no upgrade/upgrade-deps/backend. Empty identity repeats the runtime checks, requires zero
distributions and excludes base site-packages. Missing/incompatible copies stop, without repair.

Install adapter rechecks the empty identity and both wheel bytes/hashes, puts only the pinned
pip wheel first on this process's sys.path, verifies its import origin, then uses runpy on pip.
Exact pip argv: `pip --isolated --disable-pip-version-check --no-input install --no-index
--no-deps --require-hashes --no-cache-dir --no-compile --only-binary=:all: -r` followed by
`/Volumes/AIWorkspace/projects/releaselens/fixtures/b1d/requirements.txt`.
The sole requirement is a direct local file URI/hash: no index/find-links search, ensurepip,
pip installation/upgrade, extras, compiler or source build. Pip and vendored tooling execute
only in this released step. Retained pip source explicitly skips all config files when
PIP_CONFIG_FILE is `/dev/null`, including under --isolated; inspected __main__ invokes its CLI.
Pip may load its bundled vendor/stdlib modules; no malicious-code-absence claim is made.

Installed identity requires exactly rfc8785 0.1.4 and venv import origin. Before importing it,
compare every installed wheel member except pip-rewritten RECORD to the retained wheel; allow
only INSTALLER/REQUESTED/direct_url metadata additions, no .pth/bytecode/extra package/symlink.
Recheck after each suite. All target behavior, inventory and OS execution acceptance are unknown
until the released sequence runs; static declarations do not satisfy these prerequisites.

## Parent bounds, record and release protocol

Parent is existing `/Library/Frameworks/Python.framework/Versions/3.13/bin/python3` with `-I -B`.
It imports only host stdlib. Child cwd is the fixed B1d cache root; stdin is /dev/null. Rebuilt
environment contains only PATH=`os.defpath` (child-only native search path), HOME=`task/home`,
TMP/TEMP/TMPDIR=`task/tmp`, XDG_CONFIG_HOME=`task/config`, XDG_CACHE_HOME=`task/cache`,
PIP_CONFIG_FILE=/dev/null, PIP_DISABLE_PIP_VERSION_CHECK=1, PYTHONDONTWRITEBYTECODE=1, LC_ALL=C.
No credentials/proxy/PYTHONPATH/JIT settings are inherited. No shell or global PATH edit.

Selectors drain both pipes while bounding each to **262,144 bytes/process**. Each new check,
prerequisite and legacy record interval has **30 seconds**; timeout, excessive output, nonzero
exit, malformed/missing/false result or changed inventory stops. Process groups receive TERM,
then KILL, with bounded wait/reaping; exact argv/environment/exit/elapsed/termination and partial
output retained. A failed legacy row is reported before stopping; no unseen later row is passed.
Inputs are <=26,214,401 bytes; one boundary recipe at a time. Large bytes are recorded by length/
SHA-256 and small outputs also by literal hex; expected bytes come from reviewed source/recipes.
No unbounded communicate/capture of target output or eager corpus expansion.

Parent checks new task allocation (including stopped B1d evidence), retaining 32 MiB headroom
under 2 GiB, before/during/after children, and checks free space. This is sampled accounting of
a finite recipe, not an OS storage quota, memory qualification or sandbox. Isolation flags do
not prove arbitrary code cannot cause side effects. No intentional target network operation;
observed unexpected network/write/startup/package effects remain mandatory stop conditions.
All B1a/B1b/R1/B1c/stopped-B1d manifests are checked before and after each phase (also on failure),
with #29 tracked entries verified as Git blobs. Source hashes/clean checkout rechecked afterward.

There is **no release record now**. Coordinator must first review this exact commit, source/
oracle hashes, bootstrap and command plan, then issue a separate release comment under existing
assent. Coordinator-provided `artifacts/b1d/continuation/release.json` must contain issue=30,
exact head, that comment URL, exact SHA-256 map of every packet file and the remaining second-
session worker seconds (<=7200). The runner checks binding; it cannot authenticate who authored
the record. Worker may not manufacture it or self-release. A changed head needs fresh review.

Only after that release, three separate host commands in the one remaining execution session:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py bootstrap REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1d/continuation/release.json
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py run1 REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1d/continuation/release.json
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py run2 REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1d/continuation/release.json
```

These commands are a review plan, not instructions to run during preparation. Each stage must
succeed before the next; no automatic confirmation or retry. Fresh exclusive phase directory
consumes its slot even on interruption; STOP latch blocks subsequent stages on failure. One
execution-session deadline persists across commands. Run2 requires identical revision/oracle/
release record and exact expected/actual result equality with run1, excluding timing metadata.
There is no run3. Preserve partial failures; changed oracle, trust, artifact or scope cannot
be used to turn a failed qualification into a pass. Existing baseline delivery CI is separate.

## Preparation verification and handoff

Host AST parsing and manifest JSON/uniqueness/source-hash inspection are static only. No new
module was imported or called, raw input parsed as a control, numeric/JCS experiment executed,
boundary expanded, target invoked or local historical suite run. During source inspection,
an escaped-key fixture spelling and small token-length arithmetic were corrected before review;
no candidate output informed either expectation. All eight source hashes match. Required
repository checks and exact-head CI/attribution outcomes are in the PR, including prior failures.

A1 preservation/source trace prepared and statically verified; A2 fixed 96+105 inventory and
oracle prepared, independent approval pending; A3 exact prerequisites/bootstrap prepared,
actual identity/import/isolation unknown; A4 bounded parent/evidence prepared, behavior untested;
A5 mandatory preparation checkpoint only, no release; A6 checks, clocks and delivery recorded
in PR. **No A1–A6 execution completion or runtime qualification is claimed.** Stop for independent
code/oracle/command review. B1d-P1 fixing revision is supplied for coordinator verification,
not self-resolution. No approval, merge, product adoption or automatic continuation.
