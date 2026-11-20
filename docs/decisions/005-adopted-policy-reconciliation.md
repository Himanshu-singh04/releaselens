# B0d: adopted policy and synthetic-scope reconciliation

Status: founder decisions adopted; **this normative reconciliation awaits review/merge**.
Date: 2026-11-20. GPT-6 Astra (`gpt-6-astra`) / OpenCode, same persistent worker; no subagents.
[Issue #18](https://github.com/Himanshu-singh04/releaselens/issues/18) fixes A1–A6 and authorizes
documentation only, from approved main `90f77fd2906e29f3bb30850d19cf91730f3c5214`.

## Exact authority and historical status

- [Numeric adoption](https://github.com/Himanshu-singh04/releaselens/pull/17#issuecomment-7032357769):
  founder replied “ok proceed” to the sole N1–N4 request. Exact adopted source:
  [B0c A2 L34–101](https://github.com/Himanshu-singh04/releaselens/blob/90f77fd2906e29f3bb30850d19cf91730f3c5214/docs/decisions/004-mvp-decision.md#L34-L101).
  This includes replacement N2 normalization and expanded N4 artifact accounting.
- [Scope/sequence adoption](https://github.com/Himanshu-singh04/releaselens/pull/17#issuecomment-7032673526):
  founder replied “ok proceed” to the sole synthetic-terminal scope/sequence request, limited
  immediately to one reconciliation PR. Exact source at that same revision: A1 L13–32,
  exception L214–220, conditional runtime/AI deferral L188–218/L248. This assent approves
  neither this PR nor later implementation. No founder decision awaits an answer at dispatch.
- B0/B0a/B0b research and the B0c packet are accepted records, not completed product gates.
  Their bodies remain historical, including rejected alternatives, lexical N2 findings and
  B0c's recommendation to adopt D1–D4. **D1–D4 were not adopted.** B0c's generic “ok proceed”
  caveat describes earlier consent; it does not negate these later, specifically scoped decisions.
- Adoption establishes requirements; it does not prove enforcement. B0b's 105 finite controls
  on CPython 3.13.4 do not validate replacement N2 or expanded N4. Target CPython 3.14.10
  standard GIL / rfc8785 0.1.4 remains conditional, uninstalled/unqualified as a product stack.
  Local 3.13.4 and CI 3.14.4 observations are not target qualification. M0/M1–M4 stay incomplete.

## Reconciliation boundary

The active documents below reconcile only adopted decisions. B0–B0c bodies remain byte-identical;
read their review-time pending/NO-GO statements as historical context, with this addendum recording
later adoption. No fixture definitions/encoding, source, experiments, installs or target changes.

## Old-to-new clause and file trace

Old line numbers refer to approved base `90f77fd2906e29f3bb30850d19cf91730f3c5214`.
Packet source clauses refer to that same fixed revision, not moving line numbers in this PR.

| Adopted source / old active clause | Reconciled location and exact effect |
| --- | --- |
| B0c A2 N1 L44–54; contract L17 “integers must be safe and fractions finite IEEE-754 values” | [Contract encoding](../evidence-contract.md#encoding-identifiers-and-provenance): exact mathematical integral token safety before conversion, rounded integral/nonfinite rejection afterward; [testing numeric oracles](../testing.md#adopted-numeric-and-boundary-oracles-unperformed), N1/T-01, retains exact five accept/reject examples. |
| B0c replacement N2 L56–73; contract L16 Scalar, L73–74 exact equality | Contract encoding and assertion equality: safe integral binary64 values normalize to int after N1/N3, integer tokens retain exact safe int, boolean stays distinct, nonintegral values are not Scalar. Applies to JSON/expected/actual/subjects/integer fields. Testing N2/T-01/03/06 copies 1/1.0/1e0/true/1.5/1.0000000000000001 and reparse oracles. [SDD gotchas](../specs/001-mvp/solution-design.md#implementation-gotchas) points to the same order. |
| B0c N3 L75–82; contract L17 finite-fraction clause | Contract encoding: reject nonzero-to-zero underflow; accept finite nonzero subnormal rounding/signed zero. Testing N3/T-01/06 retains 1e-400 rejection, 5e-324 nonzero, -0.0 → 0. No exact-decimal promise. |
| B0c N4 L84–101; contract L9 and L243–247 byte/depth bounds | [Contract bounds](../evidence-contract.md#versioning-and-bounds): BOM rejection, container depth root 1/primitive 0/max 32, MiB 1048576, raw input/content-token and decoded artifact-array accounting inclusive. Testing N4/T-01/08 copies boundary/one-over/string/UTF-8/escaped/BOM/embedded-array/20 MiB oracles. Existing count/size ceilings and original deadline stay. |
| B0c A1 L13–32; PRD L29–47 first file-based workflow | [Product scope/workflow](../product.md#agreed-constraints-and-proposed-scope): adopted bundled terminal journey; customer workflow labeled separately. [Contract report section](../evidence-contract.md#proposed-report-shape-and-persistence) distinguishes same Result/citation semantics from customer Report/persistence. All schema fields/version literals unchanged. |
| B0c A1 finish line; existing T-06/07/10 and SDD UI/acceptance | [Testing demo criteria](../testing.md#synthetic-terminal-demo-acceptance-unperformed), PRD and SDD UI/acceptance: eight rows incl. missing/changed, fixed baseline/candidate, outcomes/deltas/reasons/citations/coverage, control escaping, ten identical hashes and independent explanation. Unperformed; not full RL-008/011/T-07/09 or customer usability. |
| B0c exception L214–220; PRD L31, roadmap L17–26/L39–55, SDD L88/L370–371 blanket pre-M0 gates | [Roadmap](../roadmap.md#ordered-milestones) carries the exact exception; PRD constraints and [SDD boundaries](../specs/001-mvp/solution-design.md#implementation-boundaries) apply it. B1 source-only definitions can precede M0 after prerequisites/permission; later pure slices need scoped runtime/JCS validation. Customer B2–B9 dependencies stay gated; milestones remain incomplete. |
| B0c scope exception; SDD external/internal interfaces, component/runtime/deployment views | SDD labels customer Files/Importer/Store/Report/summary interfaces and adds bundled pure-value/terminal flow. No path imports, Store, persistence, release package or executable demo grammar. [Operations boundary](../operations.md#adopted-synthetic-terminal-boundary) distinguishes public synthetic source from customer-private I/O. |
| B0c L188–218/L248 conditional runtime and AI deferral; operations L39–50, roadmap L24–25, SDD ADR-1/5 | Operations/PRD/SDD use conditional standard-GIL CPython 3.14.10 + rfc8785 0.1.4; target/build/installer remain unqualified/unselected, no acquisition authority. SDD ADR-5 records deferral only as confirmed; operations/testing/roadmap defer AI beyond deterministic/pilot gates. No other whole ADR closes. |
| B0c D1–D4 recommendations L103–176; no adoption | Existing customer contract/publication, operations startup/recovery, testing R5/R7 and SDD fatal/error/deadline wording retained. Explicit feasibility blockers below; no observed-only detection, late-marker allowance or decision budget becomes normative. |
| Historical decision status and README navigation | This new addendum plus README/active-document status links distinguish accepted research, adopted policy, pending normative merge and unverified enforcement. No historical evidence body or 55-heading SDD structure changes. |

## Retained guarantees and next gates

D1–D4 remain proposals only. R5 private access/ACL-drift rejection, R7 continuous identity/loss
failure, fatal-error marker absence, no-redirection/no-fallback and the 60-second comparison
deadline retain their current meaning. B0a C1–C4 remain customer-path feasibility blockers;
the existing noowners mount is ineligible and no eligible target or E1 is authorized.
The synthetic exception does not relax the 60-second obligation. Blocking terminal I/O and
scheduling still leave hard completion unverified; do not infer D4's decision-budget semantics
or permission to implement an unbounded demo. Any unresolved enforcement conflict must return
to review before a later implementation authorization; it cannot be silently waived here.

Preserved-gate audit (requirements, not passing results):

| Gate | Retained obligation and blocker |
| --- | --- |
| Privacy / D1 not adopted | Testing R5 still requires ACL drift not expose evidence or publish successfully; operations still requires owner-private creation, empty probes and ACL/owner checks. B0a C1 exposes the unsolved transient-drift schedule. |
| Identity / D2 not adopted | Testing R7 retains failure/no-success around replacement/unmount and retained-handle identity; operations keeps no path reopen/fallback. B0a C2 continuous binding and availability-to-acknowledgement remain unresolved. |
| Fatal marker / D3 not adopted | SDD E_LIMIT still says “Exit 4; no complete marker”; UI states fatal errors exit without one. RL-011/contract completion integrity/no overwrite remain. B0a C3 late failure conflict remains; no recoverable-marker exception adopted. |
| Deadline / D4 not adopted | Contract still requires runtime independently enforce a 60-second comparison deadline; SDD Q4 and testing hard-limit language remain. Applies to demo; B0a C4 and R1 interruption caveats remain unresolved evidence, not replacement semantics. |
| Target/native/package | Current noowners storage stays ineligible for customer I/O. No eligible target selected, E1 authorized, native ABI/flush/privacy tested, build/installer pin qualified, package or pilot delivered. Source-only synthetic permission does not supply any of these. |

All contract shape tables, evidence eligibility/tri-state/alignment rules, customer publication
paragraph and testing R5/R7 obligations remain unchanged, except the adopted normalization's
application to exact-type equality. New prospective vectors are documentation only; no corpus
rerun or product enforcement result is part of B0d. Required foundation CI may run unchanged
historical research controls automatically; those results do not validate new numeric policy.

Next: review/approve/merge this exact reconciliation, then separately request the eight-case
source-only fixture-specification slice. Later pure work needs scoped runtime/JCS validation,
new N2/N4 validation and its own implementation permission. Native/storage/build/package/pilot
gates remain for the customer product. AI stays deferred beyond deterministic/pilot gates.
This task creates no next issue, authorizes no follow-up, and stops for coordinator review.
