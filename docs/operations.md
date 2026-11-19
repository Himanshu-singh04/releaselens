# Local operations and recovery

Product operations remain a plan; no application, package, or model integration exists.
The persistent development worker is provisioned and verified in [issue #9](https://github.com/Himanshu-singh04/releaselens/issues/9).
[Development](development.md) governs delivery
approval; [roadmap](roadmap.md) gates implementation; [testing](testing.md) defines verification.

## Storage and execution: current reality

| Item | Current location / state | Meaning |
| --- | --- | --- |
| Source and these documents | `/Volumes/AIWorkspace/projects/releaselens` | Pendrive checkout; all task artifacts remain here. |
| CPU and RAM | Existing Mac; observed 16 GiB RAM / 8 logical CPUs | Processes use Mac compute, not pendrive memory; not a benchmark. |
| Coordinator session history | `/Users/himanshusingh/.local/share/opencode/opencode.db` | Separate Mac service, unchanged by worker provisioning. |
| Worker history and OpenAI OAuth | `/Volumes/AIWorkspace/portfolio/runtime/data/opencode/projects.db` | Founder explicitly chose pendrive database with credentials/history together; outside Git, filesystem confidentiality unverified. |
| App private key and owner `gh` authentication | Mac, outside repository | Never copied into product evidence, checkout, or CI. |
| Worker caches/state | `/Volumes/AIWorkspace/caches/project-opencode/` and `/Volumes/AIWorkspace/portfolio/runtime/state/` | Development-service routing; not a product model installation. |
| Product model/cache directories | No product routing/model configured | Future downloads still need explicit decisions and effective-path verification. |
| Dedicated project service/worker | OpenCode 2.2.7, authenticated localhost service; reusable ReleaseLens session | Effective DB handles, routing, and continuity after graceful restart verified by coordinator in #9. |
| GitHub | Remote copies of pushed tracked commits only | Uncommitted/unpushed drafts and ignored local data are not backed up there. |

Public [provisioning evidence and operations snapshot](https://github.com/Himanshu-singh04/releaselens/issues/9#issuecomment-6999734870)
record lifecycle/recovery procedures; the local guide is
`/Volumes/AIWorkspace/portfolio/documentation/project-workers.md`. The founder authorized
worker OAuth on the pendrive. Worker inference consumes the existing ChatGPT subscription
allowance, with no new paid service/API fallback; this is development assistance, not the
future product's local inference. Processes share one macOS user, not a credential sandbox.
Authenticated localhost API access and outside-Git storage do not establish filesystem
confidentiality. Other-account access to the worker database has not been tested; ownership-based
privacy cannot be assumed on the observed unencrypted `noowners` mount. No credential read
or exposure by another account has been demonstrated. Encryption at rest alone would not
establish access control while mounted. The founder's storage choice remains unchanged.
Graceful restart was verified; reboot, unplug/power-loss, and full restore were not.
Do not copy/edit a live database; SQLite backups also contain credentials. No
service, database, credential, or ownership change is part of B0.

## Proposed local runtime and packaging

The [B0 recommendation](decisions/001-runtime.md) conditionally prefers CPython 3.14.10
over TypeScript/Node 26.13.1, with an untested JCS dependency candidate and required Darwin
native bridge. Exact build/installer pins and compatibility remain blocked, not approved.
Proposed first target is the observed arm64 Mac with owner-enabled local APFS; other
platforms require separate evidence. No Windows/Linux product support is promised.
Future package must include built code, contract/version metadata, license inventory, and
reviewed synthetic examples, plus reproducible lockfile/build provenance and checksums.
No customer evidence, credentials, model weights, caches, or session history in releases.
Install/build/product commands do not exist; only [CONTRIBUTING](../CONTRIBUTING.md) commands
are currently executable project instructions. No installer or automatic updater is implied.

Earlier evidence/output placement suggestions under ignored local-data/ and artifacts/
in this checkout are **blocked on this mount**: B0's read-only `diskutil info -plist
/Volumes/AIWorkspace` reported `GlobalPermissionsEnabled=false`, and `mount` confirmed
APFS `noowners` on 2026-11-19. Product I/O must refuse this destination under the existing
private-access requirements. No mount/ownership changes or alternate destination selection
were performed; a future target requires explicit selection and validation.
Private originals should remain in customer-controlled storage; use reviewed synthetic data
for development. Report snapshots contain evidence and need the same handling as inputs.
Proposed publisher requires owner-private directories/files from creation: POSIX 0700/0600
or a validated platform equivalent, correct owner, and no ACL grants/inheritance exposing
contents to other ordinary accounts. Before writing evidence, preflight filesystem/mount
ownership and ACL support and test an empty exclusive probe on that destination; validate
effective access, not merely chmod success or displayed mode bits. Ignore-ownership volumes
or unsupported/unverifiable protections must refuse publication. Check each empty output
file before filling it and recheck directory/files/marker before completion. No chmod-only
fallback or silent destination change. These controls are not encryption and do not protect
against privileged administrators, the same account, or physical access to an unencrypted drive.

## Startup and shutdown plan after approval

1. Confirm intended volume/mount instance and directory/file identities for all explicit
   inputs and output parent; retain verified handles in one I/O context until shutdown.
   Read/hash from the same opened files and create/write/publish relative to pinned directory
   handles, with mount/identity enforcement across operations. Path checks followed by fresh
   path-based opens are insufficient. Mount loss, replacement, or identity mismatch aborts;
   never recreate a missing mount/path or reopen it as a fallback on the Mac or another volume.
2. Verify package/runtime versions, approved contract version, free disk, explicit input
   paths, and new output parent. Required free-space policy must be measured before release;
   proposed minimum is 3x combined input bytes plus 100 MiB, not a durability guarantee.
   Complete the owner-private capability/probe checks above before any evidence output.
3. Validate hashes/schemas/references before evaluation. Import files as data only. Do not
   spawn tools, follow URLs, load plugins, or obey instructions contained in evidence.
4. Compare under the contract's bounds. Revalidate pinned mounts, directory/file identities,
   and permissions immediately before writing the marker through the retained handles;
   verify again after flush before reporting success. Any detected loss fails closed with
   no successful publication; a marker from an interrupted attempt is not proof of success.
5. Inspect candidate fail/unknown and coverage; ship/hold remains a human decision.
6. Close consumers and flush writes before ejecting the volume. Verify a completed generation
   by marker hashes on reopening; never infer completion from the directory's existence.

No daemon startup is needed for the proposed MVP. The verified development service/history
routing is separate infrastructure, not an application installation prerequisite.
ADR-1/ADR-4 remain blocked. The [B0 storage analysis](decisions/001-runtime.md) describes
descriptor-relative traversal, native mount/UUID/ACL APIs, empty-object validation and a
candidate exclusive marker/flush protocol. Neither Python nor Node alone supplies all
guarantees. Native bridge ABI, continuous identity/failure semantics, effective-access tests
and APFS/USB durability need review and evidence; unsupported storage is rejected.
Only read-only mount/mode observations exist. No product privacy probe, mount-race or
durable-publication test has passed, and the worker restart test is not a substitute for T-09.

## Failure and recovery runbook

| Symptom | Recovery / evidence |
| --- | --- |
| Schema/hash/reference rejection | Preserve original bytes, record Diagnostic/location, correct exporter into a new bundle; do not suppress validation. |
| Unknown or failed assertions | Inspect cited evidence and version changes; improve export or agent outside ReleaseLens; rerun with new provenance. |
| Disk full, disconnected pendrive, process interruption | Treat absent/invalid completion marker as incomplete; keep inputs, quarantine partial output, reconnect/verify mount, retry new generation. |
| Unsupported privacy, ACL drift, mount/path substitution | E_IO / exit 4 without success; do not relax access or recreate/reopen paths. Preserve partial data on its original verified volume; after identity verification, operator chooses an explicit supported destination/new attempt. |
| Output path already exists | Refuse overwrite; select a new generation. Do not delete unfamiliar user files. |
| Corrupt completed generation | Compare marker/file/input hashes; restore verified backup or regenerate from unchanged inputs/package. Hashes detect corruption, not recover bytes. |
| Runtime/package regression | Revert to previous approved compatible package, preserve old reports, regenerate separately. Unsupported schema requires explicit conversion, never silent downgrade. |
| Excess memory/deadline | Record size, runtime, RSS/time if available; reduce reviewed suite scope explicitly. Never drop failing cases to manufacture coverage. |
| Credential/auth problem in delivery | Follow development.md recovery; credentials are not required by local comparison. |
| Future model unavailable | Deterministic comparison remains usable; explanation abstains. No paid endpoint fallback or implicit download. |

Output generation must be created exclusively with verified private access and pinned identity,
and marked complete only after durable-write steps supported by the chosen runtime/filesystem.
Test disconnect/flush behavior on the actual
volume; do not promise transaction semantics from a directory rename. Partial outputs may
be removed only after operator verification of their identity and preserved inputs.

## Retention, backup, and observability

Proposed default: no telemetry and no automatic retention/deletion service. Operator chooses
retention before importing real evidence; keep only needed snapshots and restrict sharing.
Local logs contain codes, hashes, IDs, counts, versions, elapsed time, and resource failures,
not transcripts/credentials. Hashes and identifiers can still reveal correlations.
Explicit report sharing includes embedded evidence; inspect/redact before export. Redaction
must yield new hashes and clearly distinguish results from unredacted generations.
Pendrive storage is not a backup. Track source via reviewed pushes; back up private inputs
and reports only to an existing authorized location without adding spend. Test restore by
checking hashes and replaying a synthetic comparison; remote Git never protects ignored data.

## AI, deployment, and cost gates

No AI runtime/model/weights, GPU fit, quantization, context length, or tool-use capability is
confirmed. M5 investigates at most two local combinations with primary-source license/runtime
documentation and the [AI evaluation gate](testing.md). Model/cache path redirection needs
explicit configuration and effective-path verification before any future download; directories
alone are insufficient. Mac hardware observations do not establish feasible model size/speed.
Optional retrieval/explanations must remain bounded, cited, and unable to alter deterministic
verdicts. Existing customer-owned resources are eligible only with explicit zero-incremental-
founder-cost accounting and a separately approved authority/data boundary.
No hosted deployment, domain purchase, hosted auth/billing, paid inference, or new paid CI
capacity now. Monitor any existing free allocation; exhaustion means stop/report, not upgrade.
Future product release publication needs a separate approved task with exact revision,
rollback steps, and measured installation/recovery evidence. Development-worker provisioning
is already verified in #9; it does not resolve product runtime or storage gates.
