# B0c — minimum demo and founder decision packet

Status: **recommendation only; no requirement adoption or implementation authorization.**
Date: 2026-11-20. GPT-6 Astra (`gpt-6-astra`) / OpenCode, persistent worker; no subagents.
Base: `b271ec1f19f3f4a67ef9dd2279af129334c322b1`; [issue #16](https://github.com/Himanshu-singh04/releaselens/issues/16), A1–A6.
First-cycle deadline: 07:15 UTC. This packet reuses repository evidence; no new external sources.

## Decision in one paragraph

Recommend a **bundled-synthetic, terminal-report demo**, then the separately gated customer
product. Approve N1–N4 for predictable numeric inputs and D1–D4 for honest storage claims;
explicitly permit fixture/pure-computation work before native storage qualification.
Keep CPython 3.14.10 standard GIL / rfc8785 0.1.4 as the conditional product direction.
Do not select a drive, install tooling, start E1, or declare M0 complete by adopting this packet.
The first separately authorized slice should be eight reviewed synthetic fixture definitions
and expected outcomes, not a publisher. Exact replacements and the next-issue contract follow.

## A1 — journey and observable finish line

The engineer selects the bundled refund-policy example, compares its fixed baseline and
candidate, then reads a local terminal table: case, both outcomes, delta, reason, citations,
and expected-suite coverage. No user-supplied path or customer evidence is accepted by this demo.
The candidate has a real synthetic regression and a request-only “refunded” claim; the engineer
must distinguish the regression from missing evidence and identify the relevant record.
Finish: all eight reviewed rows appear, including missing/changed cases; ten identical
comparisons yield the same Result hash; an independent reviewer explains the regression and
coverage loss from the report without author interpretation. Record failures, not a usability claim.

Required: exact Scalar rules; pass/fail/unknown; request ≠ completion ≠ independently sourced
effect; same-record subject/value binding, source/time eligibility; authoritative-suite
alignment, stable reason codes, counts, deterministic ordering/hashes and resolvable citations.
An eligible mismatching business value fails; request-only, failed completion, stale evidence
or wrong subject stays unknown. A missing negative observation cannot pass `not_contains`.
Hashes bind imported claims, not exporter honesty. This demo does not run a support agent.

Deferred: arbitrary imports, durable generations/marker/recovery, offline HTML/JSON package,
installer/pilot, adapters, database, server, AI explanations and live actions. Terminal output
is a synthetic demonstration report, not the RL-008/011 published-report contract. Public
synthetic source may remain on the existing checkout; this is no customer-storage exception.
Useful feedback: can an engineer understand effect gaps and changed-case coverage before we
spend effort on native publication? It tests presentation/semantics, not demand or policy truth.

## A2 — numeric decisions (exact proposed wording; not applied)

The authoritative [contract](../evidence-contract.md) and [tests](../testing.md) remain unchanged.
The next revision will enumerate N1–N4 replacements, examples and compatibility consequences.
Accepted [B0b](003-json-conformance.md) evidence is finite: 105 controls on CPython 3.13.4,
not general conformance, product pins or qualification of the uninstalled 3.14.10 target.

## A3 — storage decisions (exact proposed wording; not applied)

The next revision will enumerate D1–D4 replacement wording and revised failure oracles against
[B0a G1–G9/C1–C4](002-storage-protocol.md#counterexamples-and-separate-founder-decisions).
Current `noowners` storage remains ineligible. Only a separately selected, owner-enabled local
external APFS target with owner-private objects could enter qualification; none is authorized.
Stable-owner privacy, pinned-handle no-redirection, immutable generations and verified recovery
remain required. No sampled protocol proves continuous ACL/identity history or bounded syscalls.

## A4 — runtime and sequencing recommendation

Retain the exact conditional [B0 runtime direction](001-runtime.md#candidate-pins-acquisition-and-reproducibility):
CPython 3.14.10 standard GIL on arm64 macOS, stdlib validation/testing/rendering plus rfc8785
0.1.4, a fresh local venv and later platform-specific wheel containing the narrow C Store bridge.
Target interpreter, build/installer locks, native compatibility and packaging remain unverified.
Existing CPython 3.13.4 research and CI's 3.14.4 observation do not qualify that product target.

Proposed roadmap exception: after explicit adoption and synchronized normative documentation,
authorize B1 synthetic fixture definitions before M0 closes; subsequently consider individually
bounded pure Contract/Evaluator/terminal-renderer slices after runtime/schema validation.
No native bridge is needed for those pure calls. Native work remains necessary for Store and
customer imports/publication. Existing M1–M4 completion criteria are not met by this demo.
This changes the [current ordering](../roadmap.md#ordered-milestones), which forbids bypassing
unresolved runtime/schema/packaging ADRs; it cannot take effect through implication.

## A5 — draft next issue (not created or executed)

Proposed title: `feat: define eight synthetic demo fixtures and independent expectations`.
Readiness: **blocked on explicit founder scope/schema/sequence decisions and their reviewed
normative reconciliation**; no storage provisioning is a prerequisite for source-only fixtures.
Input: accepted contract revision and the eight B1 scenario categories; output: synthetic
definitions plus an independently reviewed expectation table, not an executable comparison.
Proposed files: `fixtures/mvp/` and `docs/fixtures/mvp-expectations.md`; existing B0b stays intact.
Cap: eight cases, at most three assertions each, fixed baseline/candidate and source/timestamp
claims. Include eligible/ineligible refund, escalation, missing observation, failed completion,
stale effect, removed case and changed policy. Exact file/validation acceptance follows below
in the completed packet. No importer, evaluator, renderer, native code, installs or customer data.

## Founder choices and pause branch

After coordinator review, decide separately: (1) this exact documentation revision;
(2) N1–N4; (3) D1–D4 with lost guarantees made explicit; (4) the synthetic-only sequence
exception and runtime direction; (5) authorization of the drafted next slice after prerequisites.
None follows from the earlier “ok proceed”. If the founder retains universal drift/loss
detection, fatal-error marker absence or hard syscall completion, retain storage NO-GO.
Pause customer-product implementation; the single decision that could still permit useful
progress is the explicitly limited synthetic-only exception. No automatic research extension.
