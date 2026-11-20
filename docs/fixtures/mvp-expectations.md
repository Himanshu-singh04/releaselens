# B1: contract-derived expectations

Status: author draft for independent coordinator review, not an evaluator-produced golden.
Definitions: [eight source cases](mvp-cases.md). Authority: [evidence contract](../evidence-contract.md).
This document reasons from that contract before implementation; it reports no executed T-01–06,
runtime/JCS/new N2/N4 validation, deadline enforcement, ten-run result or usability observation.

## Fixed eight-row oracle

Each case has one assertion a1. Baseline has eight complete runs; candidate has seven complete
runs and no C07 run. All present Run.error_code values are null, including candidate C05.
Side.run_id is B-Cxx or C-Cxx as defined in the source register, except missing candidate
C07 has run_id=null and run_status=null. Every expected assertion receives one Outcome,
including synthesized missing/changed outcomes; no assertion is silently dropped.

| Case | Alignment | Baseline presence / run status | Baseline a1 status / reason | Candidate presence / run status | Candidate a1 status / reason | Delta |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | matched | present / complete | pass / MATCH | present / complete | pass / MATCH | unchanged |
| C02 | matched | present / complete | pass / MATCH | present / complete | fail / MISMATCH | regression |
| C03 | matched | present / complete | fail / MISMATCH | present / complete | pass / MATCH | improvement |
| C04 | matched | present / complete | pass / MATCH | present / complete | unknown / MISSING_EVIDENCE | incomparable |
| C05 | matched | present / complete | pass / MATCH | present / complete | unknown / INELIGIBLE_EFFECT | incomparable |
| C06 | matched | present / complete | pass / MATCH | present / complete | unknown / INELIGIBLE_EFFECT | incomparable |
| C07 | missing_candidate | present / complete | pass / MATCH | missing / null | unknown / MISSING_CASE | incomparable |
| C08 | changed_definition | present / complete | pass / MATCH | changed / complete | unknown / CHANGED_CASE | incomparable |

Statuses/reasons in the a1 columns describe a1; each case inherits its sole assertion's
status. Case objects have no invented reason field. C08 baseline still matches the authoritative
hash, while candidate is changed. Whole-row changed_definition does not make baseline changed.
C05 completion error is not Run.status error: the present ineligible effect gives INELIGIBLE_EFFECT,
not RUN_ERROR. C07 missing and C08 changed precede any assertion evaluation on those sides.

## Citation locations and eligibility proof

These are descriptive locations, not serialized Citation objects. Each location expands to
the exact owner/container/artifact_id and pointer shown; artifact_hash must later equal that
selected Artifact.sha256. Derive it by the contract, never borrow a same-ID hash from another
namespace. Effect pairs cite both the observed subject and value in one artifact. No extra
contextual citations are included in these fixed Outcome citation lists; `empty` means no citations.

| Case | Baseline a1 citations | Candidate a1 citations |
| --- | --- | --- |
| C01 | baseline / bundle / record-C01: /order_id and /refund_state | candidate / bundle / record-C01: /order_id and /refund_state |
| C02 | baseline / bundle / record-C02: /order_id and /refund_state | candidate / bundle / record-C02: /order_id and /refund_state |
| C03 | baseline / bundle / record-C03: /order_id and /ticket_state | candidate / bundle / record-C03: /order_id and /ticket_state |
| C04 | baseline / bundle / reply-C04: null | empty |
| C05 | baseline / bundle / record-C05: /order_id and /refund_state | empty |
| C06 | baseline / bundle / record-C06: /order_id and /refund_state | empty |
| C07 | baseline / bundle / record-C07: /order_id and /refund_state | empty |
| C08 | baseline / bundle / reply-C08: null | empty |

Each effect entity selects its record root with pointer `""`; concatenating that with each
one-token selector gives the full citation pointers above. A value citation is exactly the
Observation.value Ref from the specified run. Candidate C04's unbound reply cannot replace a
missing Observation. C05/C06 unknowns have inspectable input evidence but no determinate claim;
empty Outcome citations do not erase their source records, event chains or reasons.
Within each effect pair, /order_id sorts before /refund_state or /ticket_state. Rows C01–C08
and their single a1 outcomes already follow contract ordering. Different owners remain distinct.

For source review, the authoritative definition references (suite, suite, input-Cxx, null) and
(suite, suite, policy-Cxx, null). Their baseline copies resolve in (baseline, suite_snapshot),
and candidate copies in (candidate, suite_snapshot). C08 additionally references kb-injection,
null in each of those suite namespaces. These are review-context locations, not extra Outcome
citations. The old policy must be inspected at candidate / suite_snapshot / policy-C08, null;
looking it up in candidate / bundle would be invalid. Equal IDs do not change that rule.

