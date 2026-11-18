# Testing and evaluation plan

Status: proposed tests and targets; no product code, fixtures, benchmark, or model exists.
Only foundation checks currently run. Requirements: [PRD](product.md); expected semantics:
[evidence contract](evidence-contract.md); component boundaries: [SDD](specs/001-mvp/solution-design.md).

## Existing checks

Use the four existing commands in [CONTRIBUTING](../CONTRIBUTING.md): repository checker,
policy unittests, actionlint, and diff check. They validate repository policy, not this
product's correctness. The repository checker sees tracked files only; coordinator must
stage new documents before its link/format coverage includes them. Supplementary draft
validation must check all new files, template heading order, and requirement coverage.
Live PR-record validation and CI verification belong to coordinator delivery, not this draft.

## Requirement-to-design-to-test matrix

All T-* entries below are planned, not existing tests. Reviewer writes expected results
before evaluator implementation; author and reviewer disagreement becomes a case review.

| Test | Requirements / design boundary | Required cases and oracle |
| --- | --- | --- |
| T-01 suite contract | RL-001, RL-002; Importer/Contract | Empty suite/assertions, duplicate IDs/keys, unsafe numbers, invalid Unicode, unsupported schema, unknown fields; each rejects with bounded diagnostic. |
| T-02 provenance/integrity | RL-002, RL-003; Importer/Contract | Alter bytes, policy metadata, hashes, or source versions; dangling/cross-container refs, invalid pointer escaping, wrong pointer type, duplicate run/event IDs, missing linked events; reject entire input. Null provenance stays explicit. |
| T-03 value tri-state | RL-004; Evaluator | Exact equals, literal contains/not_contains, wrong actual type, missing observation, explicit null value, negative assertion without evidence; unknown never satisfies not_contains. Aggregate fail beats unknown without hiding it. |
| T-04 effects | RL-005; Evaluator | Request only; completion only; completion error; agent “success” text; stale/missing time; wrong source/tool/subject; fresh matching and mismatching business values. Only eligible observation can pass/fail; others unknown. |
| T-05 alignment/deltas | RL-006, RL-007; Evaluator | Missing baseline/candidate/both, changed case hash, different suite ID, extra cases, empty runs, error/timeout/skipped, duplicate attempts. All nine pass/fail/unknown pairs; pass→unknown flags coverage loss. |
| T-06 reproducibility | RL-009; Contract/Evaluator | Ten runs of identical inputs/version have same Result hash; generated_at may differ. Object key order changes preserve semantic hash, byte hashes differ; source-array order remains significant. Changed evaluator version changes Result identity. |
| T-07 offline presentation | RL-008, RL-010; Renderer | JSON/HTML verdict parity, visible denominators/reasons/provenance, valid citations, script tags/event handlers/URLs in evidence remain inert, offline browser makes zero requests; keyboard-readable headings/tables. |
| T-08 bounds/performance | RL-010; CLI/Importer | Every limit at boundary and one unit beyond, oversized/deep JSON, huge escaped strings, deadline expiry. Record wall time, peak RSS, bytes, cold/warm volume state, toolchain and hardware. |
| T-09 recovery | RL-011, RL-012; Store | Inject write failure, full disk, permission loss, interrupted marker write, existing output, disconnected volume; no complete corrupt generation. Verify input hashes unchanged, explicit retry uses new path. |
| T-10 usability/install | RL-012; CLI/Renderer | Clean local package install/replay from guide; observe first comparison and triage without author assistance. Record failures, inaccessible report sections, export effort, and package/runtime versions. |
| T-11 optional AI/agent | RL-013, RL-014; future boundary | Citation validity/support, abstention, retrieval omissions, conflicting/outdated policy, injection, hallucinated effects, attempted tool authority, budget exhaustion, deterministic-result preservation. Gate below. |
| T-12 cost/isolation | RL-010, RL-012; operations | No paid hosting/inference credentials or downloads in required product checks; network-denied comparison works; models/customer evidence absent from package/Git. Confirm usage stays inside existing no-new-spend allocation. |

