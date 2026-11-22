# B1e: transient-file accounting repair and preparation

Status: **bootstrap and run1 passed; stopped during host reporting before confirmation**.

## Second/final-session result (2026-11-22)

[Independent preparation verification / B1d-R1 resolution](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079739529)
and [controlling execution release](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079740993)
authorized exact execution head **`e83b191771eac3fc6b1825bff2268f1c4f78b4cb`**. The coordinator's
`artifacts/b1e/release.json` matched issue32, head, published eight-file map, authorization URL
and 3600-second ceiling; SHA-256
**`39a82773727f6824ba3f3bb93453af68006f7a747dee0a2422f4a2fc5de388e6`**.
It was neither regenerated nor edited. All eight files remained unchanged through execution.
Only this results note changes afterward; executable/test/harness/oracle/requirement and
historical Decision010 bytes remain identical to the executed revision.

Second session began **13:21:34.808013 UTC**, prior conservative B1e charge **875.702482s**,
original remainder **6324.297518s**, absolute worker deadline **15:06:59.105531 UTC**.
Runner sequence began **13:22:26.196209 UTC**, separate persistent deadline
**14:22:26.196209 UTC**. No clock reset. Reporting and delivery count; final conservative
charged total/remainder is retained in `artifacts/b1e/session2/final-clock.json` and the PR.

Preflight verified clean released head, explicit host Python3.13.4, all eight hashes, old
manifests and **63+13+7+1773+9+16+54+42 entries**, exact retained-tree inventory, 33 main files,
55 SDD headings and 15 prior refs. B1e cache was empty, execution directory absent, with
**120,934,379,520 bytes available**. Old B1d cache/STOP/release remained preserved.

