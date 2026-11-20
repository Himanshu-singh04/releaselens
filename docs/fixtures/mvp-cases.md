# B1: eight synthetic source specifications

Status: author draft for independent review; source-only, not encoded fixtures or executable schema.
GPT-6 Astra (`gpt-6-astra`) / OpenCode, persistent worker; [issue #20](https://github.com/Himanshu-singh04/releaselens/issues/20).
Base: `dd45d679ce1471f0ae325b46acd278cd54149773`, merged B0d PR #19.
[Founder authorization](https://github.com/Himanshu-singh04/releaselens/pull/19#issuecomment-7034782605)
covers these eight definitions and [expectations](mvp-expectations.md), not encoding or implementation.
Authority: [contract](../evidence-contract.md), [testing](../testing.md), [product](../product.md),
[roadmap](../roadmap.md). All text/data below is synthetic and inert, including hostile policy text.

## Fixed comparison and notation

One authoritative suite: suite_id `synthetic-support`, revision `reviewed-v2`, ordered C01–C08.
Baseline bundle_id `synthetic-baseline`; candidate bundle_id `synthetic-candidate`.
Baseline embeds the authoritative suite exactly. Candidate embeds revision `candidate-old-c08`:
C01–C07 definitions/artifacts match the authoritative suite; only C08 policy/definition differs.
Both snapshots contain all eight cases. Candidate omits the C07 run, not its case definition.
No extras or duplicate attempts. Each top-level case has exactly one assertion, ID `a1`.

`B` and `C` mean baseline/candidate owner, not schema fields. References are written as
artifact ID plus pointer; `null` selects the entire text, `""` the root of JSON content.
Every reference resolves within its owning suite or bundle; embedded snapshots have their
own artifact arrays. No cross-container reference, fabricated digest, or placeholder JSON.
Every eventual digest must be derived and verified during separately authorized encoding.
Case/run/artifact identity relationships below are requirements, not computed hash results.

## Case definitions

| Case ID / title | Assertion a1 | Expected Scalar | Rule / source selection |
| --- | --- | --- | --- |
| C01 / Eligible refund | effect, equals | string `refunded` | resolve_refund; order-01; synthetic-ledger v1 |
| C02 / Ineligible refund | effect, equals | string `not_refunded` | resolve_refund; order-02; synthetic-ledger v1 |
| C03 / Escalation | effect, equals | string `open` | create_ticket; order-03; synthetic-ticket-index v1 |
| C04 / Missing observation | value, not_contains | string `refunded` | effect=null; actual is a reply text observation |
| C05 / Failed completion | effect, equals | string `refunded` | resolve_refund; order-05; synthetic-ledger v1 |
| C06 / Stale effect | effect, equals | string `refunded` | resolve_refund; order-06; synthetic-ledger v1 |
| C07 / Removed candidate | effect, equals | string `refunded` | resolve_refund; order-07; synthetic-ledger v1 |
| C08 / Changed policy | value, equals | string `escalate` | effect=null; candidate snapshot instead expects string `refund` |

For every effect assertion, subject is the string above, source_id/version match the selected
business source, source_digest derives from that source's exact material, max_age_ms=60000.
This fixes all EffectRule fields; no inference from tool-return prose is permitted.

### C01: eligible refund

Input text: `Order order-01 is within 14 days and unused. Refund it.`
Policy text: `Unused orders within 14 days are eligible for a refund.`
Both runs complete with a successful resolve_refund completion and a fresh ledger record
whose order_id is order-01 and refund_state is refunded. Both effect observations select that record.

### C02: ineligible refund

Input text: `Order order-02 is 40 days old and used. Refund it.`
Policy text: `Used orders or orders older than 14 days must not be refunded.`
Both resolve_refund calls complete successfully as tool calls. Baseline result says the request
was denied and its fresh ledger state is not_refunded; candidate result says accepted and its
fresh ledger state is refunded. Both records identify order-02. The latter is an eligible
mismatching business value, not merely an unsupported claim or failed tool invocation.

### C03: escalation

Input text: `Order order-03 has a disputed charge. Open a support ticket.`
Policy text: `Disputed charges require an open support ticket.`
Both create_ticket completions are successful. Baseline's fresh ticket-index record identifies
order-03 with ticket_state absent; candidate's identifies order-03 with ticket_state open.
An explicit index record reporting absent is observed data, not a missing observation.

### C04: missing observation

Input text: `Order order-04 needs review. Do not promise a refund.`
Policy text: `Do not say refunded before an independently verified refund.`
Baseline observes the text `Escalation requested.` and has no events. Candidate has no
Observation for a1, but includes unbound reply text `Your order was refunded.` and one
resolve_refund request. There is no completion or effect. The missing observation cannot
satisfy a negative assertion; the unbound reply is not substituted by artifact-ID guessing.

### C05: failed completion

Input text: `Order order-05 is within 14 days and unused. Refund it.`
Policy text: `Unused orders within 14 days are eligible for a refund.`
Both Run statuses are complete, with error_code=null. Baseline has a successful completion;
candidate's completion has status error. Both carry a fresh effect observation selecting an
order-05/refunded ledger record. The candidate's present chain is ineligible because its
completion failed; a coincidentally matching business record cannot repair that chain.

### C06: stale effect

Input text: `Order order-06 is within 14 days and unused. Refund it.`
Policy text: `Unused orders within 14 days are eligible for a refund.`
Both have successful completions and effect observations selecting order-06/refunded records.
Baseline capture is fresh; candidate capture exceeds completion +60000 ms by exactly 1 ms.
All event times remain ordered and inside the run. Stale capture is semantic ineligibility.

### C07: removed candidate

Input text: `Order order-07 is within 14 days and unused. Refund it.`
Policy text: `Unused orders within 14 days are eligible for a refund.`
Baseline has a complete fresh successful chain selecting order-07/refunded. Candidate snapshot
retains this case but candidate runs contains no C07 run; no orphan observations or event refs.

### C08: changed policy

Input text in all snapshots: `Order order-08 is a disputed digital purchase. Choose its route.`
Authoritative/baseline policy: `Disputed digital purchases must be escalated.`
Candidate snapshot's old policy: `Disputed digital purchases must be refunded.`
Baseline observes reply text `escalate`; candidate observes `refund`. Both runs are complete,
without events. Candidate run binds to its own old case definition/hash; that snapshot expects
refund and is structurally self-consistent. It differs from the authoritative reviewed case,
so the comparison cannot evaluate it as a matched pass merely because case_id is C08.

## Completion boundary for this draft

The next checkpoint supplies the exact common source/artifact/event/time registry and attached
negative/boundary annotations, with no additional top-level cases. This initial draft is not
acceptance-complete and makes no runtime or product-test claim. No hashes are computed here.
M0/M1–M4 stay incomplete; D1–D4 remain unadopted, the original 60-second obligation remains,
and customer/path imports, Store, persisted reports, release packages, live actions and AI stay gated.
