# B2: pure synthetic Contract and encoded B1 fixtures

2026-11-23; issue34; GPT-6 Astra (`gpt-6-astra`, OpenAI) / OpenCode persistent worker.
Status: implemented and locally tested; independent review pending. $0 new spend.
[Approved scope](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7081518899)
and [founder assent](https://github.com/Himanshu-singh04/releaselens/pull/31#issuecomment-7090850659)
authorize implementation and bounded normal test/fix cycles. Base is merged
`dfbbf2a4763dbdc1826ff4482f13d2e310c2b37b`; branch `feat/b2-synthetic-contract`.
Earlier B1 author-draft/encoding-unapproved wording is historical: merged review and this
explicit B2 assent govern. Source specifications and all historical research remain unchanged.

## Interface and scope

[`releaselens.contract.load`](../../releaselens/contract.py) accepts in-memory bytes and
owner `suite`, `baseline`, or `candidate`. Success returns an ordinary caller-owned normalized
`document`, exact input `byte_hash`, and validated `semantic_hash`. Failure returns one bounded
fixed `diagnostic` with a schema-known input location; it never returns a partial document.
These are Python API return values, not new wire-schema fields. No supplied hash is repaired.
No filesystem, network, runtime driver, Evaluator, renderer, Store or report persistence exists
in the module. Stdlib plus retained rfc8785 0.1.4 only; no packaging or new dependency.

Strict decoding rejects BOM, invalid UTF-8/Unicode, duplicate decoded keys, malformed/nonfinite
numbers, exact or rounded unsafe integers, and nonzero underflow. Adopted N2 normalizes safe
integral binary64 values, including signed zero; booleans remain distinct. Numeric handling
adapts reviewed B1d rules without importing historical research code. JSON content uses JCS;
text/source bytes retain exact Unicode and control characters without normalization.

The byte grammar walker discovers actual content token boundaries before value decoding;
it receives no known fixture offsets. Quotes/escapes/internal whitespace count toward1MiB;
outer whitespace counts toward5MiB standalone Suite/25MiB Bundle input limits. Depth counts
the full input, including embedded snapshots. Decoded20MiB totals apply independently to
each artifact array, using text UTF-8 or JSON JCS bytes. Embedded suites enforce their case,
assertion, artifact and decoded bounds inside the containing bundle's raw input bound.

Structural validation covers exact fields/types, literal schema1, IDs/hashes/UTC-millisecond
times, cardinalities/uniqueness, source tuples/provenance, namespace-local RFC6901 refs,
case-artifact identity binding, snapshot/run/observation bindings and event links/order/time.
Selectors resolve relative to the selected entity. Resolved text/nonobject entities, null/
root/nested selectors, stale captures, wrong observed subjects/tools and error completions
remain structurally admissible when their refs are valid. No semantic verdict is invented.

## Exact fixture derivation

[`tests/fixture_source.py`](../../tests/fixture_source.py) independently derives the exact
three fixtures from the hash-bound B1 source. It imports neither Contract nor rfc8785.
Its restricted canonicalizer checks ASCII property names and string/safe-int/bool/null values;
sorted compact stdlib JSON is JCS for that explicit subset. Source digests precede artifact,
case, suite and bundle identities. No expected digest comes from the validator under test.
[`identities.json`](../../fixtures/b2/identities.json) retains fixed raw/semantic/case hashes;
tests independently reconstruct exact checked-in bytes, not merely matching pass counts.

| Input | Raw bytes | Semantic SHA256 (after `sha256:`) |
| --- | --- | --- |
| [Suite](../../fixtures/b2/suite.json) | 15670 | `8d1ecd78c842baa7d6ccec349b2a833d96a829ba625c3c07cc1b24dc41aa452e` |
| [Baseline](../../fixtures/b2/baseline.json) | 39046 | `3a0ccd465a0ee259d7f9155136e2f0520749c67eb44e3faec2941720b7d4d64c` |
| [Candidate](../../fixtures/b2/candidate.json) | 36598 | `68c022d6172c51eea474dabbe6e00ccd1a8f7b0e438601c8777971fdc3911ff2` |

All three suites have8 cases/one assertion per case/17 artifacts. Baseline has8 runs/20 bundle
artifacts; candidate7 runs/18 artifacts, no C07 run/orphan evidence, and internally consistent
old C08 definition. C01–C07 case hashes agree. Inert hostile note preserves LF and ESC exactly;
JSON files escape controls for safe source display. Separate artifact namespaces remain separate.

## Verification and retained execution

Host-verification checked all11 historical manifests, all five approved source hashes, the
retained base inventory and20-file B1e cache before execution. New roots are `artifacts/b2/`
and `/Volumes/AIWorkspace/caches/releaselens/b2-contract/`; all old branches/records are retained.
The host [`experiments/b2/check.py`](../../experiments/b2/check.py) snapshots each exact source
revision before launching a fixed encoder or test command; captures both streams up to1MiB,
supervises each process for at most300s, reserves300s for delivery, samples new allocation
below256MiB and verifies retained runtime/cache before and after. No historical runner main
or closed release is invoked. Failed attempts remain exclusive records before any correction.

Exact Mac test command, sanitized B2 HOME/tmp/cache/config, isolated/no-bytecode:

```text
/Volumes/AIWorkspace/caches/releaselens/b1e-offline-validation/venv/bin/python -I -B /Volumes/AIWorkspace/projects/releaselens/tests/test_contract.py
```

First supervised test run: **20 tests passed in16.885s**, process17.193s, exit0, stdout0B,
stderr2808B, no stop reason or termination signal. The host-only source encoder exited0 in
0.049s. Both immutable command/source/output records are retained. Boundary recipes are serial,
in memory, and each input<=25MiB+1. Tests cover T-01/02 structure/identity plus relevant numeric,
raw-token/decoded/depth/cardinality limits and exact/one-over cases, including embedded arrays.
Mutations assert the intended error category/location, recomputing unrelated identities where
needed. Semantic-ineligibility controls assert successful import, not evaluator outcomes.

CI adds the same tests after the existing hash-verified wheel/environment setup. It reuses that
environment with fresh sanitized CI task directories,180s timeout plus2s kill grace and Linux
1MiB per-file stream capture limits. Hosted evidence is labeled separately from exact Mac tests.
Existing foundation/policy/research/actionlint and PR-attribution jobs remain. Final local checks,
complete attribution/current-head-current-body CI and sealed evidence are recorded in the PR.

## Clock, recovery and remaining gates

Controlling charged start **03:35:45.977457 UTC**, deadline **04:35:45.977457 UTC**; all reads,
implementation/tests/checks/delivery count. Charge full3600s for session1 of at most2/7200s;
reserve at most3600s/one session for separately dispatched corrections, never self-dispatch.
Task-registry durable admission could not be read: external-directory permission denied.
That unknown is retained separately from the first local sample/serialized dispatch; neither
substitutes for the earlier controlling start. Coordinator was asked for the registry record.

After the completed Mac run, serialized history recorded provider.transport WebSocket1006,
retry-attempt2 and synthetic continuation. This task explicitly permits native same-provider
connection recovery. No manual provider retry, model/provider/account switch, paid fallback,
quota/rate/auth bypass, config change or service restart was performed. Final audit includes
actual serialized history with an explicit cutoff and unaudited closing interval for review.
The original clock is not reset by interruption or resumed user instruction.

This delivers a finite pure Contract slice, not full T-03–12, M0/M1–M4, a usable terminal demo,
customer import or production storage qualification. D1–D4 stay unadopted; the original60-second
whole-comparison obligation is unchanged and unproven by these unit-test timings. Existing
hash/TLS/ad-hoc runtime trust and incomplete native inventory remain. Stop for independent
code/fixture/result review; no approval, merge, adoption or next-task dispatch.
