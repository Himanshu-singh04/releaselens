# Proposed evidence contract v1

Draft, pending ADR-2/ADR-3. This is an interface specification, not a shipped schema.
All shapes below are documentation notation, not executable TypeScript or JSON Schema.
The [PRD](product.md) defines scope; the [SDD](specs/001-mvp/solution-design.md) defines components.

## Encoding, identifiers, and provenance

Inputs are UTF-8 JSON, without duplicate object keys, invalid Unicode, or nonfinite numbers.
Reject unknown fields and unsupported `schema_version`; v1 uses the literal `"1"`.
All listed fields are required; `?` is not used. `T|null` explicitly permits unknown.
`ID` is 1–128 ASCII characters matching `[A-Za-z0-9][A-Za-z0-9._:-]*`.
`Hash` is `sha256:` followed by 64 lowercase hex characters. IDs identify things; hashes
identify their exact content. A stable case ID must not hide a changed case hash.
`Time` is a valid UTC timestamp `YYYY-MM-DDTHH:mm:ss.sssZ`; leap seconds are rejected in v1.
`Scalar` is string, boolean, null, or safe integer; monetary examples use integer minor units.
`JSON` is bounded valid JSON; integers must be safe and fractions finite IEEE-754 values.

`H(x)` means SHA-256 of UTF-8 RFC 8785 canonical JSON of x. Array order is significant.
Hash fields exclude only themselves at the specified object level, never nested hashes.
Text artifact digests use exact UTF-8 content bytes; JSON artifact digests use `H(content)`.
No whitespace/Unicode normalization of text or path-dependent IDs is permitted.
Record both exact input-file byte hashes and semantic bundle/suite hashes in the report.
Hashes detect substitution relative to a declared manifest, not authenticity or causation.
Redaction creates a new artifact/hash and bundle; never silently mutate an old evidence item.

## Shared shapes

| Shape | Exact fields / permitted values |
| --- | --- |
| `Source` | `{source_id:ID, kind:"policy"|"knowledge"|"prompt"|"model"|"tool"|"exporter"|"business_snapshot", version:string|null, digest:Hash|null}` |
| `Ref` | `{artifact_id:ID, pointer:string|null}`; null selects an entire text artifact; a JSON artifact requires an RFC 6901 pointer, including `""` for its root. |
| `Artifact` | `{artifact_id:ID, media_type:"text/plain"|"application/json", content:string|JSON, sha256:Hash, source:Source, captured_at:Time|null, redacted:boolean}` |
| `Provenance` | `{producer:Source, exported_at:Time|null, configuration:Source[]}`; producer kind is exporter. |
| `Diagnostic` | `{code:string, location:string, message:string}`; location is an input JSON Pointer, message omits raw sensitive content. |

Artifact content type must match media_type. References never contain file paths or URLs.
Every supplied Ref must resolve within its owning suite or bundle, including the pointer;
a dangling Ref invalidates that input. Missing evidence is represented by null or an empty
array where permitted, not by a fabricated dangling reference. All artifact IDs are unique
within the container. Cross-container refs are forbidden; reports qualify refs with owner.
Source IDs are stable within the user's project. Within one container each source_id must
have exactly one kind/version/digest tuple; different versions belong in different bundles.
Configuration contains exactly one prompt and one model descriptor, and zero or more tool
and knowledge descriptors. Unknown version/digest is null, never guessed from a filename.

## Suite and assertion definitions

| Shape | Exact fields / constraints |
| --- | --- |
| `Suite` | `{schema_version:"1", suite_id:ID, revision:string, cases:Case[], artifacts:Artifact[], suite_hash:Hash}`; at least one case, `suite_hash=H(Suite without suite_hash)`. |
| `Case` | `{case_id:ID, title:string, input:Ref, policy_refs:Ref[], assertions:Assertion[], case_hash:Hash}`; at least one assertion. |
| `Assertion` | `{assertion_id:ID, kind:"value"|"effect", operator:"equals"|"contains"|"not_contains", expected:Scalar, effect:EffectRule|null}` |
| `EffectRule` | `{tool:ID, subject:Scalar, source_id:ID, source_version:string, source_digest:Hash, max_age_ms:integer}`; max_age_ms is positive, at most 86400000. |

Case/assertion IDs are unique within suite/case respectively. Policy refs select policy or
knowledge artifacts; input and policies live in suite artifacts. Case hash is `H({definition,
artifacts})`, where definition is Case without case_hash, and artifacts is the full set of
artifacts referenced by input/policy_refs sorted by artifact_id. This binds bytes AND source
metadata. `suite_hash` binds all cases and artifacts. Revision is a human label, not identity.
`contains`/`not_contains` require string expected and string actual; literal case-sensitive
substring only, no regex, locale folding, or executable expression. `equals` uses exact type
and value equality on Scalar. Explicit JSON null is a value; absent evidence is not null data.
An effect assertion requires operator equals and a nonnull EffectRule; value requires null.
The rule pins the accepted business-observation source, subject, tool, and freshness window.
Changing any rule, input, policy bytes, or source metadata changes case_hash and comparability.

