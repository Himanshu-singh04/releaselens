# B1f: confirmation-only preparation

Status: **prepared for independent review; no B1f target use or execution release**.
2026-11-22; original GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode worker, $0 new spend.

## Authority and narrow scope

[Issue33](https://github.com/Himanshu-singh04/releaselens/issues/33),
[full briefing](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079953974),
[founder assent](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7080060030)
and [B1e review / B1e-R1](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7079952341)
control this preparation. Founder approved confirmation-only work and, for B1f only, built-in
same-provider connection recovery. Coordinator must independently review and release the exact
revision before target use. Continue draft31 from `beee491d61799e3bd756322fa0dfb503680e7eea`;
approved main remains `c2d56ef6ec90ba5121cf9d486cd3e0b382a9c22f`.

B1e's five prerequisites and first96+105 checks were independently verified. Both B1e sessions
and their deadlines remain closed. This prepares one confirmation of that initial outcome,
using the retained verified venv, without bootstrap, reinstall, relocation or old deadline reset.

## B1e-R1 additive correction

The B1e worker handoff omitted an observed provider-recovery event. The coordinator's serialized
history review identifies assistant **msg_2036e425d001VGNDKF9Isfsa8X**, created
**13:24:47.333 UTC**, completed **13:25:01.482 UTC**, with **provider.transport: WebSocket
closed with code1012**, finish=error, retry metadata **attempt2**, scheduled13:25:03.564 UTC.
Synthetic continuation **msg_2036e81ce00107Bbkn5P47628m** followed at **13:25:03.566 UTC**.
This occurred after successful run1 and before the host display `KeyError:'hex'`. **No target
command ran afterward.** The old handoff's reporting-only explanation was incomplete.

This is observed harness-managed recovery, not proof of a manually chosen alternate provider
or paid fallback. It nevertheless conflicted with B1e's strict stop/no-provider-retry instruction.
B1f permission does **not** retroactively authorize it. Original comments, Decision011 and all
sealed evidence remain unchanged. This note and the new PR response supply the correction;
only the coordinator may verify and resolve B1e-R1.

The named retained event file is
`portfolio/reviews/releaselens-pr31-b1e-provider-event.json`. The worker's direct read was denied
by the external-directory tool boundary; it was not retried through another file-access route.
The event details above are attributed to the complete published coordinator review. Current
B1f history is audited separately through the authenticated existing OpenCode session API.

## Minimal adapter and immutable inputs

New [confirm.py](../../experiments/b1f/confirm.py) imports the hash-bound reviewed runner as a
host module and calls its existing `run()` implementation. It never calls the old `main()`;
there is no bootstrap branch or old session/release write. Child process management, sanitized
environment, stdin/pipes, legacy observer validation,30-second limits,262144-byte stream caps,
TERM/KILL and bounded waits remain the reviewed implementation.

The adapter performs installed identity → identical96 new checks → identical105 legacy controls
→ installed identity. Both identities must equal retained B1e run1 identity. Complete semantic
outcome dictionaries must equal retained run1, not merely pass counts. `comparison.json` retains
both outcomes and equality even if the comparison fails. No optional descriptor display or
assumption that every RFC row has `actual.hex`; JCS-utf16 uses `actual.bytes.hex`.

Only this document and `experiments/b1f/` are new source. Runner/bootstrap/harness/oracle/
requirement/legacy/host regressions and Decisions010/011 remain byte-identical. The release map
pins ten inherited paths and three new files; inherited hashes must also match baseline Git
blobs. Oracle's eight independent source hashes are rechecked.

Retained target:
`/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python`.
Initial outcome: `artifacts/b1e/execution/run1/success.json`, SHA256
**`ce8889f3aae3142c4eb9cb988e66a1495de99c465b8521d495b4499fa3ae654e`**.
B1e results manifest: **`ef2e3a62d9bfa482e1a35f5a376476afe3e7b73e307614307bbb05cae6e408b8`**,
372 entries, including all20 retained cache files. B1e release remains
**`39a82773727f6824ba3f3bb93453af68006f7a747dee0a2422f4a2fc5de388e6`**.

Before preparation reuse, all nine manifests and **63+13+7+1773+9+16+54+42+372 entries**
verified, with raw/cache files directly rehashed. Explicit tracked-file revision mappings remain:
B1c c47d0bb, B1d continuation6d758d1, B1d session2 41f7e1d, B1e preparation e83b191, B1e results
beee491. No raw-data fallback to Git. All33 approved-base files/55 SDD headings/15 prior refs
verified. Before and after future confirmation, all nine manifests and sealed B1f preparation
entries are rechecked. The retained cache's file/symlink inventory must match the results manifest
exactly, rejecting extra startup hooks before target use. Unexpected input changes stop;
successful counts never override integrity.

## Fresh roots, accounting and exclusive attempt

New evidence/release root: `/Volumes/AIWorkspace/projects/releaselens/artifacts/b1f/`.
New optional scratch: `/Volumes/AIWorkspace/caches/releaselens/b1f-confirmation/`.
Both were absent at start; unexpected preexisting roots were rejected. Synthetic test fixtures
are retained in owned scratch, with their outcomes sealed; no old cache/evidence cleanup.
Future `artifacts/b1f/execution/` is created exclusively. Its presence consumes the only attempt,
including failure/interruption. Target/identity/mismatch errors record STOP; no retry path.

The original runner capacity function still checks retained B1e task/evidence against2GiB with
32MiB reserve. A separate instance of the same unchanged runner allocation code checks B1f
evidence+scratch against **256MiB**, also retaining32MiB reserve and checking free space.
The wrapper additionally enforces combined retained+new allocation+reserve below2GiB, and is
called by the existing `run()` capacity seam. Child cwd/environment still use B1e, never the
budget instance's roots. All output directories are covered. This remains sampled accounting,
not an OS quota, adversarial filesystem isolation or native customer-storage qualification.
Original <=25MiB+1 raw input and one boundary recipe at a time remain unchanged.

## Host-only proof and release shape

Approved host command, cwd `/Volumes/AIWorkspace/projects/releaselens`:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B experiments/b1f/test_confirm.py
```

Tests use actual retained record shapes with mocked dispatch and a Popen guard that rejects
any subprocess. Initial seven tests passed in0.107s; nine-test checkpoint passed in0.161s.
Final ten tests cover identical full
outcome/exact99 command arrays; same-pass-count semantic mismatch; before/after identity
mismatch; immediate failed-row stop; exclusive failure slot/STOP/no retry; retained/new/combined
allocation limits and missing new root; changed sealed preparation evidence; wrong release map;
and an added retained-cache file (synthetic .pth, never loaded).
They execute no acquired interpreter, bootstrap, pip, candidate/numeric/JCS or local legacy
experiment. Final evidence, repository checks, attribution and current-body CI are in the PR.

No B1f release exists during preparation. Coordinator must create `artifacts/b1f/release.json`
only after independent exact-code/hash/command review. Required shape:

```json
{
  "issue": 33,
  "head": "EXACT_REVIEWED_COMMIT",
  "authorization": "https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-COORDINATOR_RELEASE",
  "remaining_worker_seconds": 1800,
  "reference_sha256": "ce8889f3aae3142c4eb9cb988e66a1495de99c465b8521d495b4499fa3ae654e",
  "preparation_manifest_sha256": "SEALED_B1f_PREPARATION_MANIFEST_SHA256",
  "files": {"ALL_13_PACKET_PATHS": "REVIEWED_SHA256"}
}
```

Illustrative1800 seconds is not a reset; release ceiling must not exceed actual remaining B1f
time or3600. Second-session worker deadline includes preflight/reporting/delivery independently.
Release authorship remains a coordinator procedure, not authentication supplied by JSON.
Only after release, exactly one command from required checkout:

```text
/Library/Frameworks/Python.framework/Versions/3.13/bin/python3 -I -B /Volumes/AIWorkspace/projects/releaselens/experiments/b1f/confirm.py REVIEWED_HEAD /Volumes/AIWorkspace/projects/releaselens/artifacts/b1f/release.json
```

Prepared ignored packet expands every child argument and environment and proves equality to
B1e run1's reviewed99 command arrays. It is not an execution release. One confirmation only;
any target error/mismatch/timeout/changed input/uncertain effect stops without repair/retry.
Optional post-success reporting failure must be retained separately, never trigger target rerun.

## Recovery, clocks and disposition

For B1f only, built-in same-provider connection-interruption recovery is permitted, including
native reconnect/transport fallback. No manual retry loop, model/provider/account switch, paid
fallback or quota/rate/auth bypass. Observed quota/rate/auth/billing errors stop. No configuration
change or service start/restart. Managed service status reported stopped; an existing authenticated
server at127.0.0.1:4097 was located and read explicitly, without starting the managed service.
Serialized message/error/retry/synthetic metadata is audited at handoff; reasoning/native and
credential content are excluded from retained audit records. Any coverage cutoff is explicit;
successful task outcome is not evidence of an error-free transport history.

Clock began **13:47:57.643980 UTC**, before first authority/task read. Preparation deadline
**14:17:57.643980 UTC**. At most two sessions/**3600 worker seconds total**, preparation<=1800,
leaving>=1800. All reads/checks/corrections/reporting/delivery charged; coordinator waiting excluded,
no reset. Final conservative charge/remainder and allocation are retained at handoff. Old B1d/B1e
clocks remain historical/closed.

A1 preservation/reuse input verified; A2 minimal confirmation adapter prepared; A3 actual-record
shape/equality proof and exact identity/commands prepared, target confirmation unperformed;
A4 independent review gate active; A5 B1e-R1 correction and serialized-history audit supplied;
A6 checks/attribution/CI/evidence/budget at handoff. Stop for independent review, no self-release.
No acquisition/spend, system/admin/PATH/service/trust/quarantine/sysconfig/link change, package/
compiler, customer/product/native-storage work, approval/merge/adoption or next-task dispatch.
Hash/TLS/ad-hoc synthetic-research trust and incomplete native inventory remain; all privacy/
storage/product/60-second-demo gates remain. Confirmation success would answer only this finite
research question, not ship an MVP or approve customer use.