| Case | Contract-derived justification, independent of any evaluator |
| --- | --- |
| C01 | Matching case definitions; resolve_refund and all four subject claims equal order-01. Independent synthetic-ledger v1 tuple/digest matches the rule; completion success; Tcompletion <= Teffect <= Tfresh <= Tcompletion+60000 ms. Both observed refund_state strings equal refunded: MATCH. |
| C02 | Same binding/freshness conditions for order-02. Tool success means the request was processed, not that a refund was permitted. Baseline observed not_refunded equals expected; candidate observed refunded differs: eligible MISMATCH, not an evidence gap. |
| C03 | Rule/record source is synthetic-ticket-index v1, tool create_ticket, all subjects order-03, same fresh schedule and successful completion. Explicit absent is an eligible string unequal to open (baseline MISMATCH); open equals open (candidate MATCH). Missing data is not used to prove absence. |
| C04 | Baseline's exact observed text Escalation requested. lacks the literal lowercase substring refunded: MATCH for not_contains. Candidate has no Observation, so MISSING_EVIDENCE applies before any string comparison. Unbound claim text/request activity cannot satisfy a negative rule. |
| C05 | Same order-05 binding, matching ledger tuple, matching refunded value and fresh time on both sides. Candidate fx exists and resolves, but done.status=error violates semantic eligibility: INELIGIBLE_EFFECT. Run.status remains complete, so RUN_ERROR has no precedence here. |
| C06 | All order-06/source/tool/selector/completion checks hold. Baseline is fresh; candidate capture 12:01:02.001 exceeds the 12:01:02.000 deadline for this effect observation by 1 ms: INELIGIBLE_EFFECT. This freshness window is distinct from the runtime's 60-second execution obligation. |
| C07 | Baseline order-07 chain matches/freshly verifies refunded. Candidate snapshot retains matching case definition but has no run. Missing-side precedence synthesizes MISSING_CASE with no run metadata, not MISSING_EVIDENCE and not a dangling Ref. |
| C08 | Baseline definition matches authoritative reviewed-v2; observed escalate equals expected: MATCH. Candidate run correctly binds to its own old snapshot, but its case_hash differs from the authoritative case due to policy/definition changes. CHANGED_CASE overrides local complete-run evidence, regardless of refund matching its old expected value. |

The rule subject, Request.subject, Effect.subject and direct record order_id all match in
the fixed effect rows; semantic checks intentionally fail only candidate C05 completion and
C06 freshness. C02/C03 mismatches compare eligible values. A digest authenticates none of
these sources or their causal claims; pass means the assertion matches this supplied evidence.

## Counts derived by inspection

Because there is one assertion per expected case, case and assertion denominators are both eight.
No attached variant belongs to these fixed comparison totals.

| Counts field | Baseline cases | Candidate cases | Baseline assertions | Candidate assertions |
| --- | --- | --- | --- | --- |
| expected | 8 | 8 | 8 | 8 |
| pass | 7 | 2 | 7 | 2 |
| fail | 1 | 1 | 1 | 1 |
| unknown | 0 | 5 | 0 | 5 |
| missing | 0 | 1 | 0 | 1 |
| changed | 0 | 1 | 0 | 1 |
| extra | 0 | 0 | 0 | 0 |
| error | 0 | 0 | 0 | 0 |
| timeout | 0 | 0 | 0 | 0 |
| skipped | 0 | 0 | 0 | 0 |

Baseline evaluated coverage: 8/8 cases and 8/8 assertions. Candidate: 3/8 at both levels.
Aligned pairs: 6 (C01–C06), not merely the 3 pairs with determinate outcomes on both sides.
Deltas: 1 regression, 1 improvement, 1 unchanged, 5 incomparable; the five pass→unknown rows
are coverage losses. Both aggregate statuses are fail; candidate's five unknowns remain visible.
Missing/changed counts overlap unknown; completion errors do not increment run-error counters.
Extra case-ID lists are empty on both sides; neither side has an extra run.

| Assertion evidence-gap reason | Baseline | Candidate | Derivation |
| --- | --- | --- | --- |
| MISSING_EVIDENCE | 0 | 1 | C04 has no Observation |
| TYPE_MISMATCH | 0 | 0 | No fixed-row type mismatch |
| INELIGIBLE_EFFECT | 0 | 2 | C05 failed completion, C06 stale capture |