Exactly two released host commands were invoked separately, from the required checkout:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py bootstrap e83b191771eac3fc6b1825bff2268f1c4f78b4cb /Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/release.json
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py run1 e83b191771eac3fc6b1825bff2268f1c4f78b4cb /Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/release.json
```

Both host commands exited **0**. Bootstrap's five child exits were **0**, with no stderr,
timeout, parent error or termination signal:

| Prerequisite | Observed result | Seconds |
| --- | --- | ---: |
| Base identity | Passed; retained private base, pip26.3 distribution inventory | 0.258727 |
| Copied --without-pip venv | Passed; fresh B1e venv | 2.078503 |
| Empty venv identity | Passed; empty distribution inventory, no base site-packages | 1.037048 |
| Pinned offline wheel install | Passed; exact pip wheel identified, rfc8785 install reported | 1.238399 |
| Installed verification | Passed payload comparison, allowed files, inventory and import origin | 0.262062 |

Actual identity: **CPython 3.14.10 (main, Nov 11 2026, 00:14:32) [Clang 23.1.3 ]**,
native **arm64, GIL=true, JIT=false**, expected isolated private prefixes and needed module
origins. Installed inventory was exactly **rfc8785 0.1.4**; origin was
`/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/lib/python3.14/site-packages/rfc8785/__init__.py`.
Unlike B1d, installed verification actually ran and passed. Bootstrap allocation snapshot:
**78,893,056 bytes**; old preservation checks passed and all 42 B1e preparation entries rehashed.

Only then run1 was invoked. **96/96 new checks and 105/105 unchanged legacy controls passed**.
All raw new rows matched the phase outcome; all legacy observer rows matched the original
full report and fixed ID/order inventory. All **99** suite child commands exited0 with no
timeout, parent error or termination. Installed identity before/after was identical.
Longest new check **4.469736s**; longest legacy interval **1.208612s**; whole legacy child
**3.259131s**; sum of suite child elapsed **50.062411s**. Largest stdout **21,293 bytes**;
largest stderr **24,996 bytes**, the expected unchanged legacy full report. Other stderr empty.
Allocation after run1: **79,835,136 bytes**. These are sampled/finite observations, not a quota
or product performance qualification.

The fixed RFC/JCS, rejection, N1–N4, type/reparse/hash, raw/decoded boundaries and diagnostic
rows passed their reviewed assertions. Original legacy lexical-N2 P37/P38 still reject
float/exponent Scalar; those controls were not reinterpreted. Synthetic aggregate component
and envelope outcomes remain separate; schema/native-storage/product acceptance is not implied.

### Reporting failure and stop before run2

During inspection, one read requested guessed `N2-rounded-fraction.stdout`, which is not a
fixed oracle ID, and returned file-not-found. The subsequent completed `run1-inspection.json`
verified every actual fixed ID/file, all201 pass rows, raw/outcome equality, exits, limits,
identity and preservation. No actual target record was missing.

A later **host-only display helper** reading recorded JSON exited **1** with **`KeyError: 'hex'`**:
it assumed every `source=RFC` actual descriptor contained a `hex` member. This was a worker
reporting-schema assumption, **not a target test or runner failure**. Under the release's
stop-on-any-failure rule, execution stopped before run2. The display helper was not retried;
no source/oracle/target repair or extra target command followed.

**Run2 was not invoked.** There is one successful suite, **104 target child invocations total**
(5 bootstrap + 99 run1), zero target-check failures, and **no identical-confirmation result**.
The successful runner phases created no runner STOP; worker stop is separately retained at
`artifacts/b1e/session2/reporting-STOP.json`, without fabricating a runner failure. Preserve
both successes and reporting errors. Remaining time does not authorize another session/attempt.

Execution command/environment/stdout/stderr/identity/timing/outcome records are retained under
`artifacts/b1e/execution/`; fresh inspection/preservation/check/manifest/clock records under
`artifacts/b1e/session2/`. Old Decision011 manifest entry is verified against the original
**e83b191 Git blob** after this update; every old raw/cache entry remains a direct disk check.
No old manifest, release, STOP or venv is rewritten or cleaned.

A1 preservation verified; A2/A3 independently reviewed repair/host proof retained and bootstrap/
initial suite passed; A4 immutable inputs preserved; A5 stopped on reporting failure, confirmation
**unperformed**; A6 results-only delivery/checks/attribution/CI recorded in PR for independent
result review. This is a **partial finite success with an incomplete confirmation sequence**,
not a completed two-run qualification, runtime adoption, PR approval/merge or product readiness.
No new acquisition/spend, fallback, system/trust change or customer/product/native-storage work.
B1a-I1 and all privacy/storage/product/deadline gates remain unresolved.

## Historical preparation record (execution revision above)

The following describes the prior preparation checkpoint. Claims that no B1e target ran or
release existed apply to that checkpoint; the actual results above supersede those temporal
claims without changing the reviewed executable or expectations.

2026-11-22; original GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode worker, $0 new spend.

## Authority and fixed scope

[Issue #32](https://github.com/Himanshu-singh04/releaselens/issues/32) fixes A1–A6.
Founder said “ok proceed” to the sole
[B1e briefing](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079064010),
recorded in [authorization](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079508649).
[Independent B1d result verification / B1d-R1](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079062458)
verified a correct stopping result and independently reproduced an accounting defect.

Continue draft #31 / `research/b1d-offline-validation` from reviewed results
`41f7e1d431419539faf5b1523bcd12d386cac5d6`; approved main remains
`c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`. This is a new bounded attempt, not a restart
of B1d. [Decision010](010-offline-runtime-validation.md), its execution revision
`6d758d11b164fcd22530e23003a57891dbe3b3b6`, STOP, partial venv and closed clocks remain historical.
No old records/manifests are rewritten or partial venv reused. B1d-R1 remains for coordinator
verification; this worker supplies a fixing revision and proof, not self-resolution.

Only the [runner](../../experiments/b1d/runner.py), one fresh-task path in
[bootstrap](../../experiments/b1d/bootstrap.py), [host regressions](../../experiments/b1e/test_runner.py)
and this document change. No target interpreter, bootstrap, pip, rfc8785, numeric/JCS harness
or local legacy suite is invoked during preparation. Normal unchanged baseline CI and pinned
delivery downloads remain allowed; their results are separate from target qualification.

## Reproduction and minimal repair

The exact old `allocation()` enumerated each root with `rglob('*')`, materialized the list,
then called `lstat()` on each entry. A real synthetic file deleted after enumeration but
immediately before its real `lstat()` reproduced **FileNotFoundError**. The same host test
command first ran against unchanged results-head runner: stable baseline passed, disappearing
child errored, **2 tests / 1 expected error**, exit 1. Logs are retained under
`artifacts/b1e/regression-before.*`. No target code was imported to reproduce this defect.

The repaired allocation function uses a small explicit stdlib `scandir` traversal with
`lstat()` for every entry. This avoids glob's implicit suppression of traversal errors:

- Validate both roots with `lstat`; missing, non-directory or symlink roots are fatal.
- Ignore **only ENOENT for descendant entries/directories** disappearing before stat/scan.
- Propagate permission, ENOTDIR and other I/O failures. An unreadable subtree is not empty.
- Recheck both root directory identities (`st_dev`, `st_ino`) after traversal; root loss or
  replacement is fatal, including first-root loss while the second is scanned.
- Count allocated blocks (`st_blocks * 512`) as before; do not follow listed child symlinks.
  Keep the **2 GiB** bound, **32 MiB** reserve and `statvfs` free-space checks unchanged.

This is sampled accounting, not a storage quota or adversarial filesystem sandbox. Entries
created after enumeration may be seen only by a later sample; a sampled directory subsequently
removed can be conservatively overcounted. The finite recipe and reserve remain essential.
Root identity sampling is not continuous monitoring and does not prove native-storage safety.

The host reproduction proves a runner defect, **not the exact missing path or cause in the
historical B1d execution**. That record captured only the parent exception class. Pip's success
text still does not establish installation: B1d prerequisite 5 and both suites never ran.

## Bounded parent diagnostics and host proof

Parent records now include operation, bounded exception class, errno, at most four runner-only
function/line sites, and a redacted location. Only task/evidence root labels and fixed top-level
directory names may appear; other relative names are redacted, with a 16-hex SHA-256 prefix
for correlation. Outside-task paths are not disclosed. Exception messages, source snippets,
locals and unbounded tracebacks are excluded. This is internal research evidence, not a change
to the target Diagnostic contract or oracle.

Operation labels distinguish capacity, process start/wait/signal, pipe setup/read/select/close,
legacy-record processing and deadlines. Process-start failures now produce a command record
without inventing a child exit. Existing TERM/KILL and bounded wait/reaping remain; signal/close
I/O failures fail the command and retain bounded evidence. Phase STOP also records bounded
failure and failed-preservation details. The runner CLI emits bounded JSON instead of a raw
exception traceback. Recorded child stdout/stderr retain the original per-stream cap.

Exact host-only command, cwd `/Volumes/AIWorkspace/projects/releaselens`:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B experiments/b1e/test_runner.py
```

