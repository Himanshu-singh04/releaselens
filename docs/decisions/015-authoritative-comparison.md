# B4: authoritative alignment and comparison

2026-11-23; issue38; GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode persistent worker.
Status: implemented and locally tested; independent coordinator review pending. $0 new spend.
[Fixed A1–A6](https://github.com/Himanshu-singh04/releaselens/pull/37#issuecomment-7094112711)
and [founder authorization](https://github.com/Himanshu-singh04/releaselens/pull/37#issuecomment-7094223905)
authorize bounded implementation/test/fix cycles. Briefing UTF-8 SHA256 verified exactly:
`152b4eb17e5906a2c341759e99e2adc4c5760f4b71b5958047db4863425f7df9`.
Base `365229b5cc43f455c1a0280b4865388c7bacaaf6` is accepted B3; reviewed/merged tree
`f4542112f33d31f0b79bfa1821ce4646d2b7d313` matches. Branch `feat/b4-alignment-comparison`.

## Pure boundary

[`comparison.compare(suite, baseline, candidate, evaluator_version)`](../../releaselens/comparison.py)
accepts already Contract-validated normalized documents. It returns the existing SDD
`{ok:true,value:Result}` / `{ok:false,error:Diagnostic}` envelope. This is not a decoder or
import API. B2 Contract and B3 evaluator remain byte-identical; comparison directly reuses
their pure helpers and adapts B3's internal diagnostic to fixed null-location E_INTERNAL.
The fixed message is `Comparison failed.`; nested/internal exceptions discard all partial
work. Small guards reject empty/duplicate/malformed sets, invalid own-run bindings, malformed
nested outcomes and invalid returned hash shape; they do not replace Contract validation.

Both embedded suite IDs must equal authority; baseline is checked first. Incompatibility
returns fixed E_SUITE (`Incompatible suite identifier.`) at that owner's
`/suite_snapshot/suite_id`, without a Result. Compatible suite revision/hash differences do
not reject unchanged case hashes. Evaluator version is an explicitly supplied valid JSON
string, included verbatim in identity; invalid types/Unicode return E_INTERNAL. No ambient
version, I/O, clock read, randomness, model/event execution, or input mutation occurs.

## Alignment, counts and identity

Exactly the authoritative cases form rows and denominators. A missing run synthesizes
MISSING_CASE for every authoritative assertion, even with a changed snapshot definition.
A present mismatching case hash synthesizes CHANGED_CASE with authoritative IDs/cardinality,
retaining that run's ID/status. Matching runs use B3 independently; a matching side still
evaluates when the other is changed. Whole-row changed_definition precedes missing labels;
otherwise missing_both/baseline/candidate precede matched. Missing/changed causes precede
run-status reasons, while changed error/timeout/skipped status contributes overlapping counts.

Matched pass→fail is regression, fail→pass improvement, equal determinate statuses unchanged;
all unknown pairs and every unaligned row are incomparable. aligned_pairs includes matched
unknown/error runs. Case/assertion Counts partition authoritative expected sets by tri-state;
missing/changed and error/timeout/skipped overlap, weighted by authoritative assertion count.
Extras are sorted run case IDs outside authority; their own embedded assertion cardinalities
contribute only to extra counters. Snapshot-only definitions without runs are not extras.
Extras do not alter expected-set verdicts, denominators or run-status counters.

Rows/outcomes/extras follow contract ordering; B3's exact owner/ref/hash-bound citations and
UTF-16 ordering/full-citation deduplication remain intact. Result contains exactly the existing
schema1/version/input semantic hashes/rows/extras/case and assertion counts/aligned_pairs/hash.
`result_hash` uses existing Contract RFC8785 hashing, excluding only itself. No stored ratio,
coverage-loss, gap, aggregate-status or delta-total fields; these derive from retained rows.
No generated_at, Report, raw-byte hash or persisted output. Returned collections, including
nested citations, are independent of inputs under mutation in either direction.

## Clause-authored T-05/T-06 tests

[`tests/test_comparison.py`](../../tests/test_comparison.py) was written from contract
177–205/220–240/255–259, testing R4 and B1 paper tables before observing compare output.
Expected rows/sides/status/reason/citations/counts/deltas are handwritten. Citation and Result
hashes use the unchanged independent stdlib restricted-JCS B2 recipe, not evaluator output
or Contract hashing as the sole oracle. Small test-only definitions remain within that
recipe's supported domain; affected identities are independently resealed and Contract must
accept each semantic input. Duplicate attempts instead assert the exact Contract rejection.

The16 methods cover the full eight-row oracle, all nine pairs, every missing/changed side
combination, both-empty runs, changed+missing precedence, unequal authoritative/old/extra
assertion sets, changed run-status overlap, compatible suite-hash differences/incompatible
IDs, snapshot-only cases, extras on either/both sides, matching error/timeout/skipped, all
multi-assertion aggregation modes, complete Counts conservation, R4 three-case gaps plus
TYPE_MISMATCH and missing/changed exclusions, ten identical comparisons, independent hashes,
version-only identity, raw object-order/whitespace and source-array-order controls, sorted
rows/outcomes/extras, namespace collision/binding, input/return mutation isolation and
redacted nested/evaluator/hash failures. Malformed caller/nested-result tests intentionally
violate preconditions to exercise fixed internal failure rather than semantic unknown.

Fixed counts: baseline7 pass/1 fail/0 unknown; candidate2 pass/1 fail/5 unknown, expected8
each; candidate missing1/changed1; extras0; aligned_pairs6. Derived deltas1 regression/
1 improvement/1 unchanged/5 incomparable; case/assertion coverage8/8 and3/8. Candidate gaps
MISSING_EVIDENCE1/TYPE_MISMATCH0/INELIGIBLE_EFFECT2 exclude MISSING_CASE/CHANGED_CASE. These
are reproducible imported-evidence comparisons, not authenticity, usability or causal proof.

## Retained execution and preservation

Fresh [`experiments/b4/check.py`](../../experiments/b4/check.py) launches only the fixed B4,
B3 and B2 test entry points. No historical driver or expired supervisor is imported/executed.
It verifies retained base/cache inventories before/after, snapshots exact source/argv/env/
clock, supervises300s/process and1MiB/stream, counts all fresh B4 evidence/scratch against
256MiB and reserves300s beyond invocation allowance for delivery. Sanitized HOME/tmp/cache/
config are under `/Volumes/AIWorkspace/caches/releaselens/b4-comparison/`; attempts in
`artifacts/b4/`. No local acquisition/install/repair/replacement interpreter occurred.

Host Python3.13 `-I -B experiments/b4/check.py LABEL comparison|evaluator|contract` launches
retained `/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python`
with `-I -B` and the corresponding `tests/test_comparison.py`, `test_evaluator.py` or
`test_contract.py`, from the repository root.

| Attempt | Retained-runtime outcome | Supervised process | stdout/stderr |
| --- | --- | --- | --- |
| comparison-1 |15 tests passed0.539s |0.953s |0B/2537B |
| evaluator-1 |21 unchanged tests passed0.397s |0.669s |0B/3294B |
| contract-1 |22 unchanged tests passed22.441s |22.723s |0B/3096B |
| comparison-2 |16 tests passed0.581s |1.072s |0B/2711B |

All exit0, no stop reason/signals. Revision2 adds defensive malformed nested-outcome/hash
guards and their fault tests; both revisions remain retained. No failed target attempt.
B2 boundary recipes remain serial<=25MiB+1; semantic documents are checked<150000B each.
CI preserves baseline/B2/B3 checks and adds bounded B4 execution reusing its verified wheel/
venv:180s timeout+2s grace,1MiB output files, fresh sanitized B4 task dirs. Hosted results are
separate from exact Mac evidence; final policy/CI/attribution outcomes are in the PR handoff.

Before edits14 historical manifests/3324 entries,2139 prior raw files including later B3
coordinator records, all12 source bindings and retained inventories verified. Old refs and
all four B2 fixtures/encoder/22+21 regressions preserved. Only workflow entries intentionally
changed: prior B2 mappings remain through9e67eb4; B3 workflow entry maps explicitly through
reviewed d8ff5f7. Original four B2 sources still map through3bfc7a. All raw/cache/source
snapshots always use direct hashes; old159-entry B3 seal remains unchanged.

## Clock, history and remaining gates

First-session floor **07:20:41.649686 UTC**, deadline **08:20:41.649686 UTC**; all reads,
edits/tests/checks/CI/recovery/delivery count. Full3600s charge; at most one separately
dispatched3600s correction reserved within7200s. No reset/self-dispatch. Coordinator
reconciles durable admission/final idle independently; no denied registry path retry.

Before the first source edit, actual history recorded transport WebSocket1000, retry-attempt2
and synthetic continuation. Authorized native same-provider recovery retained the original
clock. No manual provider retry/switch/paid fallback/bypass/config/service change. Full
history cutoff and explicitly unaudited closing interval are recorded at handoff.

B3 admission06:25:23.577/serialized06:25:23.603/final idle06:46:17.262 UTC and elapsed
1307.612418s were resolved additively by coordinator;43 messages/54 calls had no provider
event. Original unknown-at-handoff records stay intact; B3's unused correction reserve closed.

Ten pure comparisons establish Result reproducibility only. Original60-second whole-comparison
completion remains unproven; development suite timeouts do not replace it. Blocking terminal
I/O/scheduling still requires review before presentation implementation. No terminal/demo
acceptance, renderer/CLI, customer/path import, Store, persisted Report, packaging, native/
storage work, outreach or AI. D1–D4 remain unadopted. Stop for independent coordinator review;
approval/merge or a subsequent task requires separate authority.
