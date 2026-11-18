# Local operations and recovery

Draft plan; no application, package, model integration, persistent project server, or
dedicated project worker is provisioned. [Development](development.md) governs delivery
approval; [roadmap](roadmap.md) gates implementation; [testing](testing.md) defines verification.

## Storage and execution: current reality

| Item | Current location / state | Meaning |
| --- | --- | --- |
| Source and these documents | `/Volumes/AIWorkspace/projects/releaselens` | Pendrive checkout; all task artifacts remain here. |
| CPU and RAM | Existing Mac; observed 16 GiB RAM / 8 logical CPUs | Processes use Mac compute, not pendrive memory; not a benchmark. |
| Coordinator and all current session history | `/Users/himanshusingh/.local/share/opencode/opencode.db` | Current Mac OpenCode service; changing working directory does not relocate history. |
| App private key and `gh` authentication | Mac, outside repository | Credentials remain on Mac; never copied into evidence, pendrive checkout, or CI. |
| Model/cache directories | Directories exist; redirection NOT configured | No claim that model weights/caches currently route to pendrive or that a model is installed. |
| Dedicated project server/workers | NOT provisioned | Temporary documentation specialist is not the promised persistent project worker. |
| GitHub | Remote copies of pushed tracked commits only | Uncommitted/unpushed drafts and ignored local data are not backed up there. |

Desired future project-history placement on the pendrive requires separate configuration,
service restart, mounted-volume checks, and routing verification. Do not move/copy a live
session database casually; obtain the actual service's supported backup/restore procedure
before migration. Keep coordinator history on its existing Mac service unless separately
authorized. Record process identity, effective database path, and verified test-session routing
after restart; provisioned directories alone are not proof. No migration occurs in this task.

## Proposed local runtime and packaging

ADR-1 proposes a TypeScript/Node modular CLI, with Node v26.13.1 as an unverified candidate
pin; exact toolchain/dependencies await review. See [SDD sources](specs/001-mvp/solution-design.md).
Mac-first package, Linux compatibility only after evidence; no Windows support promise yet.
Future package must include built code, contract/version metadata, license inventory, and
reviewed synthetic examples, plus reproducible lockfile/build provenance and checksums.
No customer evidence, credentials, model weights, caches, or session history in releases.
Install/build/product commands do not exist; only [CONTRIBUTING](../CONTRIBUTING.md) commands
are currently executable project instructions. No installer or automatic updater is implied.

Proposed evidence/output placement: explicit paths under ignored local-data/ and artifacts/
in this checkout, operator-selected before use. These are suggestions, not automatic routing.
Private originals should remain in customer-controlled storage; use reviewed synthetic data
for development. Report snapshots contain evidence and need the same handling as inputs.
No account service or app-level encryption is designed; rely on deliberate filesystem access
and existing device protection. A shared machine is not automatically an isolated tenant.

## Startup and shutdown plan after approval

1. Confirm `/Volumes/AIWorkspace` is the intended mounted device and checkout identity;
   fail visibly if absent rather than creating a lookalike directory on the Mac disk.
2. Verify package/runtime versions, approved contract version, free disk, explicit input
   paths, and new output parent. Required free-space policy must be measured before release;
   proposed minimum is 3x combined input bytes plus 100 MiB, not a durability guarantee.
3. Validate hashes/schemas/references before evaluation. Import files as data only. Do not
   spawn tools, follow URLs, load plugins, or obey instructions contained in evidence.
4. Compare under the contract's bounds; publish report files and completion marker last.
5. Inspect candidate fail/unknown and coverage; ship/hold remains a human decision.
6. Close consumers and flush writes before ejecting the volume. Verify a completed generation
   by marker hashes on reopening; never infer completion from the directory's existence.

No daemon startup is needed for the proposed MVP. Current server/history routing work is a
separate infrastructure task, not an application installation prerequisite.

## Failure and recovery runbook

| Symptom | Recovery / evidence |
| --- | --- |
| Schema/hash/reference rejection | Preserve original bytes, record Diagnostic/location, correct exporter into a new bundle; do not suppress validation. |
| Unknown or failed assertions | Inspect cited evidence and version changes; improve export or agent outside ReleaseLens; rerun with new provenance. |
| Disk full, disconnected pendrive, process interruption | Treat absent/invalid completion marker as incomplete; keep inputs, quarantine partial output, reconnect/verify mount, retry new generation. |
| Output path already exists | Refuse overwrite; select a new generation. Do not delete unfamiliar user files. |
| Corrupt completed generation | Compare marker/file/input hashes; restore verified backup or regenerate from unchanged inputs/package. Hashes detect corruption, not recover bytes. |
| Runtime/package regression | Revert to previous approved compatible package, preserve old reports, regenerate separately. Unsupported schema requires explicit conversion, never silent downgrade. |
| Excess memory/deadline | Record size, runtime, RSS/time if available; reduce reviewed suite scope explicitly. Never drop failing cases to manufacture coverage. |
| Credential/auth problem in delivery | Follow development.md recovery; credentials are not required by local comparison. |
| Future model unavailable | Deterministic comparison remains usable; explanation abstains. No paid endpoint fallback or implicit download. |

Output generation should be created exclusively and marked complete only after durable-write
steps supported by the chosen runtime/filesystem. Test disconnect/flush behavior on the actual
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
Future release publication and persistent-worker provisioning each need separate approved
tasks with exact revisions, rollback steps, and measured startup/storage-routing evidence.