The candidate gap sum is 3, a subset of 5 unknown assertions: MISSING_CASE and CHANGED_CASE
are excluded. Do not invent an evidence-coverage ratio or shrink the expected denominator.

## Attached paper variants

These bounded annotations attach to the existing eight cases; none is a ninth case, encoded
fixture, executable example or generated payload. Consider each independently, outside the
fixed table/counts above. Mutations apply only to the named candidate run/artifacts unless
explicitly described as a hypothetical definition below. For eventual encoding, recompute affected identities after a mutation;
do not hide semantic/reference tests behind stale hash failures. Changing an assertion/policy
needs a new reviewed case definition; changing only run evidence changes bundle identity.

| Attached annotation | Documentary change or question | Expected consequence and clause |
| --- | --- | --- |
| C01 request-only / completion-only | Keep req only, or req+successful done; remove fx/record. In the Observation for a1, set value=null and effect_event_id=null. Retain only corresponding argument/result artifacts. | Structurally valid absent effect: unknown / MISSING_EVIDENCE. A successful completion still cannot verify a business effect. |
| C01 transcript-only | Keep fx, but replace record-C01 with text/plain from agent-model, exact text refund completed, captured Tfresh. Set entity.pointer=null and both selectors=null. | Resolved text is structurally valid; source/shape/selectors are ineligible: unknown / INELIGIBLE_EFFECT. Do not retain JSON selectors that would make the test a malformed Ref instead. |
| C01 wrong subject | Keep source/time/tool/request/effect/rule order-01; change only the record order_id to order-99. | Ref resolves to a JSON object but same-record observed subject mismatches: unknown / INELIGIBLE_EFFECT, even if refund_state still says refunded. |
| C02 fail precedence | Inspect fixed candidate C02 failure alongside C04–C08 unknowns. | Aggregate remains fail and retains all five unknowns; counters partition the same eight-case set. No extra assertion is added to manufacture this result. |
| C03 dangling entity Ref | Supply entity artifact_id absent-C03, which exists in no owning artifact array, instead of record-C03. | Structurally invalid input; reject the entire modified input, producing no comparison counts/delta. This is not missing evidence or an unknown assertion. |
| C04 absent negative / bound value | Main candidate has no Observation. In a variant, add an Observation for a1 with value Ref reply-C04, null, and effect_event_id=null. | Main is unknown / MISSING_EVIDENCE. Variant's literal text contains refunded, so not_contains fails / MISMATCH and cites candidate / bundle / reply-C04, null. Absence cannot pass the negative rule. |
| C05 run error instead | Change candidate Run.status to error and error_code to TOOL_FAILURE, keeping the supplied chain. | All its outcomes become unknown / RUN_ERROR before effect eligibility. Main run-error counts are zero; this separate variant would make candidate case/assertion error counts 1 and INELIGIBLE_EFFECT gap count 1 instead of 2, with total unknown still 5. |
| C06 inclusive freshness | Change candidate record capture to 2026-01-01T12:01:02.000Z; keep other facts. | Capture exactly completion+60000 ms is eligible: pass / MATCH, citing candidate / bundle / record-C06 subject/value. Main's one-ms-over capture is ineligible. Record content digest stays equal; bundle hash changes because capture metadata changes. |
| C08 hostile selected knowledge | Inspect the unchanged kb-injection sequence and the candidate's old policy in their proper suite namespaces. | Neither instruction text nor ESC may execute or alter outcomes. Display controls visibly escaped (for example printable backslash-u001b and backslash-n), never as terminal controls. Exact escape styling awaits renderer design; source identity still binds the original characters. Candidate remains CHANGED_CASE. |

### C04 numeric annotation: N2 types and identity

For this paper illustration only, consider a value-equals comparison whose expected Scalar
is integer 1; it is not the fixed C04 not_contains assertion and is not an additional case.
Changing to that assertion would require a newly reviewed definition before future encoding.

| Actual numeric/boolean token described | Normalized value/type | Value-equals expectation against integer 1 |
| --- | --- | --- |
| 1 | integer 1 | pass / MATCH |
| 1.0 or 1e0 | integer 1 | pass / MATCH |
| 1.0000000000000001 | integer 1 after accepted binary64 rounding | pass / MATCH |
| true | boolean true | unknown / TYPE_MISMATCH, not integer 1 |
| 1.5 | nonintegral binary64, not Scalar | unknown / TYPE_MISMATCH for an observed actual; invalid if supplied as required expected Scalar |