The tests explicitly reject other interpreter paths/versions and import only the host runner,
not bootstrap/harness. Synthetic temporary directories live under the new B1e cache root;
only those owned test fixtures are removed. Host children are explicit Python3.13 `-I -B -c`
processes, restricted by the test spawn wrapper. No acquired interpreter is launched.

The final 20-test suite covers stable nested counting; real child disappearance at lstat;
directory cleanup before scandir; both missing/file/symlink roots; root loss/replacement;
EACCES/EIO/ENOTDIR at stat and traversal; no child-symlink traversal; real capacity/reserve
boundary, low free space and statvfs failure; successful host child; disappearance through the
live capacity caller; cap termination/reaping; bounded/redacted allocation-error evidence;
process-start and pipe errors; original stream cap; persistent deadline and 30-second timeout;
and a synthetic phase failure whose exclusive started slot and STOP prevent further dispatch.
The phase test uses a synthetic release and mocked dispatch, never target commands. Permission
errors are injected at actual I/O seams; this does not establish mount permission enforcement.
The timeout test advances the parent clock deterministically, rather than waiting 30 seconds.

The initial repaired 19-test suite passed in **0.205s**; the final suite adds the live-caller
disappearance regression and an explicit ENOENT guard. Final command output, exact outcomes,
repository checks, attribution and required CI are retained in the PR/evidence packet.
Host regression counts do not expand or substitute for the immutable 96+105 target checks.

## Preservation and immutable inputs

Before editing, all **63 + 13 + 7 + 1,773 + 9 + 16 + 54** manifest entries verified, along
with **33** approved-main files, **55** SDD headings and **15** prior refs. All old raw/cache
entries remain direct disk checks. For tracked research entries only, the runner resolves:

| Manifest | Original tracked-file Git revision |
| --- | --- |
| B1c, its two tracked files | `c47d0bb716ad2ad4762dbe0fabcd1520badd9a97` |
| B1d continuation, its six packet files | `6d758d11b164fcd22530e23003a57891dbe3b3b6` |
| B1d session2, its six packet files | `41f7e1d431419539faf5b1523bcd12d386cac5d6` |

These are explicit path/revision allowlists, not a fallback for changed raw data. Session2
manifest stays `2f1837fc1120cbe2b2598cccbe2a53e695ea7dc154c1a867d4374f8681e12093`.
Old release stays `846051c31aa9824d6f912a46dbe3fe778dae37c1ee4bdff7a5251b18cd0a0ab1`;
old STOP stays `e76ae4744cfb50278dd6afd178c0477cfa1f27e1d7c030edebc1f48ec694ee43`.

Byte-identical immutable inputs:

