# Proposed roadmap and bounded backlog

Planning baseline for [issue #5](https://github.com/Himanshu-singh04/releaselens/issues/5)
merged in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6); App corrections
merged in [PR #8](https://github.com/Himanshu-singh04/releaselens/pull/8), and development-worker
provisioning is verified in [issue #9](https://github.com/Himanshu-singh04/releaselens/issues/9).
B0 research merged in [PR #11](https://github.com/Himanshu-singh04/releaselens/pull/11),
conditionally accepting the direction with validation gates still open.
The founder subsequently adopted N1–N4 and the synthetic-terminal exception below;
[B0d](decisions/005-adopted-policy-reconciliation.md) records exact authority and this pending
reconciliation. D1–D4 remain unadopted; the B0c packet's recommendation bundle was not adopted.
None completes M0 or delivers a product milestone. Dependencies are gates, not calendar promises. Scope is in the
[PRD](product.md), contracts in the [SDD](specs/001-mvp/solution-design.md), tests in
[testing](testing.md), and local execution/recovery in [operations](operations.md).

## Ordered milestones

Adopted exception: “After reviewed schema adoption, B1 source-only synthetic definitions may precede M0.
After scoped runtime/JCS validation, separately authorized pure Contract/Evaluator/terminal-renderer
slices may precede native storage and full packaging qualification.
Accept only bundled reviewed synthetic inputs; no customer/path import, Store,
persisted report or release package. M0/M1–M4 remain incomplete.”

This changes task ordering, not the customer milestone exits below. This reconciliation
must merge before the coordinator separately requests the eight-case fixture-specification
slice; no fixture task or implementation is authorized now. Later pure work needs scoped
runtime/JCS/replacement N2/expanded N4 validation and its own bounded implementation permission.
The original 60-second deadline remains for the demo; unverified terminal-I/O/scheduling
completion is a blocker to claiming readiness, not adoption of D4. AI deferral is adopted.

| Milestone | Depends on | Observable exit evidence | Exclusions |
| --- | --- | --- | --- |
| M0: confirm design | B0 technical decisions after merged planning baseline | Owner decision on exact revision, ADR-1–5 resolved, independent consistency review, foundation checks and PR record. | No provisioning; only the separately authorized synthetic exception above may precede closure. |
| M1: deterministic contract fixtures | M0; runtime/schema decisions | Reviewed synthetic refund/escalation corpus; parser/hash/reference rejection vectors; T-01/02 pass. | No agent calls or AI. |
| M2: baseline/candidate evaluator | M1 | Golden tri-state/effect/alignment results; T-03/04/05/06 pass with all expected cases retained. | No vendor adapter. |
| M3: local report and recovery | M2 | Offline HTML/JSON parity; inert rendering, bounded resources, interruption recovery; T-07/08/09/12 pass. | No server/accounts/billing. |
| M4: narrow pilot and packaging | M3 | Reproducible local package, version/provenance record, observed onboarding, six comparison sessions sought; T-10 evidence. | No claim that recruitment targets are demand. |
| M5: optional grounded AI investigation | M4 evidence plus new approval | Primary-source runtime/model/license research, measured local fit, held-out T-11 results, authority/cost decision. | No autonomous business effects or automatic shipping. |

ADR-5's AI deferral is adopted for the deterministic demo/MVP; M5 still needs its own design
approval. Outside the exact synthetic exception, unresolved runtime/schema/packaging ADRs
cannot be bypassed to “start scaffolding.” The exception does not complete M0 or any milestone.
An owner may reject or change proposals; update dependent docs and obtain fresh revision review.

## Issue-ready task slices

B0–B0d below have linked issues; B1–B9 remain proposed tasks, not created/authorized issues.
Every implementation PR
must carry a bounded scope, requirement IDs, expected test outcomes, and review evidence.

| Task | Dependency / scope cap | Acceptance and verification |
| --- | --- | --- |
| B0: investigate design gates | #10 closed by merged PR #11; accepted research | [Recommendation/results](decisions/001-runtime.md): conditional Python target, Node comparison, exact candidate versions and untested gaps; current noowners mount rejected. M0 remains blocked. |
| B0a: storage capability protocol | #12 closed by merged PR #13; accepted documentation | [Protocol](decisions/002-storage-protocol.md), including R1 interruption-layer correction: minimal Darwin ABI, proposed target eligibility (none authorized/provisioned), finite R5/R7/durability/deadline matrix and explicit NO-GO guarantees. D1–D4 unaccepted; E1 unauthorized. No helper code, installs or mount changes. |
| B0b: finite JSON/JCS research | #14 closed by PR #15; accepted research | [Historical controls](decisions/003-json-conformance.md); lexical N2 is not current policy or validation of replacement N2/N4. |
| B0c: decision packet | #16 closed by PR #17; accepted documentation | [Packet](decisions/004-mvp-decision.md); subsequent separate numeric/scope adoption recorded in B0d. D1–D4 unadopted. |
| B0d: adopted-policy reconciliation | #18; current documentation-only task | [Authority/trace](decisions/005-adopted-policy-reconciliation.md); review and exact-revision approval before merge. No fixture specs/code. |
| B1: fixture vocabulary | Source-only definitions may precede M0 after reviewed schema adoption, reconciliation merge and separate authorization; 8 cases, <=3 assertions each | Include eligible refund, ineligible refund, escalation, missing observation, failed completion, stale effect, removed case, changed policy. Lead reviews expectations independently; no customer data. Encoding/executable work needs its own scope/gates. |
| B2: import/identity boundary | Customer path: M0 and B1; Suite/Bundle only | Implement schema/hash validation with malformed, duplicate, dangling-ref and source-version tests T-01/02. Only pure Contract work can use the pre-M0 exception; no customer/path import there. |
| B3: value and effect rules | Customer: M0 and B2. Synthetic: reviewed B1 definitions and validated pure Contract subset under the exception | T-03/04 verify exact tri-state semantics, time/source eligibility, and negative assertions. No fuzzy semantic judge. |
| B4: alignment and deltas | B3; same lane-specific gates; one attempt/case/bundle | T-05/06 verify expected-set denominators, changed hashes, all nine outcome pairs, extra/missing rows, and reproducible result hash. |
| B5: offline report | Customer path: M0 and B4; one HTML/JSON layout | T-07 verifies shared Result, escaped evidence, inspectable references, zero external requests, and keyboard navigation. The separately scoped terminal renderer does not satisfy this exit. |
| B6: publication and limits | B5; one local output lifecycle | T-08/09 cover bounds, private-access probes/ACLs, mount substitution across I/O/publication, partial writes, collisions, and recovery without overwrites or path fallback. |
| B7: package and pilot guide | B6; Mac-first installation path | T-10/12 prove clean-install instructions and no paid dependencies; retain exact toolchain/package hashes and measured limits. |
| B8: pilot learning record | B7; three teams sought, two revisions each | Record consented/anonymized observations, export effort, triage time, repeats, failures, and pricing responses. Decide continue/narrow/stop. |
| B9: AI feasibility design | B8; docs plus separately approved bounded experiment | Compare at most two local model/runtime combinations; document license, exact weights/hash, quantization, context, RAM/latency/cost, T-11 quality and abstention. No model downloads in required CI. |

B0a proposes one next experiment, E1: a read-only native metadata ABI probe, only after
separate authorization selects an eligible external target and permits its scratch build.
No such target is currently authorized/provisioned. Requirement decisions D1–D4, storage
evidence and Python/JCS/build compatibility must address the [remaining blockers](decisions/002-storage-protocol.md)
before M0 can close. B1 source-only definitions may use the adopted exception; the customer
path retains its full gates. Candidate versions
are researched, not tested product pins. Model-serving SDK and weights remain deferred
beyond deterministic/pilot gates. Completion of B0a does not authorize E1 or any new task.

## Dependency and release discipline

Keep tasks small enough for one focused PR; combine only when the boundary cannot be tested
independently. Never trade an unknown outcome for an easy green test. Release candidates
require passing product checks once implemented, coordinator acceptance, then owner approval
under [development](development.md). Product implementation PRs require separate authorization.
No date or throughput commitment follows from the Mac's observed hardware configuration.
Any paid service, broader authority, multi-user storage, or live tool execution is a new scope
decision, not an incidental adapter. Deferred items remain out of the critical MVP path.

## Planning issue acceptance map

This table records the original issue #5 planning delivery. The adopted synthetic-only
ordering above supersedes its blanket pre-M0 sequence; original customer milestone exits stay.

| Issue #5 criterion | Documentation / delivery evidence |
| --- | --- |
| A1 users/workflows/requirements | product.md, RL-001–014, explicit pilot/pricing hypotheses. |
| A2 architecture/contracts/errors | SDD, evidence-contract.md, pending ADRs, nonexistent-interface labels. |
| A3 ordered bounded work | M0–M5 and B0–B9 above; B1 initial implementation task after gates. |
| A4 product verification/cost | testing.md, tri-state/effect/coverage matrix, unmeasured targets. |
| A5 operations/storage/recovery | operations.md; current Mac/pendrive split and future routing distinguished. |
| A6 exact-revision approval | Coordinator-owned AGENTS/development updates; owner decision and delegated-submission disclosure in PR record. Workers cannot self-approve. |
| A7 links/checks/history/SHA | README and local validation; coordinator stages drafts, reruns tracked checker, records pushed SHA/review timeline and verifies PR CI. |

The issue #5 planning delivery is recorded in merged PR #6. Subsequent B0 findings and
worker delivery evidence belong to #10's PR; the coordinator independently verifies them.
Approval of a changed head requires a fresh exact-revision decision.