## Fixtures and review discipline

Start with eight synthetic order-support cases in B1; later expand negative cases, not only
happy-path volume. Include a false “refund completed” answer with no business effect, an
unauthorized refund with a real effect, an escalation without a support ticket observation,
and changed knowledge that contradicts older policy. Exact rule tests do not prove semantic
policy compliance. One case should contain malicious instructions in a retrieved document.
No real customer transcripts in public Git or CI. Redaction alters evidence identity; retain
the redaction process/version in exporter provenance and review expectations on redacted data.
Pin suite, artifact, bundle, evaluator, package/lockfile, and runtime hashes/versions in test
records. Validate JCS against RFC vectors and pointer escaping independently of report snapshots.
Use property checks for fail/unknown aggregation, expected-count conservation, and reference
closure; golden files alone can conceal systemic denominator errors.

## Proposed measurements and gates

Nothing here is measured. On a 100-case/10-assertion fixture with <=10 MiB total inputs,
target <=10 seconds and <=512 MiB peak RSS for each of 10 local runs. Proposed hard limits
are in the contract, including a 60-second deadline. A resource failure is an operational
error, never a comparison pass. Report both cold and warm pendrive readings and outliers.
Observed 16 GiB RAM/8 logical CPUs describes the host, not capacity or an achievable SLA.
Required CI uses synthetic data, no paid inference/hosting, no model downloads, and existing
allocation only; if that allocation is exhausted, stop and report instead of buying capacity.
Pilot targets: <=15 minutes first comparison, <=10 minutes triage in four of six sessions,
and two teams repeating on a second change. Log recruitment shortfalls; do not fabricate users.

## Later AI/RAG/agent evaluation gate

No runtime/model is selected. Proposed role: explain existing outcomes or suggest new cases
for human review. Retrieval is local over explicitly imported policy/knowledge/evidence only;
no web search, hidden memory, or customer tool calls. Preserve source/version/hash per chunk.
Proposed retrieval budget: <=8 chunks, <=1000 UTF-8 bytes/chunk; <=2048 output tokens and
30 seconds per explanation; concurrency one. These limits are unmeasured and model-dependent.
If context cannot fit, retrieval is insufficient, sources conflict, or a budget expires,
abstain. Cite exact artifact pointers and quoted spans; validate pointers and quote equality
deterministically, then have humans judge whether citations actually support the claim.

Proposed output: `{case_id, status:"supported"|"abstained", explanation, citations, reason}`,
where citations use contract Citation plus `quote:string`; quote must be an exact substring
of the selected string. Non-string evidence is cited without a quote in a separately reviewed
future schema. Unsupported/invalid output becomes abstained; it cannot modify Result/status.
AI-derived case suggestions remain separate drafts; importing them never executes their text.

Before approval, assemble 60 held-out labeled examples separate from prompt tuning: supported,
missing evidence, policy conflict, stale retrieval, injection, and fabricated-effect groups.
Run each three times, retaining model ID/weights hash/license/quantization/runtime version,
prompt/retriever versions, decoding settings, seed if supported, hardware, timings, and costs.
Proposed gate: 100% structurally resolvable citations; >=95% human-rated supported claims;
>=90% abstention on insufficient/conflicting cases; zero unauthorized actions or deterministic
verdict changes. Report numerator/denominator and per-group failures, not a single average.
These are pilot gates, not population guarantees. Failed gate keeps AI disabled.

Agent authority proposal: read only the current validated bundle and return a bounded JSON
explanation/suggestion. No shell, filesystem writes, credentials, network, report edits,
customer actions, or release authorization. Adapter/agent expansion requires new design,
explicit owner approval, and adversarial tests; model instruction-following is not a sandbox.
