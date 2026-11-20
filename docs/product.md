# ReleaseLens product requirements

Status: planning baseline merged in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6)
for [issue #5](https://github.com/Himanshu-singh04/releaselens/issues/5). [B0 research](decisions/001-runtime.md)
was conditionally accepted in [PR #11](https://github.com/Himanshu-singh04/releaselens/pull/11);
technical validation gates remain open and M0 is incomplete.
The founder adopted exact N1–N4 and synthetic-terminal scope/sequence/AI deferral on 2026-11-20.
[B0d](decisions/005-adopted-policy-reconciliation.md) records authority; normative reconciliation
merged in [PR #19](https://github.com/Himanshu-singh04/releaselens/pull/19). D1–D4 remain unadopted.
Adoption is not tested enforcement or task authorization; [B1](fixtures/mvp-cases.md) has separate source-only permission.
Requirements describe intended behavior, not delivered functionality. No product runtime or tests exist.
See [solution design](specs/001-mvp/solution-design.md), [contract](evidence-contract.md),
[roadmap](roadmap.md), [testing](testing.md), and [operations](operations.md).

## Problem and first customer

A support-automation engineer changes a refund policy, retrieval corpus, system prompt,
model, or tool definition. A few plausible answers do not establish that the agent still
follows policy or actually completes promised actions. Today our proposed user manually
compares transcripts and backend records; this workflow and its frequency need interviews.

Initial user: one engineer maintaining one support agent for a small support team.
Decision partner: the support lead who owns policy and decides whether to release.
First use case: refund eligibility and escalation on a synthetic order-support dataset.
The buyer, procurement process, urgency, and willingness to pay are unvalidated hypotheses.
ReleaseLens is independent of the other portfolio products and has its own release lifecycle.

## Agreed constraints and proposed scope

Already agreed: local-first operation, independent product, no new initial founder hosting
or inference expenditure, imported evidence treated as untrusted data, missing evidence
never promoted to pass, and separation of tool request, completion, and verified effect.
The customer product remains a deterministic file-based comparison CLI with offline HTML/JSON.
The adopted first-demo scope is narrower: bundled synthetic inputs and a terminal display.
CPython 3.14.10 standard GIL / rfc8785 0.1.4 is the conditional direction, uninstalled/unqualified
as a product stack; local 3.13.4 and CI 3.14.4 do not qualify it. AI is deferred beyond
deterministic/pilot gates. Other runtime/build/storage/packaging and enforcement gates remain.
Only the [explicit sequence exception](roadmap.md#ordered-milestones) permits pre-M0 work:
source-only definitions after reviewed schema adoption, then separately authorized pure work
after scoped runtime/JCS validation. It grants no implementation permission by itself.

The later customer release consumes reviewed synthetic fixtures, then operator-prepared baseline
and candidate exports. It does not call the agent under test. Export preparation is an
explicit pilot cost; vendor adapters and live execution are deferred until demand is known.
No hosted accounts, authentication service, billing, dashboard, production monitoring,
autonomous release gate, customer tool execution, or shared portfolio backend is in MVP.

## Narrow workflow and acceptance scenarios

Adopted first-demo journey: select the bundled refund-policy example, compare fixed baseline/
candidate, and read a terminal table of both outcomes, delta, reason, citations and coverage.
Accept no user-supplied paths/customer evidence; escape terminal control characters. Keep all
eight reviewed rows, including missing/changed cases. Ten identical comparisons must yield
the same Result hash, and an independent reviewer must explain the regression and coverage
loss without author interpretation. These are future acceptance criteria, not completed results.
Preserve exact Scalars, pass/fail/unknown, request/completion/effect separation, same-record
subject/value/source/time eligibility and missing-negative-observation rules. No agent executes.
The demo tests understanding of evidence gaps; it establishes neither demand nor policy truth.
No Store, persisted report or release package; arbitrary imports, durable recovery, HTML/JSON,
installer/pilots, adapters, database/server, AI and live actions remain deferred. Public synthetic
source may stay on the checkout, without qualifying it for customer evidence. The original
60-second deadline remains; any unresolved enforcement conflict blocks that inference of readiness.

The customer workflow remains separately gated:

1. Engineer and support lead review a versioned suite of refund/escalation cases and rules.
2. Engineer obtains exports outside ReleaseLens for the unchanged baseline and changed agent.
3. Engineer supplies the reviewed suite and two evidence bundles to local comparison.
4. ReleaseLens validates hashes/references, aligns cases, evaluates deterministic assertions,
   and writes a new offline report showing candidate failures and evidence gaps first.
5. Lead inspects source/version changes, assertion evidence, and coverage; makes a human
   ship/hold decision outside the tool. The report is an aid, never release authorization.

Scenario S1: baseline escalates an ineligible refund; candidate refunds it. A matching
backend observation supports candidate fail, even if the final answer sounds correct.
Scenario S2: candidate says “refunded” and requests a refund, but has no completion or
business observation. Effect assertion is unknown, not pass and not a fabricated failure.
A refund record for order-8 cannot verify order-7, even with valid hashes and matching tool
metadata: observed subject and value must come from the same independently sourced record.
Scenario S3: a candidate omits a baseline case or changes its definition. The missing or
incompatible row remains visible; intersection-only pass percentages are prohibited.
Scenario S4: both bundles reproduce all reviewed cases with sufficient evidence. Passing
means only that these assertions passed against these imports, not that the agent is safe.

## Requirements

IDs are stable; changing meaning requires a reviewed PR and contract/test impact review.
Rows retain the customer-product acceptance obligations. Adopted numeric rules apply throughout;
the terminal demo does not fulfill RL-008/011 publication. Phase labels imply no implementation.

| ID | Requirement and observable acceptance | Phase |
| --- | --- | --- |
| RL-001 | Accept a nonempty reviewed suite with stable case/assertion IDs, source versions, and content hashes; reject ambiguous definitions. | MVP |
| RL-002 | Import only explicit local data; reject invalid schemas, hashes, duplicate IDs, broken references, or unsupported versions before evaluation. | MVP |
| RL-003 | Preserve run, model/prompt/tool/knowledge configuration provenance and original evidence references; unknown provenance is explicit. | MVP |
| RL-004 | Evaluate deterministic rules with pass/fail/unknown; absent or resolved-but-ineligible evidence stays unknown for positive and negative rules, while malformed/dangling references reject import. | MVP |
| RL-005 | Distinguish request, completion, and independently sourced effect; observed subject/value must bind to one business-record object, with observed subject equal to rule/request/effect subject. “Success” text alone cannot establish an effect. | MVP |
| RL-006 | Align against the reviewed suite; show missing, extra, changed, errored, skipped, and timed-out cases without shrinking coverage denominators. | MVP |
| RL-007 | Compare baseline/candidate outcomes with regression, improvement, unchanged, and incomparable labels; show candidate failures even when baseline fails. | MVP |
| RL-008 | Produce self-contained offline HTML/JSON with evaluated coverage, defined evidence-gap reason counts, source/version differences, and owner/container-qualified citations. A separate evidence-coverage metric is deferred. | MVP |
| RL-009 | Repeated deterministic evaluation of identical inputs and evaluator version produces identical semantic results and content IDs. | MVP |
| RL-010 | Enforce bounded resources and data-only handling; no network, script execution, plugins from imports, or hidden inference. | MVP |
| RL-011 | Write immutable report generations; interruption, full disk, or missing mount leaves no apparently complete partial report. | MVP |
| RL-012 | Provide a zero-new-spend local setup/recovery path and versioned release provenance; expose limitations before pilot use. | MVP |
| RL-013 | Later AI/RAG explanations cite exact imported evidence, abstain on insufficient support, and cannot override deterministic outcomes. | Later gate |
| RL-014 | Any later agent/adapter has explicit bounded authority, budgets, and held-out evaluations before use; never infer effect from a request. | Later gate |

## Meaning of success

Product success hypothesis: engineers can identify the intentionally introduced refund
regression and explain the evidence gap without asking the author to interpret the report.
Pilot proposal: three teams, two policy/prompt revisions each, at least 20 reviewed cases
per team, and two weeks of observation after an MVP exists. These are recruitment targets.
Proposed usability targets: first synthetic comparison within 15 minutes; report triage
within 10 minutes in at least four of six observed sessions. Nothing is measured yet.
Proposed demand signal: two teams voluntarily repeat comparison for a second real change.
Record failed onboarding and export-preparation time, not just successful sessions.

Pricing hypothesis: test willingness to pay $29–$99 per team/month for a supported local
tool, or a one-time paid pilot setup. Neither a price nor a commercial model is selected.
Ask what users would replace and who could authorize payment before building billing.
If export preparation dominates saved review time, narrow supported evidence or revisit
the workflow before adding a hosted platform. No demand or revenue is claimed.

## Decision ownership and traceability

Owner confirms product scope and significant ADRs on the reviewed documentation revision;
the approval and exact-SHA procedure lives in [development](development.md).
The persistent development worker is verified in [issue #9](https://github.com/Himanshu-singh04/releaselens/issues/9);
worker delivery is not independent review or owner approval.
[Testing](testing.md) maps every requirement to planned verification; [roadmap](roadmap.md)
maps issue acceptance A1–A7 to artifacts and coordinator-owned delivery evidence.
Policy authors own expected outcomes; engineers own export provenance; release owners own
ship/hold decisions. ReleaseLens cannot establish exporter honesty from a content hash.