| Input | SHA-256 |
| --- | --- |
| Harness | `d75d56203fa021082bfc59e694d7585a25e208cfffcf17fa5280ea539af72673` |
| 96-check oracle | `578c4e6c9396e2ff7df142dcbc3be68e48c669fb698e7a324e1df661ae05fd32` |
| Requirement | `7bde3df9609b602441977269899e4855375e40f0bc8bccc244e8abef5d05e77e` |
| Legacy adapter | `70872703b65a6ccdfb330b74e0cd7dafbde7aa4a69508e219abd4b9970cfa581` |
| Legacy corpus | `cec1d004789a52cf49cccb451d4c88b004e4f036eade9bf1cac67f3e4c87ea3f` |
| B1c archive | `42031ed5f0d38777335252c8c77d64708c8010dd67c128246bdec25000672666` |
| Target executable | `89becc2608603543736d7f0cf890f3edc52928e488fa5a54fddc96a30abb9054` |
| Pip wheel | `f3b60b20ffaadd4415ed7957212a38ac63fa4c5fa375bd0f4a797777940fad13` |
| rfc8785 wheel | `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48` |

## Fresh command packet and review gate

New roots were absent at start; unexpected preexisting roots were rejected. Cache/scratch/venv:
`/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/`; ignored evidence:
`/Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/`. Initial available space was
**120,943,923,200 bytes**. No B1d path is reused. Before fresh bootstrap, task root must be empty,
execution directory absent, roots valid and at least 2 GiB available. Phase slots remain exclusive.

There is **no B1e execution release during preparation**. Coordinator must independently review
the fixing revision, eight-file packet hashes, oracle preservation, host proof and commands.
Only the coordinator may create `artifacts/b1e/release.json`, shaped as:

```json
{
  "issue": 32,
  "head": "EXACT_REVIEWED_40_HEX_COMMIT",
  "authorization": "https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-COORDINATOR_RELEASE",
  "remaining_worker_seconds": 3600,
  "files": {"EVERY_PACKET_PATH": "EXACT_REVIEWED_SHA256"}
}
```

The example seconds are illustrative, not a new budget: the coordinator sets a positive ceiling
no greater than actual remaining B1e time (and <=7200). The worker's second-session deadline also
charges preflight/reporting/delivery. The runner persists its separate deadline from bootstrap
without resetting on run1/run2. Release authorship is procedural, not authenticated by JSON.
The packet contains the old six packet paths plus this document and the host regression file.

After release only, invoke these **separately** from the checkout, substituting the reviewed SHA:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py bootstrap REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/release.json
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py run1 REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/release.json
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1d/runner.py run2 REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1e/release.json
```

Exact child arrays remain Decision010's table with **only V and P substituted**:
V=`/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv`, P=`V/bin/python`.
T remains retained B1c `python/bin/python3.14`; B/H remain checkout `experiments/b1d/bootstrap.py`
and `harness.py`. Base identity → copied `--without-pip` venv → empty identity → offline pinned
wheel install → installed verification. Each suite verifies identity before/after, runs the
fixed 96 new checks and unchanged 105 controls, with identical outcome confirmation on run2.
The prepared ignored command packet expands all paths/arrays for review; it is not a release.

Same isolated/no-bytecode flags, sanitized task-local child environment, no-index/no-deps/
require-hashes/no-cache/no-compile install, and no extra package/compiler. Preserve 30 seconds
per prerequisite/check, 262144 bytes per stream/process and <=25 MiB+1 raw input. Any bootstrap
or target failure stops the new attempt; no retry, repair, run3, fallback or oracle correction.

## Clock and disposition

New B1e preparation session started **13:02:28.545665 UTC**; absolute first-session deadline
**14:02:28.545665 UTC**. At most two sessions / **7200 worker seconds total**, preparation <=3600,
leaving at least 3600 for execution. All corrections/checks/reporting/delivery count; coordinator
waiting is excluded. No reset. Final charged elapsed/remainder and allocation are in the PR and
fresh evidence. B1d's closed clock is unchanged and provides no B1e time authority.

A1 preservation verified; A2 defect reproduced and narrowly repaired; A3 host-only regressions
and bounded parent evidence supplied; A4 immutable inputs and fresh command packet prepared;
A5 stop for independent exact-revision review, no self-release; A6 checks/attribution/CI/clock
recorded at handoff. These are preparation claims, **not runtime/JCS/N1–N4 qualification**.
No new acquisition/spend, admin/system/PATH/service/trust/quarantine/sysconfig/link changes,
provider fallback, product/customer/native-storage work, runtime adoption, approval or merge.
Existing hash/TLS/ad-hoc research trust and incomplete native dependency/license inventory remain;
B1a-I1 and all product/privacy/storage/deadline gates remain unresolved.
