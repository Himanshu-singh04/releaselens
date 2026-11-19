# Testing and evaluation plan

Status: proposed product tests and targets; no product code, benchmark, or model exists.
Foundation and [B0b research checks](decisions/003-json-conformance.md) run; the latter
are finite parser/JCS controls, not product tests or runtime qualification. Requirements: [PRD](product.md); expected semantics:
[evidence contract](evidence-contract.md); component boundaries: [SDD](specs/001-mvp/solution-design.md).

## Existing checks

Use the four existing commands in [CONTRIBUTING](../CONTRIBUTING.md): repository checker,
policy unittests, actionlint, and diff check. They validate repository policy, not this
product's correctness. The repository checker sees tracked files only; the author must
stage new documents before its link/format coverage includes them. Supplementary draft
validation must check all new files, template heading order, and requirement coverage.
Workers record live PR-policy/CI outcomes; the coordinator independently verifies delivery.
The [B0 investigation](decisions/001-runtime.md) includes read-only runtime/mount observations,
not T-* results. Current noowners storage, native APIs, and unproven publication/failure
semantics block readiness; R5/R7 remain required and unchanged.
The [B0a protocol](decisions/002-storage-protocol.md) maps these obligations to G1–G9 and
the finite F-01–24 fault matrix. All capability/fault tests remain unperformed; simulated
faults, process kills and physical power loss have distinct evidence limits. No eligible
external test target is authorized/provisioned, and counterexamples are not passing tests.

## Requirement-to-design-to-test matrix

All T-* entries below are planned, not existing tests. Reviewer writes expected results
before evaluator implementation; author and reviewer disagreement becomes a case review.

| Test | Requirements / design boundary | Required cases and oracle |
| --- | --- | --- |
| T-01 suite contract | RL-001, RL-002; Importer/Contract | Empty suite/assertions, duplicate IDs/keys, unsafe numbers, invalid Unicode, unsupported schema, unknown fields; each rejects with bounded diagnostic. |
| T-02 provenance/integrity | RL-002, RL-003; Importer/Contract | Alter bytes, policy metadata, hashes, or source versions; dangling/cross-container refs, malformed/unresolved entity or member selectors, duplicate run/event IDs, missing linked events; reject entire input. Resolved text/nonobject effect entities are structurally valid. Null provenance stays explicit. |
| T-03 value tri-state | RL-004; Evaluator | Exact equals, literal contains/not_contains, wrong actual type, missing observation, explicit null value, negative assertion without evidence; unknown never satisfies not_contains. Aggregate fail beats unknown without hiding it. |
| T-04 effects | RL-004, RL-005; Evaluator | Request only; completion only/error; resolved transcript/tool-return refs; stale/missing time; wrong source/tool/observed subject; null/non-direct selectors; fresh matching/mismatching eligible values. Ineligible evidence imports successfully then yields unknown. Same-record subject binding vectors below. |
| T-05 alignment/deltas | RL-006, RL-007; Evaluator | Missing baseline/candidate/both, changed case hash, different suite ID, extra cases, empty runs, error/timeout/skipped, duplicate attempts. All nine pass/fail/unknown pairs; pass→unknown flags coverage loss. |
| T-06 reproducibility | RL-009; Contract/Evaluator | Ten runs of identical inputs/version have same Result hash; generated_at may differ. Object key order changes preserve semantic hash, byte hashes differ; source-array order remains significant. Changed evaluator version changes Result identity. |
| T-07 offline presentation | RL-008, RL-010; Renderer | JSON/HTML parity, evaluated-coverage denominators and evidence-gap counts, namespace-qualified citations with collision vectors below; invalid generated citation blocks publication. Script tags/event handlers/URLs remain inert; zero browser requests; keyboard-readable headings/tables. |
| T-08 bounds/performance | RL-010; CLI/Importer | Every limit at boundary and one unit beyond, oversized/deep JSON, huge escaped strings, deadline expiry. Record wall time, peak RSS, bytes, cold/warm volume state, toolchain and hardware. |
| T-09 recovery | RL-011, RL-012; Store/Importer | Private access/probe enforcement, mount/path substitution during I/O, write failure, full disk, interrupted marker, existing output; no false success or redirected writes. Verify input hashes unchanged; explicit retry follows identity verification. |
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

R1/T-04: keep valid hashes, accepted source tuple, fresh times, successful completion, and
rule/request/effect subject=order-7. Select an order-8 entity with refunded: unknown, not pass.
In one artifact containing orders[0]=order-7/pending and orders[1]=order-8/refunded, selecting
the root with /orders/0/order_id and /orders/1/refund_state resolves but is ineligible (multi-token
selectors). Selecting /orders/0 with /order_id and /refund_state yields fail; the correct
order-7/refunded record yields pass. Both pass/fail outcomes cite the observed ID and value.
R2/T-02/04: a resolved text transcript with null selectors, a resolved nonobject JSON value,
or a resolved JSON tool-return record yields unknown; a malformed or dangling entity/member
pointer rejects import. Do not use dangling references to simulate absent evidence.
R3/T-07: reuse one artifact_id with different content/hashes in all five valid owner/container
namespaces. Each citation must resolve only its qualified target, including escaped pointer
tokens. Swapped namespaces/hash, invalid owner/container pairs, or missing target must fail
without fallback; test deterministic sort and that cross-namespace IDs are not deduplicated.
R4/T-05/07: three expected cases, one effect assertion each: request-only complete run, stale
effect complete run, and error run. Each side's counts are expected=3, pass=0, fail=0, unknown=3,
error=1; evaluated coverage=0/3 at case and assertion levels. Evidence-gap counts are
MISSING_EVIDENCE=1, INELIGIBLE_EFFECT=1, TYPE_MISMATCH=0; RUN_ERROR is excluded from that sum.
No separate evidence-coverage field/percentage is rendered. These are planned vectors only.

R5/T-09: permissive umask, inherited broad ACL, wrong owner, ignore-ownership/unsupported
volume, and ACL drift must not expose evidence or publish successfully. Verify empty-probe
rejection before evidence writes and denied access from another ordinary account on supported
platforms; mode-bit/chmod assertions alone do not qualify. Record filesystem/mount settings.
R7/T-09: replace/unmount the volume or swap an ancestor after preflight, during input reads,
between writes, and immediately around marker publication. Verify retained-handle identity
enforcement, failure on loss, no local/replacement-volume files or fallback directories,
and no success announcement; include a supported-volume success control. Platform feasibility
is unproven; design review must identify required OS APIs/helpers before implementation.
R8/T-03/07: every pass/fail value outcome includes its exact observed citation. Remove it or
replace it with a valid same-kind artifact (even equal content), another pointer, or another
side/container: report publication rejects with E_INTERNAL. Include correct text-null and
JSON-pointer citations, extra contextual citations, and unknown-with-no-evidence controls.
R9/T-01/02/10: compare --bogus locates argument index 1; repeated flag locates its second
occurrence; missing value locates its flag; wholly missing required flag and unlocatable
system errors use null. Input errors identify suite/baseline/candidate plus a schema-known
pointer (root for parse failure). Validate exact tagged shapes and no raw values/paths/token
text in diagnostics, including secret-like argv and unknown JSON keys.

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
where citations use owner/container-qualified contract Citation plus `quote:string`, resolved
only within its exact namespace; quote must be an exact substring
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
