# Proposed roadmap and bounded backlog

Draft for [issue #5](https://github.com/Himanshu-singh04/releaselens/issues/5); no milestone
below is delivered. Dependencies are gates, not calendar promises. Scope is in the
[PRD](product.md), contracts in the [SDD](specs/001-mvp/solution-design.md), tests in
[testing](testing.md), and local execution/recovery in [operations](operations.md).

## Ordered milestones

| Milestone | Depends on | Observable exit evidence | Exclusions |
| --- | --- | --- | --- |
| M0: confirm design | Current documentation PR | Owner decision on exact revision, ADR-1–5 resolved, independent consistency review, foundation checks and PR record. | No runtime code or provisioning. |
| M1: deterministic contract fixtures | M0; runtime/schema decisions | Reviewed synthetic refund/escalation corpus; parser/hash/reference rejection vectors; T-01/02 pass. | No agent calls or AI. |
| M2: baseline/candidate evaluator | M1 | Golden tri-state/effect/alignment results; T-03/04/05/06 pass with all expected cases retained. | No vendor adapter. |
| M3: local report and recovery | M2 | Offline HTML/JSON parity; inert rendering, bounded resources, interruption recovery; T-07/08/09/12 pass. | No server/accounts/billing. |
| M4: narrow pilot and packaging | M3 | Reproducible local package, version/provenance record, observed onboarding, six comparison sessions sought; T-10 evidence. | No claim that recruitment targets are demand. |
| M5: optional grounded AI investigation | M4 evidence plus new approval | Primary-source runtime/model/license research, measured local fit, held-out T-11 results, authority/cost decision. | No autonomous business effects or automatic shipping. |

If M0 approves deferral of AI, ADR-5 is resolved for MVP only; M5 still needs its own design
approval. No unresolved runtime/schema/packaging ADR may be bypassed to “start scaffolding.”
An owner may reject or change proposals; update dependent docs and obtain fresh revision review.

## Issue-ready task slices

Each row is a proposed issue, not an already-created GitHub issue. Every implementation PR
must carry a bounded scope, requirement IDs, expected test outcomes, and review evidence.

| Task | Dependency / scope cap | Acceptance and verification |
| --- | --- | --- |
| B0: close design gates | Now; documentation only | Record runtime/language, exact dependency pins or explicit investigation outcomes, schema/evaluation/resource decisions, and AI deferral. Coordinator/owner review M0. |
| B1: fixture vocabulary | M0; 8 synthetic cases, <=3 assertions each | Include eligible refund, ineligible refund, escalation, missing observation, failed completion, stale effect, removed case, changed policy. Lead reviews expected outcomes independently; no customer data. |
| B2: import/identity boundary | B1; Suite/Bundle only | Implement chosen schema and hash validation with malformed, duplicate, dangling-ref, and source-version tests T-01/02. No renderer/evaluator. |
| B3: value and effect rules | B2; three operators and one effect chain | T-03/04 verify exact tri-state semantics, time/source eligibility, and negative assertions. No fuzzy semantic judge. |
| B4: alignment and deltas | B3; one attempt/case/bundle | T-05/06 verify expected-set denominators, changed hashes, all nine outcome pairs, extra/missing rows, and reproducible result hash. |
| B5: offline report | B4; one HTML/JSON layout | T-07 verifies shared Result, escaped evidence, inspectable references, zero external requests, and keyboard navigation. |
| B6: publication and limits | B5; one local output lifecycle | T-08/09 cover deadline/size boundaries, partial writes, output collision, missing mount, and recovery without overwrites. |
| B7: package and pilot guide | B6; Mac-first installation path | T-10/12 prove clean-install instructions and no paid dependencies; retain exact toolchain/package hashes and measured limits. |
| B8: pilot learning record | B7; three teams sought, two revisions each | Record consented/anonymized observations, export effort, triage time, repeats, failures, and pricing responses. Decide continue/narrow/stop. |
| B9: AI feasibility design | B8; docs plus separately approved bounded experiment | Compare at most two local model/runtime combinations; document license, exact weights/hash, quantization, context, RAM/latency/cost, T-11 quality and abstention. No model downloads in required CI. |

Initial bounded task after approval is B1, not a complete application scaffold. If ADR-1
needs additional investigation first, B0 remains documentation research; do not write product
code under a provisional runtime choice. Package manager, JSON parser/JCS library, compiler,
model-serving SDK, and model weights have not been selected, installed, or benchmarked here.

## Dependency and release discipline

Keep tasks small enough for one focused PR; combine only when the boundary cannot be tested
independently. Never trade an unknown outcome for an easy green test. Release candidates
require passing product checks once implemented, coordinator acceptance, then owner approval
under [development](development.md). Product implementation PRs require separate authorization.
No date or throughput commitment follows from the Mac's observed hardware configuration.
Any paid service, broader authority, multi-user storage, or live tool execution is a new scope
decision, not an incidental adapter. Deferred items remain out of the critical MVP path.

## Planning issue acceptance map

| Issue #5 criterion | Documentation / delivery evidence |
| --- | --- |
| A1 users/workflows/requirements | product.md, RL-001–014, explicit pilot/pricing hypotheses. |
| A2 architecture/contracts/errors | SDD, evidence-contract.md, pending ADRs, nonexistent-interface labels. |
| A3 ordered bounded work | M0–M5 and B0–B9 above; B1 initial implementation task after gates. |
| A4 product verification/cost | testing.md, tri-state/effect/coverage matrix, unmeasured targets. |
| A5 operations/storage/recovery | operations.md; current Mac/pendrive split and future routing distinguished. |
| A6 exact-revision approval | Coordinator-owned AGENTS/development updates; owner decision and delegated-submission disclosure in PR record. Workers cannot self-approve. |
| A7 links/checks/history/SHA | README and local validation; coordinator stages drafts, reruns tracked checker, records pushed SHA/review timeline and verifies PR CI. |

The temporary documentation specialist does not commit, push, mutate GitHub, or provision
workers. This file does not claim A6/A7 remote delivery is complete; coordinator records
those outcomes after review. Approval of a changed head requires a fresh exact-revision decision.
