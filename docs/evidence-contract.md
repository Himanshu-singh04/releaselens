# Proposed evidence contract v1

Interface specification, not a shipped schema; remaining ADR-2/ADR-3 gates stay open.
N1–N4 and the synthetic-only scope are adopted; [B0d](decisions/005-adopted-policy-reconciliation.md)
records authority; normative reconciliation merged in [PR #19](https://github.com/Himanshu-singh04/releaselens/pull/19). Enforcement remains unverified.
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
`JSON` is bounded valid JSON. Reject a numeric token whose exact mathematical
decimal value is integral and outside [-9007199254740991, 9007199254740991], including dot and
exponent forms, before binary64 conversion. Reject nonfinite binary64 results and rounded
integral binary64 results outside that range. Other finite rounding is permitted subject to N3.
N3: Reject a nonzero exact decimal token if binary64 conversion produces zero.
Accept finite nonzero subnormal rounding. Accept signed exact zero; canonicalize it to 0.

`Scalar` is string, boolean, null, or safe integer; monetary examples use integer minor units.
After N1/N3 validation, normalize every integral binary64 numeric value
in the safe range to an exact integer, including dot/exponent spellings and signed zero.
Integer-grammar tokens retain their exact safe integer value. Nonintegral numbers remain binary64
and are not Scalars. Boolean is a distinct type; never coerce it to/from integer.
N1 is the JSON safety rule above; replacement N2 is this normalization rule. Apply them to
every JSON number, including nested artifact content, expected/actual values, subjects and
integer fields, before type validation, hashing or equality. Other field constraints still apply.
Thus 1, 1.0 and 1e0 have the same Scalar meaning and semantic hash; true stays distinct.
The accepted binary64 rounding trade-off includes 1.0000000000000001 becoming integer 1;
numeric spelling does not encode type, and exact decimal precision is not promised.

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
| `Diagnostic` | `{code:string, location:Location, message:string}`; message is a fixed diagnostic description, never raw input values, argument text, paths, or OS exception text. |
| `Location` | `{kind:"input", input:"suite"|"baseline"|"candidate", pointer:string}` OR `{kind:"argument", index:integer}` OR null; no other fields. |

Input locations use RFC 6901 pointers relative to the selected input's root, including
suite_snapshot paths inside bundles. Unlike evidence Refs, they may identify a missing member.
Use schema-known property names/array indices only; unknown keys report their known parent,
and unparseable input uses pointer "". Argument index is zero-based in user tokens after the
executable (excluding runtime/script wrappers): compare is index 0. Unknown/repeated flags
locate the offending occurrence; a missing value locates its flag. A wholly missing required
flag or unlocatable I/O/platform/internal error uses null. Never echo the indexed token/value.

Artifact content type must match media_type. References never contain file paths or URLs.
Every supplied Ref must resolve within its owning suite or bundle, including the pointer;
a dangling Ref invalidates that input. Missing evidence is represented by null or an empty
array where permitted, not by a fabricated dangling reference. All artifact IDs are unique
within the container. Cross-container refs are forbidden; reports qualify refs with owner
and container. Each embedded suite_snapshot has its own artifact namespace, independent
of its containing bundle; equal artifact IDs across these namespaces are permitted.
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
and value equality on Scalar after the numeric normalization above, including subject equality.
Explicit JSON null is a value; absent evidence is not null data.
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
| `Effect` | `{event_id:ID, kind:"effect", seq:integer, occurred_at:Time|null, completion_id:ID, subject:Scalar, entity:Ref, subject_pointer:string|null, value_pointer:string|null}` |

`Event` is exactly Request, Completion, or Effect. Each run references a case in its embedded
suite_snapshot with matching case_hash. Unique run_id and one run per case per bundle;
repeated trials require distinct bundles, never “last run wins.” Zero runs is valid missing
coverage. error/timeout require error_code; complete/skipped require null. A skipped run
has empty events/observations. Partial error/timeout evidence can be displayed, not passed.
Observation assertion_id must exist in that run's case; at most one per assertion. Value
observations use value Ref|null (resolved in the owning bundle.artifacts) and null effect_event_id.
Effect observations use null value and effect_event_id pointing to an Effect in the same run,
or null for missing evidence.

Event IDs and seq are unique within run; seq is a nonnegative safe integer. Linked completion
must follow its request in seq; effect must follow its completion. One completion per request
and one effect per completion in v1; retries are distinct requests. Events need not be adjacent.
All links resolve within the same run; no cross-case chains. Multiple observations can cite
one event only if each rule is independently satisfied. Events remain data; no execution occurs.
Request arguments, completion result, and effect entity all cite bundle artifacts.
Structural validation: entity is any well-formed resolved Ref, including text or nonobject
JSON. Each nonnull subject_pointer/value_pointer must be a valid RFC 6901 pointer resolving
relative to the selected entity value, not the artifact root. Null means selector absent.
Malformed or unresolved refs/selectors invalidate input; resolved values never fail import
merely because their media type, source kind, or selected shape is ineligible for an effect.

Semantic eligibility: entity must select a JSON object (not an array) from an independent
business_snapshot artifact. Both selectors must have exactly one reference token, selecting
direct Scalar members of that same object. Empty/root or multi-token selectors are ineligible,
even if resolved: an artifact-root selection cannot combine one record's ID with another's
state. Exporters with nested records must select the record object and expose direct fields.
The observed subject member must equal EffectRule.subject, Request.subject, and Effect.subject
by exact type/value equality. Source tuple, request tool, successful completion, and freshness
must also match the rule. Only then compare the observed value member with Assertion.expected.
Effect pass/fail citations must include both observed subject and value, using the same artifact
and full pointers formed by entity.pointer + the respective one-token selector.
Missing selectors or any semantic ineligibility yield unknown, never an import error or pass.
Agent transcript/tool-return text is not independent business evidence, even when it says
“refund completed”; a resolved Ref to it is valid but ineligible. Importers must disclose
source origin; a dishonest exporter can still forge it. Report wording must retain that limit.

## Time and evaluation rules

occurred_at is a producer's event-time claim; captured_at is the observation capture-time
claim; exported_at is serialization time. None is a trusted clock or causal proof.
seq supplies run-local ordering, never global ordering between baseline and candidate.
Known run start/end must be ordered; known linked event times must be nondecreasing and
within known run boundaries. Violations invalidate input. Null times are permitted.
For effect evaluation, completion/effect times and entity artifact captured_at must be known,
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
entity selects {"order_id":"order-7","refund_state":"pending"}; selectors are /order_id
and /refund_state. Expected refunded => fail. Missing effect observation => unknown; leaving
a dangling entity Ref instead => import error. A resolved entity Ref to agent text with null
selectors => unknown. A fresh eligible order-7 record with refunded => pass against imported
evidence, not proof of exporter authenticity. An order-8 record with refunded => unknown even
if every hash/source/time is valid and request/effect metadata both claim order-7.

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
Report evaluated coverage is `(pass + fail)/expected`, separately per side for cases and
assertions. Both denominators come from the nonempty reviewed suite, not surviving imports.
A separate “evidence coverage” metric is deferred; presence of requests or artifacts is not
eligible evidence coverage. Show unknown, aligned-pair, missing/changed/extra, and run-status
counts with the meanings below. Also show assertion evidence-gap counts per side for each
of MISSING_EVIDENCE, TYPE_MISMATCH, and INELIGIBLE_EFFECT: count expected Outcomes with status
unknown and that exact reason. These are derived reason counts, not a new ratio or stored
field; their sum is only a subset of assertion unknown, excluding run/alignment causes.

## Proposed report shape and persistence

The adopted synthetic-terminal demo uses the same Suite/Bundle/Result semantics and
namespace-qualified citations for bundled reviewed inputs. It accepts no customer/path
imports and invokes no Store, persisted Report or release package. It displays outcomes,
deltas, reasons, citations and coverage with terminal control characters escaped; it does
not satisfy RL-008/011 publication. The Report shape and persistence obligations below
remain the customer-product contract. No field or schema-version literal changes for the demo.
The [roadmap exception](roadmap.md#ordered-milestones) changes sequencing only within that scope;
the bounds and original 60-second deadline below still apply. Enforcement is unverified.

| Shape | Exact fields |
| --- | --- |
| `Outcome` | `{assertion_id:ID, status:"pass"|"fail"|"unknown", reason:string, citations:Citation[]}` |
| `Citation` | `{owner:"suite"|"baseline"|"candidate", container:"suite"|"bundle"|"suite_snapshot", ref:Ref, artifact_hash:Hash}` |
| `Side` | `{presence:"present"|"missing"|"changed", run_id:ID|null, run_status:"complete"|"error"|"timeout"|"skipped"|null, status:"pass"|"fail"|"unknown", outcomes:Outcome[]}` |
| `Row` | `{case_id:ID, alignment:string, baseline:Side, candidate:Side, delta:"regression"|"improvement"|"unchanged"|"incomparable"}` |
| `Counts` | `{expected:integer, pass:integer, fail:integer, unknown:integer, missing:integer, changed:integer, extra:integer, error:integer, timeout:integer, skipped:integer}` |
| `Result` | `{schema_version:"1", evaluator_version:string, suite_hash:Hash, baseline_hash:Hash, candidate_hash:Hash, rows:Row[], extra_baseline:ID[], extra_candidate:ID[], case_counts:{baseline:Counts,candidate:Counts}, assertion_counts:{baseline:Counts,candidate:Counts}, aligned_pairs:integer, result_hash:Hash}` |
| `Report` | `{schema_version:"1", generated_at:Time, input_byte_hashes:{suite:Hash,baseline:Hash,candidate:Hash}, suite:Suite, baseline:Bundle, candidate:Bundle, result:Result}` |

alignment uses only the five labels above. Each Side has one Outcome per expected assertion,
including synthesized unknowns. Reasons use stable codes: MATCH, MISMATCH, MISSING_EVIDENCE,
TYPE_MISMATCH, INELIGIBLE_EFFECT, RUN_ERROR, RUN_TIMEOUT, RUN_SKIPPED, MISSING_CASE, CHANGED_CASE.
Reason precedence: missing side => MISSING_CASE; changed case => CHANGED_CASE; otherwise
error/timeout/skipped => corresponding RUN_* for every assertion. For a complete run, absent
Observation or null in the assertion's applicable field (value for value assertions,
effect_event_id for effect assertions) => MISSING_EVIDENCE. Present value of wrong type =>
TYPE_MISMATCH; present effect failing any eligibility condition => INELIGIBLE_EFFECT. Eligible
comparisons use MATCH/MISMATCH. Thus request-only produces MISSING_EVIDENCE, stale effect
produces INELIGIBLE_EFFECT, and an error run produces RUN_ERROR regardless of attached evidence.
Counts pass/fail/unknown partition expected; other counters overlap and must be labeled.
Assertion missing/changed/error/timeout/skipped count assertions in affected cases; extra
counts assertions in extra cases. Extra ID lists are case IDs, sorted lexically.
Citation resolution uses exactly one artifact array: (suite,suite) => Report.suite.artifacts;
(baseline,bundle)/(candidate,bundle) => Report[owner].artifacts; (baseline,suite_snapshot)/
(candidate,suite_snapshot) => Report[owner].suite_snapshot.artifacts. All other pairs are invalid.
Find the unique artifact_id there, require artifact_hash == Artifact.sha256, then resolve Ref
by its media-type/pointer rules. Never search another namespace or fall back by matching ID/hash.
Every pass/fail value Outcome must include the exact observed-value Citation: owner is that
Row's baseline/candidate side, container is bundle, ref equals Observation.value in the run
identified by Side.run_id and matching assertion_id, and artifact_hash is that artifact's
validated sha256. Require exact artifact_id and pointer equality, including null for text;
another existing artifact, same-kind source, equal scalar, or matching bytes is not a substitute.
Additional contextual citations are allowed but cannot replace the required observed citation.
Renderer validates this binding as well as resolution before publication, without re-evaluating
rules. Empty/misbound determinate citations prevent publication (E_INTERNAL), as do invalid
effect citations under their subject/value binding rules; future invalid AI citations abstain.
Rows/outcomes sort by case_id/assertion_id. Citations sort lexicographically by owner, container,
artifact_id, pointer (null before strings), then artifact_hash; string ordering uses UTF-16 code
units without locale folding. Identical full citations are deduplicated; distinct namespaces
remain distinct even with equal artifact IDs/hashes. The renderer uses this exact resolver.
`result_hash=H(Result without result_hash)`; generated_at is deliberately outside it.
Report retains input snapshots for offline audit; duplicates are an intentional portability
tradeoff. HTML renders these same results with escaped text, no scripts or remote resources.
Valid comparison writes report.json and report.html in a new generation directory, with
completion.json written last: `{schema_version:"1", json_hash:Hash, html_hash:Hash}` containing
SHA-256 hashes of the exact respective output-file bytes. Existing generations are
never overwritten. Publication additionally requires the verified owner-private permissions
and pinned I/O identities in [operations](operations.md); unsupported storage fails closed.
The marker is an integrity convention, not a guarantee against disk loss.

## Versioning and bounds

Retained numerical ceilings, with adopted N4 accounting and unverified enforcement:
suite <= 5 MiB, each bundle <= 25 MiB,
1000 expected cases, 20 assertions/case, 200 events/run, 2000 artifacts/container,
1 MiB/artifact, JSON depth <= 32, and aggregate decoded artifacts <= 20 MiB/container.
Reject a UTF-8 BOM. Count open object/array containers, ignoring string contents:
root container depth 1, primitive depth 0; depth 32 is allowed, 33 rejects. MiB = 1048576 bytes.
Suite/bundle limits count exact input UTF-8 bytes including whitespace. Per-artifact 1 MiB
counts its raw JSON content-value token bytes, including quotes/escapes and internal whitespace.
Aggregate decoded content counts UTF-8 bytes for text and JCS bytes for JSON, independently
per artifact array, including embedded suite arrays. All byte bounds are inclusive.
Measure token spans before decoding and decoded totals after content validation. Whitespace/
escape-heavy exports can exceed limits despite equal decoded content; re-encoding changes byte hashes.
Apply case/assertion limits to embedded snapshots too. Reject excess before full allocation
where possible; runtime must independently enforce a 60-second comparison deadline.
No archives, symlinks, recursive discovery, external URI dereferencing, or automatic migrations.
New major schemas require explicit conversion to a new file with old/new hashes recorded;
preserve originals. Never partially interpret an unsupported schema as an empty passing suite.