## Bundle, runs, and tool evidence

| Shape | Exact fields / constraints |
| --- | --- |
| `Bundle` | `{schema_version:"1", bundle_id:ID, suite_snapshot:Suite, provenance:Provenance, artifacts:Artifact[], runs:Run[], bundle_hash:Hash}`; hash excludes only bundle_hash. |
| `Run` | `{run_id:ID, case_id:ID, case_hash:Hash, started_at:Time|null, ended_at:Time|null, status:"complete"|"error"|"timeout"|"skipped", error_code:string|null, observations:Observation[], events:Event[]}` |
| `Observation` | `{assertion_id:ID, value:Ref|null, effect_event_id:ID|null}` |
| `Request` | `{event_id:ID, kind:"request", seq:integer, occurred_at:Time|null, tool:ID, subject:Scalar, arguments:Ref}` |
| `Completion` | `{event_id:ID, kind:"completion", seq:integer, occurred_at:Time|null, request_id:ID, status:"success"|"error", result:Ref}` |
| `Effect` | `{event_id:ID, kind:"effect", seq:integer, occurred_at:Time|null, completion_id:ID, subject:Scalar, observation:Ref}` |

`Event` is exactly Request, Completion, or Effect. Each run references a case in its embedded
suite_snapshot with matching case_hash. Unique run_id and one run per case per bundle;
repeated trials require distinct bundles, never “last run wins.” Zero runs is valid missing
coverage. error/timeout require error_code; complete/skipped require null. A skipped run
has empty events/observations. Partial error/timeout evidence can be displayed, not passed.
Observation assertion_id must exist in that run's case; at most one per assertion. Value
observations use value Ref|null and null effect_event_id. Effect observations use null value
and effect_event_id pointing to an Effect in the same run, or null for missing evidence.

Event IDs and seq are unique within run; seq is a nonnegative safe integer. Linked completion
must follow its request in seq; effect must follow its completion. One completion per request
and one effect per completion in v1; retries are distinct requests. Events need not be adjacent.
All links resolve within the same run; no cross-case chains. Multiple observations can cite
one event only if each rule is independently satisfied. Events remain data; no execution occurs.
Request arguments, completion result, and effect observation all cite bundle artifacts.
An effect observation selects a Scalar in a JSON business_snapshot artifact. A successful
completion is necessary but insufficient: source tuple, subject, tool, time, and value must
also satisfy the reviewed EffectRule. Agent transcript or tool-return text is not an
independent business_snapshot, even when it says “refund completed.” Importers must disclose
source origin; a dishonest exporter can still forge it. Report wording must retain that limit.

## Time and evaluation rules

occurred_at is a producer's event-time claim; captured_at is the observation capture-time
claim; exported_at is serialization time. None is a trusted clock or causal proof.
seq supplies run-local ordering, never global ordering between baseline and candidate.
Known run start/end must be ordered; known linked event times must be nondecreasing and
within known run boundaries. Violations invalidate input. Null times are permitted.
For effect evaluation, completion/effect times and observation captured_at must be known,
and completion <= effect <= captured_at <= completion + max_age_ms. Missing times, stale
capture, or a mismatched source/tool/subject make that assertion unknown with a reason.
Source freshness uses explicit versions and this window, never filesystem modification time.
Export time need not equal capture time; a later import does not refresh old observations.

For a complete run, each value assertion resolves its observation. Missing observation,
null value Ref, or wrong actual type => unknown. A supplied invalid Ref is an import error.
A supported comparison on an eligible actual value returns pass or fail. A missing string
cannot pass not_contains. For effect, a completion error or absent eligible chain => unknown;
a fresh eligible business observation unequal to expected => fail; equal => pass.
For error/timeout/skipped runs all assertion outcomes are unknown, with run status retained.
No assertions can be disabled at runtime; edit/review the suite to change required coverage.
Aggregate: any fail => fail; otherwise any unknown => unknown; otherwise all pass => pass.
Empty required sets are invalid, never vacuous pass. Preserve unknown counts even with fail.

Illustrative sequence (not a valid fixture): request refund(order-7), completion success,
business snapshot refund_state=pending. Expected refunded => fail. Remove the snapshot =>
unknown. Replace with agent text “refunded” => unknown. Snapshot refunded with matching
source/time/subject => pass against imported evidence, not proof of exporter authenticity.

## Alignment and comparison

