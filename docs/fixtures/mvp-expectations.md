# B1: contract-derived expectations

Status: author draft for independent coordinator review, not an evaluator-produced golden.
Definitions: [eight source cases](mvp-cases.md). Authority: [evidence contract](../evidence-contract.md).
This document reasons from that contract before implementation; it reports no executed T-01–06,
runtime/JCS/new N2/N4 validation, deadline enforcement, ten-run result or usability observation.

## Fixed eight-row oracle

Each case has one assertion a1. Baseline has eight complete runs; candidate has seven complete
runs and no C07 run. All present Run.error_code values are null, including candidate C05.

| Case | Alignment | Baseline presence / run status | Baseline a1 / case | Candidate presence / run status | Candidate a1 / case | Delta |
| --- | --- | --- | --- | --- | --- | --- |
| C01 | matched | present / complete | pass / MATCH | present / complete | pass / MATCH | unchanged |
| C02 | matched | present / complete | pass / MATCH | present / complete | fail / MISMATCH | regression |
| C03 | matched | present / complete | fail / MISMATCH | present / complete | pass / MATCH | improvement |
| C04 | matched | present / complete | pass / MATCH | present / complete | unknown / MISSING_EVIDENCE | incomparable |
| C05 | matched | present / complete | pass / MATCH | present / complete | unknown / INELIGIBLE_EFFECT | incomparable |
| C06 | matched | present / complete | pass / MATCH | present / complete | unknown / INELIGIBLE_EFFECT | incomparable |
| C07 | missing_candidate | present / complete | pass / MATCH | missing / null | unknown / MISSING_CASE | incomparable |
| C08 | changed_definition | present / complete | pass / MATCH | changed / complete | unknown / CHANGED_CASE | incomparable |

Statuses/reasons in the a1/case columns describe a1; each case inherits its sole assertion's
status. Case objects have no invented reason field. C08 baseline still matches the authoritative
hash, while candidate is changed. Whole-row changed_definition does not make baseline changed.
C05 completion error is not Run.status error: the present ineligible effect gives INELIGIBLE_EFFECT,
not RUN_ERROR. C07 missing and C08 changed precede any assertion evaluation on those sides.

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

## Completion boundary for this draft

Next checkpoint adds exact namespace-qualified citations, per-case clause/source/time proof,
hash dependency explanation and attached variant expectations. Counts above are documentary
arithmetic, not computed golden hashes or test results. Independent review remains pending.