All numeric input first undergoes N1/N3 rejection. In valid JSON artifact content, 1/1.0/1e0
share normalized semantic content/hash while raw spelling/input byte hashes differ. true has
distinct type/content. Text artifacts containing those spellings are still strings, not numeric
tokens; do not normalize text. Reparse preservation is a prospective N2 requirement, not a test
performed here. The historical lexical-N2 corpus remains untouched.

### C07 byte/depth annotation: N4 accounting

These short token descriptions are paper arithmetic, not encoded artifacts or boundary payloads.
For an illustrative text content value consisting of U+00E9 (é), a raw quoted literal token
uses 4 UTF-8 bytes (two quotes plus two for é); spelling it as quoted backslash-u00e9 uses
8 raw bytes (two quotes plus six escape characters). Both decode to 2 text-content UTF-8 bytes.
If that same content is instead a JSON string value in an application/json artifact, decoded
aggregate accounting uses its JCS bytes, including quotes: 4 bytes. Media type matters.
Whitespace between an artifact property and its value is part of raw suite/bundle bytes, not
the content-value token. Whitespace inside JSON object/array content counts toward its token
limit even when canonicalization removes it. No newline or whitespace is silently trimmed.

| Boundary question attached to C07 | Paper expectation; every other relevant limit must also hold |
| --- | --- |
| Suite/bundle raw bytes | Exactly 5 MiB suite / 25 MiB bundle allowed; one byte beyond rejects. Count all raw UTF-8 bytes including whitespace; MiB=1048576. |
| One artifact raw content token | Exactly 1 MiB allowed; one byte beyond rejects, including quotes/escapes/internal whitespace. Do not test only decoded length. |
| Decoded aggregate | Exactly 20 MiB per artifact array allowed; one byte beyond rejects. Count text UTF-8 or JSON JCS bytes as above. No generated payload or fit claim. |
| Embedded suites | Check authoritative suite.artifacts, baseline bundle.artifacts, baseline suite_snapshot.artifacts, candidate bundle.artifacts and candidate suite_snapshot.artifacts independently. Repeated IDs do not combine arrays or excuse any limit; containing input still obeys its raw limit. |
| Nesting | Root object/array depth 1, primitive depth 0; depth 32 allowed, 33 rejects. Braces inside strings add no depth. No nested array payload is constructed here. |
| BOM | Leading UTF-8 BOM rejects; do not strip it before byte accounting. |

## Clause-to-case audit and review status

| Contract clause | Cases / checkable source and oracle |
| --- | --- |
| [Encoding and provenance](../evidence-contract.md#encoding-identifiers-and-provenance), [shared shapes](../evidence-contract.md#shared-shapes) | Common material/tuple register; N2 annotation; all refs remain owner-local. No computed digest literals. |
| [Case/assertion identity](../evidence-contract.md#suite-and-assertion-definitions) | C01–C07 hash equality, C08 selected policy/expected/source changes; max one fixed assertion per case. |
| [Tool evidence](../evidence-contract.md#bundle-runs-and-tool-evidence) | C01/C02/C03/C05/C06/C07 direct subject/value pairs; C01 attached ineligible versus C03 invalid-reference distinctions. |
| [Time/evaluation](../evidence-contract.md#time-and-evaluation-rules) | Common schedule, C05 completion/run-error distinction, C06 60000/60001 ms; C04 absent negative and C02 fail precedence. |
| [Alignment/coverage](../evidence-contract.md#alignment-and-comparison) | C07 absent run, C08 self-consistent changed snapshot; eight-row counts, six aligned pairs, five incomparable coverage losses. |
| [Reasons/citations/counts](../evidence-contract.md#proposed-report-shape-and-persistence) | Per-side oracle/citation tables; MISSING_CASE/CHANGED_CASE before run/evidence; all denominator and overlapping counters shown. |
| [Bounds](../evidence-contract.md#versioning-and-bounds) | C07 attached N4 paper accounting and independent embedded arrays; no payload/validation claim. |

Every definition and expected result is authored from the documentary contract before an
evaluator exists. This supplies independently reviewable rationale, not independent approval.
The coordinator must audit the case/count/reference trace and resolve any disagreement before
merge; do not rewrite a future oracle just to match implementation output. No unresolved
source/reference conflict was found in this author's paper review; encoding may expose new ones.

All T-01–06, runtime/JCS/new N2/N4, hard-deadline enforcement and ten-run/independent terminal
triage remain unverified. D1–D4 are unadopted; customer/privacy/storage gates remain unchanged.
No customer/path import, Store, persisted report, release package, live agent/action or AI.
M0/M1–M4 remain incomplete. This task stops at source-specification review, without self-dispatch.