The explicitly supplied reviewed suite is authoritative for expected cases and denominator.
For each expected case, baseline/candidate must each contain a run with matching case_hash.
Missing run => missing/unknown; differing hash => changed_definition/unknown, even if IDs
match. Different suite hashes alone do not invalidate unchanged case hashes. Different
suite_id => fatal incompatible input. Extra run cases are displayed as extra and excluded
from expected-case metrics, never silently dropped. No fuzzy matching or invented pairing.
Case alignment labels: matched, missing_baseline, missing_candidate, missing_both, or
changed_definition; changed_definition takes precedence if any present run hash mismatches.
Each side separately retains present/missing/changed status and its run status.

| Baseline → candidate | Delta |
| --- | --- |
| pass → fail | regression |
| fail → pass | improvement |
| pass → pass; fail → fail | unchanged |
| Any unknown or unaligned side | incomparable |

Candidate aggregate still exposes fail/unknown regardless of delta. pass→unknown is an
incomparable coverage loss, prominently flagged, never “no regressions, safe to ship.”
Report evaluated coverage is `(pass + fail)/expected`; evidence coverage, unknown count,
aligned pair count, missing/changed/extra counts, and run error statuses appear separately.
Case and assertion denominators both come from the reviewed suite, not surviving imports.

## Proposed report shape and persistence

| Shape | Exact fields |
| --- | --- |
| `Outcome` | `{assertion_id:ID, status:"pass"|"fail"|"unknown", reason:string, citations:Citation[]}` |
| `Citation` | `{owner:"suite"|"baseline"|"candidate", ref:Ref, artifact_hash:Hash}` |
| `Side` | `{presence:"present"|"missing"|"changed", run_id:ID|null, run_status:"complete"|"error"|"timeout"|"skipped"|null, status:"pass"|"fail"|"unknown", outcomes:Outcome[]}` |
| `Row` | `{case_id:ID, alignment:string, baseline:Side, candidate:Side, delta:"regression"|"improvement"|"unchanged"|"incomparable"}` |
| `Counts` | `{expected:integer, pass:integer, fail:integer, unknown:integer, missing:integer, changed:integer, extra:integer, error:integer, timeout:integer, skipped:integer}` |
| `Result` | `{schema_version:"1", evaluator_version:string, suite_hash:Hash, baseline_hash:Hash, candidate_hash:Hash, rows:Row[], extra_baseline:ID[], extra_candidate:ID[], case_counts:{baseline:Counts,candidate:Counts}, assertion_counts:{baseline:Counts,candidate:Counts}, aligned_pairs:integer, result_hash:Hash}` |
| `Report` | `{schema_version:"1", generated_at:Time, input_byte_hashes:{suite:Hash,baseline:Hash,candidate:Hash}, suite:Suite, baseline:Bundle, candidate:Bundle, result:Result}` |

alignment uses only the five labels above. Each Side has one Outcome per expected assertion,
including synthesized unknowns. Reasons use stable codes: MATCH, MISMATCH, MISSING_EVIDENCE,
TYPE_MISMATCH, INELIGIBLE_EFFECT, RUN_ERROR, RUN_TIMEOUT, RUN_SKIPPED, MISSING_CASE, CHANGED_CASE.
Counts pass/fail/unknown partition expected; other counters overlap and must be labeled.
Assertion missing/changed/error/timeout/skipped count assertions in affected cases; extra
counts assertions in extra cases. Extra ID lists are case IDs, sorted lexically.
Rows/outcomes sort by case_id/assertion_id; citations sort by owner/artifact_id/pointer.
`result_hash=H(Result without result_hash)`; generated_at is deliberately outside it.
Report retains input snapshots for offline audit; duplicates are an intentional portability
tradeoff. HTML renders these same results with escaped text, no scripts or remote resources.
Valid comparison writes report.json and report.html in a new generation directory, with
completion.json written last: `{schema_version:"1", json_hash:Hash, html_hash:Hash}` containing
SHA-256 hashes of the exact respective output-file bytes. Existing generations are
never overwritten. The marker is an integrity convention, not a guarantee against disk loss.

## Versioning and bounds

All numerical bounds are proposed/unmeasured: suite <= 5 MiB, each bundle <= 25 MiB,
1000 expected cases, 20 assertions/case, 200 events/run, 2000 artifacts/container,
1 MiB/artifact, JSON depth <= 32, and aggregate decoded artifacts <= 20 MiB/container.
Apply case/assertion limits to embedded snapshots too. Reject excess before full allocation
where possible; runtime must independently enforce a 60-second comparison deadline.
No archives, symlinks, recursive discovery, external URI dereferencing, or automatic migrations.
New major schemas require explicit conversion to a new file with old/new hashes recorded;
preserve originals. Never partially interpret an unsupported schema as an empty passing suite.
