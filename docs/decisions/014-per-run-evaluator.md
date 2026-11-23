# B3: pure per-run value and effect evaluator

2026-11-23; issue36; GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode persistent worker.
Status: implemented and locally tested; independent coordinator review pending. $0 new spend.
[Fixed A1–A6](https://github.com/Himanshu-singh04/releaselens/pull/35#issuecomment-7093230949)
and [founder authorization](https://github.com/Himanshu-singh04/releaselens/pull/35#issuecomment-7093299676)
permit bounded implementation/test/fix cycles. Base `c84063097abca509cbde0e93a44131f6a34cc0dc`
is accepted B2, with the same tree as reviewed `9e67eb41242a8611dad9301225c52b3ad3fd6bb8`.
Branch: `feat/b3-value-effect-evaluator`. Earlier research and B2 clocks remain closed.

## Boundary and rules

[`evaluate_run(bundle, run_id, owner)`](../../releaselens/evaluator.py) is an internal pure
primitive over **Contract-validated normalized Bundle values**. Owner is baseline/candidate;
the selected run binds to its own embedded case. It returns the existing present Side and
one Outcome for every assertion, without adding schema/version fields. It does not decode or
rehash inputs. Small invariant guards reject missing runs, mismatched case bindings, empty or
malformed assertion sets, duplicates and unsupported run states as fixed null-location
E_INTERNAL, never vacuous pass. These guards are not a replacement Contract validator.

The evaluator directly reuses Contract's pure `_ref`, `_pointer`, `_time` and `_assertion`
helpers; Contract and its22 tests are unchanged. There is no alternate resolver/decoder,
filesystem/network access, clock read, randomness, event execution or input mutation.
Unexpected internal failures discard the entire Side, including any previously computed
outcomes, and return `Run evaluation failed.` without exception/evidence text.

Run error/timeout/skipped takes precedence over evidence and synthesizes all RUN_* unknowns.
For complete runs, absent Observation or null applicable field gives MISSING_EVIDENCE.
Value equals requires exact Scalar type and value; contains/not_contains use literal,
case-sensitive substrings. Explicit selected JSON null is data. Wrong actual type gives
TYPE_MISMATCH; missing negative evidence never passes. Aggregate fail precedes unknown,
then all-pass, retaining every outcome and unknown.

Effects require the linked successful completion, rule-matching request tool and exact
business_snapshot source tuple, a selected JSON object and two direct Scalar member
selectors. Both selectors contain exactly one RFC6901 token (including correctly escaped
tokens and the empty member name). Rule/request/effect/observed subjects must match by type
and value in that same record. Known completion/effect/capture times must satisfy inclusive
`completion <= effect <= capture` and `capture - completion <= max_age_ms`. Exact timedelta
comparison handles millisecond/day/year rollover without overflowing an added deadline at
year9999. Any present semantic ineligibility gives INELIGIBLE_EFFECT; an eligible value
differs by type or value => MISMATCH/fail, otherwise MATCH/pass. Source/time claims remain
untrusted exporter claims, not authenticity or causation proof.

Determinate values cite exactly Observation.value and its owning bundle artifact hash.
Determinate effects cite observed subject and value in the same artifact, with the selected
entity pointer prefixed to each one-token selector. Unknowns have no citations; no optional
context is emitted. Outcomes sort by assertion_id; full citations sort by owner/container/
artifact_id/pointer (null first)/hash using UTF-16 code units, deduplicating only identical
full citations. Returned citation/ref objects are fresh and cannot mutate input objects.

## Clause-authored tests and retained execution

[`tests/test_evaluator.py`](../../tests/test_evaluator.py) was authored from contract clauses
and the B1 paper tables before any evaluator output was observed. Status/reason/citation
expectations are handwritten, not generated goldens. Fixed baseline C01–C08 and candidate
C01–C06 match their paper tuples. A separately labeled candidate C08 test demonstrates only
its own old definition's local result; authoritative changed/missing alignment remains B4.

Small test-only mutations/definitions use a separate independent restricted canonicalizer:
UTF-16 key order, strings/safe ints/bool/null and exactly nonintegral float1.5. That explicit
subset matches compact stdlib JSON spelling; other floats are rejected by the recipe. The
unchanged B2 encoder's ASCII-key restriction is not silently extended. Artifact/case/suite/
run/bundle identities are independently resealed, then Contract acceptance is required before
semantic evaluation. Invalid reference/time controls stop at Contract; internal-misuse tests
deliberately violate the precondition and expect only E_INTERNAL.

The21 methods cover all approved A4 groups: literal value pass/fail/type/null/missing/nested
selection and N2/JCS reparse; request/completion-only and failed completion; source/tool and
each subject claim; transcript/tool-return/nonobject/array/selector ineligibility; same-record
anti-splicing with exact fail/pass record citations; absent times and inclusive/one-ms-over
freshness; invalid structural links/times/refs; run precedence and multi-assertion aggregation;
escaped/nested/empty-member pointers; UTF-16 citation order/full-key dedup; cross-owner and
snapshot collisions/exact observation binding; repeated calls/input immutability/return-value
mutation; fixed internal diagnostics, including failure after a successful first assertion.
Citation comparator-only vectors test ordering/dedup, not renderer resolution/publication.

Fresh [`experiments/b3/check.py`](../../experiments/b3/check.py) supervises only the new B3
evaluator suite and unchanged B2 suite. It imports no old driver or supervisor. It verifies
retained base/cache inventories before and after, snapshots sources/argv/environment/clock,
captures1MiB/stream with300s process ceiling, samples total B3 allocation below256MiB, and
reserves300s beyond the invocation ceiling for delivery. Sanitized HOME/tmp/cache/config are
under `/Volumes/AIWorkspace/caches/releaselens/b3-evaluator/`; immutable attempts are in
`artifacts/b3/`. No install/bootstrap/repair/replacement interpreter occurred.

Approved host Python3.13 `-I -B experiments/b3/check.py LABEL contract|evaluator` launches:

```text
/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python -I -B /Volumes/AIWorkspace/projects/releaselens/tests/test_evaluator.py
/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python -I -B /Volumes/AIWorkspace/projects/releaselens/tests/test_contract.py
```

First evaluator run:21 tests0.387s, process0.696s, exit0. Unchanged B2:22 tests24.496s,
process24.779s, exit0. Additional explicit effect bool/int mismatch and late internal-fault
assertions then passed in evaluator revision2: **21 tests0.422s**, process0.757s, exit0.
All three runs: stdout0B, stderr3294B/3096B/3294B, no stop reason or signals. Both evaluator
test revisions and results remain retained; no failed target attempt occurred. B2 boundary
recipes remain serial, <=25MiB+1/input; new semantic documents are checked below100000B.
CI preserves inherited checks and adds bounded evaluator execution using its existing
hash-verified wheel/venv; fresh task directories,180s plus2s kill grace,1MiB output-file limits.
Hosted results are distinct from exact Mac evidence. Final policy/CI/attribution results
and sealed preservation/history/clock identities are recorded in the PR handoff.

## Preservation, clock and remaining gates

Before edits all13 historical manifests/3165 entries and2030 existing raw evidence files
were verified, including later coordinator records. All nine approved source hashes matched.
Four B2 fixture files, source encoder, Contract and22 B2 tests remain unchanged. Prior refs
are retained. Original historical mappings remain exact; changed workflow entries covered
by B2 seals map explicitly to their identical reviewed9e67eb4 blob, while the original four
B2 source mappings still use3bfc7a. Raw/cache/source snapshots always use direct hashes.

B2 acceptance resolved its earlier metadata statements additively: final correction admission
04:41:54.259 UTC, serialized04:41:54.376, idle04:55:54.725, elapsed883.405265s, full3600s
charged; coordinator audited31 messages/43 calls with no session2 provider event. Original
denied-read/unknown-at-handoff records remain intact. No registry path was retried.

B3 session1 charged floor **06:24:29.649582 UTC**, deadline **07:24:29.649582 UTC**. All reads,
edits/tests/checks/CI/delivery/recovery count; full3600s charge, at most one separately
dispatched3600s correction reserved within7200s total. Coordinator independently reconciles
durable admission/final idle; the earlier floor controls. No self-dispatch. Native same-provider
connection recovery only as authorized, with actual history audit/cutoff and closing interval
disclosure at handoff; quota/rate/auth/billing errors stop. No config/service changes.

B4 alignment, missing/changed sides, deltas/counts/Result identity, renderer and full T-05/T-06
remain unimplemented. This is not an authoritative cross-suite verdict or readiness claim.
Original60-second whole-comparison obligation remains unproven; development suite limits do
not replace it. Blocking terminal I/O/scheduling still needs explicit review before later
demo implementation. D1–D4 remain unadopted. No customer/path import, Store, persisted report,
packaging, native/storage work, outreach or AI. Stop for independent coordinator review;
approval/merge and any subsequent task require separate authority.
