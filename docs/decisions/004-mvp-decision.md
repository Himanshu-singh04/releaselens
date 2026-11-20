# B0c: minimum demo and founder decision packet

Status: **recommendation only; no requirement adoption or implementation authorization.**
Date: 2026-11-20. GPT-6 Astra (`gpt-6-astra`) / OpenCode, persistent worker; no subagents.
Base: `b271ec1f19f3f4a67ef9dd2279af129334c322b1`; [issue #16](https://github.com/Himanshu-singh04/releaselens/issues/16), A1–A6.
First-cycle deadline: 07:15 UTC. Evidence: existing repository records; zero new external sources.

Recommend a **bundled-synthetic terminal demo**, then the customer product. Adopt N1/N3/N4,
the **N2 replacement below**, D1–D4 and an explicit pre-storage fixture/pure-computation exception.
Keep CPython 3.14.10 standard GIL / rfc8785 0.1.4 as the conditional product direction; M0 stays open.
The first authorized slice should specify eight reviewed synthetic fixtures and expected outcomes.

## A1: journey and observable finish line

The engineer selects the bundled refund-policy example, compares its fixed baseline/candidate,
then reads a terminal table: case, both outcomes, delta, reason, citations and expected-suite coverage.
The demo accepts no user-supplied path/customer data; the renderer escapes terminal control characters.
The engineer must distinguish the synthetic regression from a request-only “refunded” claim and cite its record.
Finish: all eight reviewed rows appear, including missing/changed cases; ten identical
comparisons yield the same Result hash; an independent reviewer explains the regression and
coverage loss from the report without author interpretation. Record failures, not a usability claim.

Required: exact Scalars; pass/fail/unknown; request ≠ completion ≠ independently sourced effect;
same-record subject/value/source/time eligibility; suite alignment; stable reasons/counts/hashes/citations.
An eligible mismatching business value fails; request-only, failed completion, stale evidence
or wrong subject stays unknown. A missing negative observation cannot pass `not_contains`.
Hashes bind imported claims, not exporter honesty. This demo does not run a support agent.

Deferred: arbitrary imports, durable generations/marker/recovery, offline HTML/JSON package,
installer/pilot, adapters, database, server, AI and live actions. Terminal output does not satisfy
RL-008/011 publication. Public synthetic source stays on the checkout; customer storage stays gated.
Feedback: can engineers understand effect gaps/changed coverage? Demand and policy correctness remain untested.

## A2: numeric decisions (exact proposed wording; not applied)

Locations refer to the unchanged base [contract](../evidence-contract.md) and [testing plan](../testing.md).
No executable schema exists. Proposed text governs all `JSON`, `Scalar` and integer-field uses;
field names/schema-version literal stay unchanged. Quoted replacements require explicit adoption.
Accepted [B0b](003-json-conformance.md): 105 finite CPython 3.13.4 controls, not target qualification; lexical N2 differs below.
Current shared test clauses: T-01 “unsafe numbers”; T-03 “Exact equals”; T-06 “Object key order
changes preserve semantic hash, byte hashes differ”; T-08 “Every limit at boundary and one unit beyond”.
Retain those clauses and append the exact per-decision vectors below; no product tests exist yet.

### N1: safe integers before and after conversion: adopt

Old contract L17: “`JSON` is bounded valid JSON; integers must be safe and fractions finite IEEE-754 values.”
Replace with: “`JSON` is bounded valid JSON. Reject a numeric token whose exact mathematical
decimal value is integral and outside [-9007199254740991, 9007199254740991], including dot and
exponent forms, before binary64 conversion. Reject nonfinite binary64 results and rounded
integral binary64 results outside that range. Other finite rounding is permitted subject to N3.”
Schema: apply before constructing any numeric field, including nested artifact content.
Append to T-01: “Accept 9007199254740991; reject 9007199254740992, 9007199254740993e0, 1e30
and 9007199254740991.5 (rounds to an unsafe integer), with a fixed input diagnostic.”
Reject lexical-only checks (`1e30` evades them). Compatibility: unsafe dot/exponent inputs reject; use strings for large IDs.

### N2: replace lexical typing with canonical-value normalization

Old contract L16: “`Scalar` is string, boolean, null, or safe integer; monetary examples use integer minor units.”
Old L73–74: “`equals` uses exact type and value equality on Scalar.” B0b proposed integer
grammar → int, dot/exponent → float, making `1.0` ineligible for Scalar; recommend **against** it.
Replace L16 with: “`Scalar` is string, boolean, null, or safe integer; monetary examples use
integer minor units. After N1/N3 validation, normalize every integral binary64 numeric value
in the safe range to an exact integer, including dot/exponent spellings and signed zero.
Integer-grammar tokens retain their exact safe integer value. Nonintegral numbers remain binary64
and are not Scalars. Boolean is a distinct type; never coerce it to/from integer.”
Retain exact-type `equals` **after** normalization, including expected/actual, subjects and integer fields.
Append to T-01/03/06: “1, 1.0 and 1e0 normalize to integer 1 and yield equal semantic hashes
and Scalar outcomes; raw byte hashes differ. true never equals 1. 1.5 is JSON, not Scalar.
1.0000000000000001 rounds to integer 1. JCS serialization/reparse preserves normalized types and outcomes.”
Reject lexical N2 because JCS maps `1` and `1.0` to identical bytes while lexical eligibility
could differ. Compatibility: integral float spellings become valid Scalars; producers lose
spelling-as-type distinctions. This is value-after-binary64-rounding, not decimal precision.
**Unverified replacement:** preserve B0b's corpus; validate this rule with new independent normalization/reparse vectors.

### N3: nonzero underflow: adopt

Old L17 is quoted under N1; “fractions finite IEEE-754 values” does not decide zero underflow.
Append after N1: “Reject a nonzero exact decimal token if binary64 conversion produces zero.
Accept finite nonzero subnormal rounding. Accept signed exact zero; canonicalize it to 0.”
Schema: apply throughout JSON before N2 normalization; no separate decimal numeric type.
Append to T-01/06: “1e-400 rejects; 5e-324 remains nonzero; -0.0 accepts and canonicalizes to 0.”
Reject silent underflow: it erases nonzero evidence. Compatibility: some valid JSON rejects; subnormals still round.

### N4: depth, bytes and BOM: adopt with explicit artifact accounting

Old L9: “Inputs are UTF-8 JSON, without duplicate object keys, invalid Unicode, or nonfinite numbers.”
Old L243–245: “suite <= 5 MiB, each bundle <= 25 MiB” and “1 MiB/artifact, JSON depth <= 32,
and aggregate decoded artifacts <= 20 MiB/container.” Other count limits remain unchanged.
Append: “Reject a UTF-8 BOM. Count open object/array containers, ignoring string contents:
root container depth 1, primitive depth 0; depth 32 is allowed, 33 rejects. MiB = 1048576 bytes.
Suite/bundle limits count exact input UTF-8 bytes including whitespace. Per-artifact 1 MiB
counts its raw JSON content-value token bytes, including quotes/escapes and internal whitespace.
Aggregate decoded content counts UTF-8 bytes for text and JCS bytes for JSON, independently
per artifact array, including embedded suite arrays. All byte bounds are inclusive.”
Schema: retain counts/limits; measure token spans before decoding, decoded totals after validation.
Artifact/aggregate accounting is an **unverified clarification** beyond B0b's standalone byte tests.
Append to T-01/08: “Depth 32 accepts, 33 rejects; braces in strings do not add depth. Each
byte limit accepts exactly its bound and rejects one byte over; count whitespace, multibyte
UTF-8 and escaped text. BOM rejects. Test embedded arrays and 20 MiB decoded aggregate separately.”
Reject post-trim/character counts, BOM stripping and root-depth-zero: they disagree on limits.
Compatibility: whitespace/escape-heavy exports may reject; re-encoding changes byte hashes. Resources remain unmeasured.

## A3: storage decisions (exact proposed wording; not applied)

Recommend all four replacements together. [C1–C4 schedules](002-storage-protocol.md#counterexamples-and-separate-founder-decisions)
are reasoned counterexamples, not executed faults. Reconcile cited tests/operations/SDD in the
adoption PR; no storage schema fields change. RL-011 still rejects partial/hash-invalid completion.

### D1: stable-owner privacy, observed drift rejection

Old [R5/T-09](../testing.md#fixtures-and-review-discipline): “permissive umask, inherited broad ACL,
wrong owner, ignore-ownership/unsupported volume, and ACL drift must not expose evidence or
publish successfully.” [Operations](../operations.md#proposed-local-runtime-and-packaging) requires
owner-private creation and rechecks; retain its empty-probe and ordinary-account denial duties.
Replacement: “Under stable owner/privileged permissions, ordinary other accounts must be
unable to read evidence or replace its private namespace. Reject wrong owner, broad/inherited
ACL, noowners or unverified protection before evidence writes. Check each empty output and
recheck at publication; observed permission drift aborts without a success summary.
Owner-driven permission changes between checks are outside the confidentiality guarantee.”
Oracle replacement: “R5 retains real ordinary-account denial and zero-evidence preflight
rejection tests. Inject observed drift: require failure/no summary. Exercise transient ACL
grant/read/restore separately as a limitation demonstration, never as a passing privacy test.”
Retain stable-owner access control; lose prevention during owner-driven drift. User must keep permissions stable; no silent repair.

### D2: no redirection, sampled identity/loss detection

Old [R7/T-09](../testing.md#fixtures-and-review-discipline): “replace/unmount the volume or swap an
ancestor after preflight, during input reads, between writes, and immediately around marker
publication. Verify retained-handle identity enforcement, failure on loss, no local/replacement-volume
files or fallback directories, and no success announcement”. [Operations](../operations.md#startup-and-shutdown-plan-after-approval)
also says “Mount loss, replacement, or identity mismatch aborts”.
Replacement: “Retain verified handles; never redirect I/O, reopen by path or choose fallback.
Check identity/mount/private access before and after reads, writes and publication steps,
and after flush before acknowledgement. Observed mismatch or surfaced I/O failure aborts
without initiating a success summary. Success describes the last successful checkpoint,
not continuous namespace/volume availability or an atomic guarantee through caller receipt.”
Oracle replacement: “R7 tests every scheduled fault and requires unchanged replacement-tree
sentinels/no fallback in all cases. Observed faults must fail. Swap-and-restore between checks
or loss after the final check may evade detection; record that limitation, not test success.”
Retain no-redirection/no-fallback; lose continuous detection/atomic availability-to-acknowledgement. Verify storage before retry.
Operations step 4's “no successful publication” becomes “no new success summary; recover under D3”.

### D3: recovered integrity is not caller acknowledgement

Old [SDD error table](../specs/001-mvp/solution-design.md#error-handling): “Exit 4; no complete marker”;
old [UI state text](../specs/001-mvp/solution-design.md#ui-visualization-guide): “fatal errors exit
without a complete marker.” [Contract](../evidence-contract.md#proposed-report-shape-and-persistence)
already says “The marker is an integrity convention, not a guarantee against disk loss.”
Replace the fatal-marker rule with: “Fatal errors suppress a success summary and preserve the
generation for verified recovery. A late failure may leave a valid, unacknowledged completion
marker. Recovery accepts integrity only after validating required files and both exact byte
hashes; it must not infer that the original caller observed success. Never delete a marker
merely to disguise a late failure; retries create a new generation after identity verification.”
Oracle replacement for T-09: “Missing/partial/mismatched files or marker reject; valid hashes
after late error are recoverable with acknowledgement unknown. Observe summary separately.
Inject failures before/after marker rename, flush, final checks and close; no error-path overwrite.”
Retained: hash-bound completeness/no overwrite and required flush ordering before success.
Lose fatal-return marker absence. Users can recover valid failed-attempt output; a marker does not prove acknowledgement.
SDD E_INTERNAL's “no successful report” becomes “no success summary; recovered integrity may exist”.

### D4: decision budget, not a syscall completion deadline

Old [contract L246–247](../evidence-contract.md#versioning-and-bounds): “Reject excess before full
allocation where possible; runtime must independently enforce a 60-second comparison deadline.”
Old [testing](../testing.md#proposed-measurements-and-gates): “Proposed hard limits are in the contract, including a 60-second deadline.”
Replacement: “Retain allocation/count limits. Start a 60-second monotonic decision budget at
compare entry before Store.prepare; check before/after bounded computation and I/O steps.
On observed expiry, start no new comparison/publication work or success summary; return E_LIMIT,
exit 4 when control returns. Cancellation is best effort; record cleanup latency and uncertain
in-flight publication. No hard syscall, process-exit, stdout-delivery or no-late-marker bound.”
Oracle replacement for T-08/09: “Use an independent monotonic observer; inject expiry before
work and block I/O across 60 seconds. Require no newly initiated work/summary after observed
expiry; measure overshoot, cleanup and marker state. A pending syscall may finish later.”
Retained: budget/visible resource failure. Lost: hard completion/rollback; users may wait beyond
60 seconds and must recover before retrying. Preserve B0a R1: Python may implicitly retry EINTR;
Store/bridge no-retry rules do not bound blocking. A watchdog request is not verified termination.

### Proposed target profile: separate authorization still required

Current `noowners` mount remains ineligible. Propose one nonprivileged writer, stable ownership,
owner-enabled local **external APFS**, private effective-UID 0700 directories/0600 single-link
files, empty extended ACLs and nonreplaceable ancestors; trust OS/kernel and honest hardware.
Exclude same-UID/root/stolen-drive protection and internal-disk substitution. Founder must name
an eligible existing device/subtree, evidence location, allowed faults and cleanup owner, excluding
worker credentials/databases and shared physical-loss risk. No path/device is selected here.
Authorize metadata, writes/account tests and physical faults separately; no purchase/remount/permission repair implied.

## A4: runtime and sequencing recommendation

Retain the exact conditional [B0 runtime direction](001-runtime.md#candidate-pins-acquisition-and-reproducibility):
CPython 3.14.10 standard GIL on arm64 macOS, stdlib validation/testing/rendering plus rfc8785
0.1.4, a fresh local venv and later platform-specific wheel containing the narrow C Store bridge.
Use stdlib tooling/reviewed hash-locked offline artifacts; exact pip/backend pins remain **unselected**.
CPython license direction is PSF-2.0 plus notices; inspected rfc8785 wheel is Apache-2.0, 9240
bytes, no mandatory dependencies, SHA-256 `520d690b448ecf0703691c76e1a34a24ddcd4fc5bc41d589cb7c58ec651bcd48`.
Bridge/compiler/SDK notices/package inventory remain unverified. Target 3.14.10 remains uninstalled/unverified;
local 3.13.4/CI 3.14.4 do not qualify it. No supported product runtime/build currently exists.

| Gate / current status | Dependency; smallest next evidence | Separate authorization? |
| --- | --- | --- |
| B0/B0a/B0b finite research — **met** | Accepted records; 105 controls, not product conformance | No rerun needed for this packet |
| N/D adoption, ADR-1–5, M0 — **unmet** | Exact choices; reconcile contract/tests/operations/SDD/roadmap, independent review; AI deferred explicitly | Yes, owner decision; M0 stays open |
| B1 synthetic expectations — **unmet** | Adopted schema/exception; review eight expected rows before code | Yes, drafted slice below |
| Runtime/JCS/N2/N4 — **unverified** | Authorized exact 3.14.10 acquisition; verify artifact/provenance; finite vectors including new normalization and artifact accounting | Yes, installation/validation scope |
| Build/installer/package — **unverified** | Target runtime; select exact hashed pip/backend locks, inspect licenses, clean offline build/install inventory | Yes; no assumed toolchain support |
| Pure evaluator/demo — **unmet** | Runtime/schema + reviewed fixtures; T-03–06 subset and independent terminal triage | Yes, bounded implementation slices |
| Target eligibility/G1/G2/G5 — **unverified** | Named owner-enabled target; read-only metadata/ABI E1 then separate empty/private/no-redirection/collision tests | Yes, E1 and later writes separately |
| G3/G4/G7/G8 strong guarantees — **unmet** | Adopt D1–D4 or supply a different evidenced design; code cannot erase C1–C4 | Yes, requirement decision |
| Native ABI/lifetime/G9 — **unverified** | Target/compiler; layouts, returned-error/EINTR handling, fd/ACL cleanup and blocked-call observation | Yes, native experiment |
| Publication/recovery/durability — **unverified** | Eligible target + bridge + adopted failure model; finite F-01–24, real flush/restart/device evidence | Yes; physical loss separately |
| Bounds/resources — **unverified** | Runtime/importer; all limits, decoded aggregate, RSS/time and D4 overshoot on actual host | Yes, product validation scope |
| Customer readiness/M3–M4 — **unmet** | Import integrity, inert offline HTML/JSON, T-07–10/12, package guide, observed onboarding | Yes, product/pilot scopes |

Exact proposed exception to [M0/M1/B1 ordering](../roadmap.md#ordered-milestones): “After reviewed
schema adoption, B1 source-only synthetic definitions may precede M0. After scoped runtime/JCS
validation, separately authorized pure Contract/Evaluator/terminal-renderer slices may precede
native storage and full packaging qualification. Accept only bundled reviewed synthetic inputs;
no customer/path import, Store, persisted report or release package. M0/M1–M4 remain incomplete.”
Apply this exception to the PRD/SDD implementation gates too; approval of N/D alone is not it.
Terminal scope reduces RL-008 for the demo. Pure calls need no native bridge; eventual Store and original product gates do.

## A5: draft next issue (not created or executed)

Proposed title: `docs: define eight synthetic demo fixture specifications and expectations`.
Readiness: **blocked on founder scope/schema/sequence adoption and reviewed normative reconciliation**; no target needed.
Input: adopted contract, B1 categories and independently authored expectations. Output/files:
`docs/fixtures/mvp-cases.md` (source-data specifications), `docs/fixtures/mvp-expectations.md`
(outcomes/reasons/citations/counts/deltas); preimplementation specs, not hash-valid JSON or completed M1.
Cap: eight cases, <=3 assertions each; fixed baseline/candidate, source tuples and timestamps.
Required rows: eligible refund pass→pass; ineligible refund pass→fail; escalation fail→pass;
missing observation pass→unknown; failed completion pass→unknown; stale effect pass→unknown;
removed candidate pass→unknown; changed-policy case changed_definition/unknown and incomparable.
Positive acceptance: review rows before code; explicit request/completion/effect chains, same-record
citations, explained hash changes; denominator eight, fail outranks unknown without hiding it.
Negative acceptance: transcript-only/request-only/failed completion never verify effects;
wrong subject or stale evidence cannot pass; missing negative observation cannot pass; dangling
references are rejection examples, not missing evidence. Include inert malicious policy text.
Future encoding must compute/verify hashes; no fake hash placeholders. Review 1/1.0/true and N4 accounting examples.
Checks: repository/policy/actionlint/diff, independent table/count/reference review, attribution/CI.
No T-01–06 pass claim. Exclude code/installs/captures/native/E1/customer data/permissions/AI; one PR, stop at review.

## Founder choices and pause branch

Recommended package, each choice separately recorded after coordinator review:
1. Accept the identified documentation revision as a decision packet, not implementation approval.
2. Adopt N1/N3/N4 including artifact accounting, and **replacement N2**, not B0b lexical N2.
3. Adopt D1–D4 together for the customer-product profile, accepting the four lost guarantees.
4. Adopt the terminal scope/sequence exception, conditional runtime and AI deferral; authorize normative reconciliation first, not M0 closure.
5. After prerequisites merge, separately authorize the drafted fixture-specification slice; runtime/native/target actions stay gated.
“Ok proceed” adopts none of these. Retaining universal drift/loss detection, fatal-error marker
absence or hard syscall completion keeps storage NO-GO. Pause customer-product implementation;
the single progress-enabling choice is the synthetic-only exception. No automatic study extension.
