---
title: "ReleaseLens deterministic comparison MVP"
status: draft
version: "0.3"
---

# Solution Design Document

Planning baseline merged in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6).
The [B0 research](../../decisions/001-runtime.md) was conditionally accepted in PR #11;
tested pins and M0 closure remain blocked. The [B0a storage protocol](../../decisions/002-storage-protocol.md)
is proposed for separate review, with explicit no-go guarantees and no authorized test target.
All product components, interfaces, directories, and targets below are proposed/nonexistent.
Template headings are retained verbatim, including bracketed example headings.

## Validation Checklist

### CRITICAL GATES (Must Pass)

- [x] Required sections contain a draft design or explicit N/A.
- [x] No unresolved clarification placeholders in section bodies; decisions are explicit ADRs.
- [x] Architecture pattern and proposed interfaces are described.
- [ ] All architecture gates closed: B0 research accepted, but unresolved validation and requirement decisions remain.
- [ ] Implementation readiness: blocked until owner decisions resolve these gates.

### QUALITY CHECKS (Should Pass)

- [x] Context sources, actual foundation commands, boundaries, and requirement mapping documented.
- [x] Components, data lifecycle, errors, and measurable proposed targets specified.
- [x] B0 research review/approval recorded in PR #11 merge verification; not implementation readiness.
- [ ] B0a protocol independently reviewed and exact-revision founder decision recorded.
- [ ] Runtime/SDK compatibility, resource measurements, and product validation not performed.

## Constraints

CON-1 Agreed: independent local-first product; zero new initial hosting/inference expenditure.
CON-2 Agreed: imported evidence is data; missing evidence is unknown; requests are not effects.
CON-3 Current: repository contains foundation checks, not application code or runtime manifests.
CON-4 Current: source/docs and worker history/OpenAI OAuth are on the pendrive; Mac CPU/RAM
executes processes. Coordinator history/App key remain on Mac; see [operations](../../operations.md).
Worker provisioning does not establish product-private I/O: the observed pendrive is noowners.
CON-5 Proposed: deterministic fixtures/imports first, one local process, no agent execution.
CON-6 Proposed/unmeasured: bounded data and offline reports within [contract](../../evidence-contract.md) limits.

## Implementation Context

### Required Context Sources

#### Documentation Context

| Source read | Relevance | Why |
| --- | --- | --- |
| [Issue #5](https://github.com/Himanshu-singh04/releaselens/issues/5) | CRITICAL | A1–A7 and documentation-only authorization. |
| [AGENTS](../../../AGENTS.md), [contributing](../../../CONTRIBUTING.md) | CRITICAL | Data boundaries, existing commands, contribution policy. |
| [Development](../../development.md), [foundation](../../foundation.md) | CRITICAL | Delivery evidence, review ownership, actual bootstrap state. |
| [PRD](../../product.md), [contract](../../evidence-contract.md) | CRITICAL | Requirements and authoritative proposed shapes/semantics. |
| [Roadmap](../../roadmap.md), [testing](../../testing.md), [operations](../../operations.md) | HIGH | Milestones, verification, storage/recovery. |
| [README](../../../README.md) | HIGH | Public status and navigation; must not imply product availability. |
| Architecture skill template.md and validation.md, local OpenCode configuration | HIGH | Required section order and design-validation criteria; reviewed 2026-11-18. |
| [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) | HIGH | Canonical JSON hashing, duplicate-key/Unicode restrictions; informational specification. |
| [RFC 6901](https://www.rfc-editor.org/rfc/rfc6901.txt) | HIGH | Exact JSON Pointer reference semantics and resolution errors. |
| [B0 runtime recommendation and source register](../../decisions/001-runtime.md) | CRITICAL | #10 runtime comparison, exact version-specific sources retrieved 2026-11-19, observations, native API gaps and ADR disposition. |

External sources constrain proposals, not prove local installation or compatibility. Recheck
runtime support before pinning. No model-serving behavior is assumed without a later primary-source review.

#### Code Context

| File read | Relevance | Implication |
| --- | --- | --- |
| [scripts/check_repository.py](../../../scripts/check_repository.py) | HIGH | Checks tracked text and relative file links only; excludes untracked drafts and anchors. |
| [.github/workflows/ci.yml](../../../.github/workflows/ci.yml) | HIGH | Existing foundation/PR checks; no product build or inference. |
| [.gitignore](../../../.gitignore) | HIGH | Local evidence, models, caches, and session databases excluded from Git. |

Application code context: N/A; no package manifest, product schemas, fixtures, or modules exist.

#### External APIs (if applicable)

N/A for MVP runtime. GitHub supports development delivery only; evidence import does not call
GitHub, vendors, customer agents, model providers, or business systems. Future adapters need separate contracts.

### Implementation Boundaries

- Must preserve: foundation checks, human review, independent product, and zero-spend constraint.
- Can modify for B0a/#12: storage protocol and minimal planning/status links; approval protocol remains coordinator-owned.
- Must not touch now: runtime code, deployment, credentials, model downloads, or worker provisioning.
- Future implementation starts only after explicit decisions close every current ADR gate.

### External Interfaces

#### System Context Diagram

```mermaid
graph LR
    Operator[Engineer / support lead] --> CLI
    Files[Reviewed suite / exported bundles] --> CLI
    CLI --> Report[Offline report files]
    Report --> Operator
```

Files and Report are local data, Operator is external; CLI maps to src/cli below.
The support agent and business system export data outside this boundary; there is no execution arrow.

#### Interface Specifications

Proposed/nonexistent CLI grammar: `releaselens compare --suite FILE --baseline FILE
--candidate FILE --out NEW_DIRECTORY`. Exactly one value per required flag; unknown/repeated
flags fail. No implicit discovery, configuration search, environment credentials, or network.
Inputs are regular nonsymlink files; output must be a new directory under an explicitly
selected existing nonsymlink parent. Require verified owner-private directories/files
(0700/0600 or validated equivalent), ownership/ACL and mount-capability preflight, and an
empty probe before evidence writes; chmod success alone is insufficient. Unsupported access
control refuses publication. [Operations](../../operations.md) specifies pinned-handle mount/
directory identity enforcement through reads, writes, and marker publication; no path fallback.
Outputs: report.json, report.html, completion marker; schemas and hashes in the contract.
stdout: one JSON summary `{status:"pass"|"fail"|"unknown",result_hash:Hash,output_path:string}`
only after complete publication; status aggregates all expected candidate cases.
stderr: Diagnostic JSON lines with tagged input/argument locations or null, per the contract;
no raw evidence, argument values, paths, or OS exception text. Proposed exit codes:
0 candidate pass; 1 candidate fail; 2 usage/input/integrity error; 3 candidate unknown;
4 I/O/resource/internal failure. Fatal error takes precedence; then fail, unknown, pass.
N/A: HTTP endpoints, auth tokens, webhooks, billing, or database connections.

### Cross-Component Boundaries (if applicable)

One product owner and one future package, with pure evaluation separated from filesystem I/O.
The contract is the only public data boundary; internal APIs remain package-private.
Major contract changes require explicit conversions and fixtures; no silent compatibility.
No shared runtime/database/service with other portfolio projects.

### Project Commands

Only existing commands, copied from CONTRIBUTING.md (Git, Python 3.11+, actionlint 1.7.12):

```sh
python3 scripts/check_repository.py
python3 -m unittest discover -s scripts -p 'test_*.py'
actionlint -shellcheck= -pyflakes=
git diff --check
```

Install/dev/build/migrate/seed/product-test commands: N/A; none exist. The CLI grammar above
is a design proposal, not a runnable instruction. Future commands must enter CONTRIBUTING first.

## Solution Strategy

Propose a modular CLI: explicit JSON imports, pure evaluator, immutable results and static
offline renderer. [B0](../../decisions/001-runtime.md) conditionally recommends CPython
3.14.10 with a JCS dependency candidate and a narrow Darwin native bridge; the earlier
TypeScript/Node proposal remains a compared alternative. The native bridge stays in Store;
no new service is proposed. Compatibility, storage guarantees and deadline enforcement
remain blocked. This retains inspectable evidence at the cost of manual export preparation
and narrow semantics; no hosting or inference is needed.
No database is needed for bounded immutable comparisons; files simplify portability but
make concurrent editing and large datasets deliberately unsupported. AI is a later optional layer.

## Building Block View

### Components

```mermaid
graph LR
    CLI --> Importer
    CLI --> Evaluator
    CLI --> Renderer
    CLI --> Store
    Importer --> Contract
    Evaluator --> Contract
    Renderer --> Contract
    Store --> Contract
```

CLI orchestrates only. Importer owns parsing/integrity; Evaluator owns alignment/assertions;
Renderer owns safe presentation; Store owns publication; Contract owns types/version constants.
No component invents evidence, and Renderer cannot re-evaluate or change a verdict.

### Directory Map

All paths proposed, none created by this documentation task. These are logical component
locations; Python package layout is not frozen while ADR-1/4 remain blocked:

| Component | Directory | Responsibility / requirements |
| --- | --- | --- |
| CLI | src/cli | Explicit inputs, deadlines, exit status; RL-010, RL-012. |
| Importer | src/import | Bounded reads, schema/reference/hash checks; RL-001, RL-002, RL-003. |
| Contract | src/contract | Shapes and canonical identity helpers; RL-001, RL-003, RL-009. |
| Evaluator | src/evaluate | Pure alignment, rule outcomes, aggregation; RL-004, RL-005, RL-006, RL-007, RL-009. |
| Renderer | src/report | Self-contained escaped HTML and JSON; RL-008. |
| Store | src/storage | New generation, file digests, completion marker; RL-011. |

fixtures/ would hold reviewed synthetic data; tests/ would cover the [test matrix](../../testing.md).
Later AI work would require a separately reviewed src/explain boundary; it is not in this MVP diagram.

### Interface Specifications

#### Interface Documentation References

[Evidence contract](../../evidence-contract.md), CRITICAL: Suite, Bundle, Run, Event, Ref,
Result, Report, namespace-qualified Citation resolution, provenance, bounds, and aggregation.
It is authoritative over illustrative prose; embedded suites and bundle artifacts are distinct namespaces.
[Operations](../../operations.md), HIGH: publication lifecycle, sensitive inputs, recovery.

#### Data Storage Changes

N/A for database changes. Proposed files: explicit reviewed suite, two immutable input bundles,
and a new output generation with three files. Store does not copy inputs to a global cache.
Report snapshots deliberately duplicate bounded imports for offline audit. No search index.

#### Internal API Changes

Proposed package-private interfaces; all failures return `{ok:false,error:Diagnostic}`:

| Operation | Input | Success `{ok:true,value:...}` |
| --- | --- | --- |
| Store.prepare | Three explicit input paths, new output path | Opaque IoContext with retained verified handles/identities and destination privacy preflight; no evidence written. |
| Importer.load | IoContext, fixed limits | Validated Suite/Bundles, exact byte hashes read from the pinned files; never partial imports. |
| Evaluator.compare | Validated Suite, baseline Bundle, candidate Bundle, evaluator_version | Result; no I/O, clock, randomness, or model calls. |
| Renderer.render | Report | UTF-8 JSON/HTML bytes after exact observed-reference citation binding checks; escaped evidence, no active content. |
| Store.publish | Same IoContext, rendered bytes | Absolute output_path and marker hashes after private-access/mount-identity revalidation. |

CLI creates generated_at once after evaluation, packages Report, renders, publishes, then
emits status. IoContext is private process state, never imported JSON; CLI retains it across
stages and releases handles on all exits. Contract's H helper has conformance tests planned.
N/A: OpenAPI specification, internal HTTP endpoints, cross-process RPC.

#### Application Data Models

Suite defines reviewed expectations; Bundle preserves an export and suite snapshot; Run
records one case attempt; Event preserves request/completion/effect distinctions. Artifact
supplies source-bound bytes; Ref selects exact evidence. Result derives outcomes and coverage;
Report adds timestamp, byte hashes, and snapshots. All fields are specified in the contract.

#### Integration Points

CLI passes validated values between components in memory. Only Importer reads source files;
only Store writes output. Renderer consumes the computed Result, never source HTML templates.
No external integration SDK selected. Export adapters and model runtimes remain gated later work.

### Implementation Examples

These are behavioral examples, not created code or runnable fixtures.

#### Example: [Complex Business Logic Name]

One refund case has value=pass, effect=unknown: case unknown. Add a supported policy failure:
case fail with one unknown still counted. Baseline pass and candidate unknown is incomparable
coverage loss, not unchanged. Baseline fail and candidate fail is unchanged but still a failure.

#### Example: [Integration Pattern Name]

A completed refund call with only a success message lacks business evidence. An eligible
snapshot must bind observed subject and value to direct members of one selected record object;
observed subject must agree with rule/request/effect. A valid order-8 refund cannot verify
order-7; selecting sibling records through root-level multi-token selectors stays unknown.
Resolved transcript/tool-return refs are structurally valid but ineligible (unknown), while
malformed/dangling refs or malformed/unresolved member selectors reject import. Missing selectors stay unknown.

#### Test Examples as Interface Documentation

Planned golden vectors in T-01 through T-06 exercise both examples and exact report shapes.
Tests are planned, not present. Fixture reviews must identify expected outcomes independently
of the evaluator, so snapshots cannot merely bless implementation output.

## Runtime View

### Primary Flow

#### Primary Flow: [Main User Action]

1. Engineer supplies reviewed suite and baseline/candidate exports with a new output location.
2. CLI validates arguments; Store prepares pinned/private I/O; Importer bounds reads and validates inputs.
3. Evaluator aligns each expected case and applies tri-state rules without side effects.
4. CLI packages snapshots; Renderer produces identical semantic results in JSON and HTML.
5. Store verifies private access and pinned identities across writes and around final marker publication.
6. CLI emits completion and candidate status; lead reads report and makes their own decision.

### Error Handling

| Class / code | Behavior and recovery |
| --- | --- |
| Usage / E_USAGE | Exit 2; tagged zero-based argument index, or null for absent required option; fixed message without echoing tokens. |
| Parse/schema/version / E_SCHEMA | Exit 2; bounded location diagnostic; correct producer export. |
| Hash/reference/identity / E_INTEGRITY | Exit 2; reject entire comparison; preserve original input. |
| Different suite_id / E_SUITE | Exit 2; select correct suite/bundles; do not fuzzy-match. |
| Missing/stale/type/ineligible evidence | Complete report with unknown reason; obtain better evidence. |
| Rule mismatch | Complete report with fail; review agent/policy; not a parser error. |
| Imported error/timeout/skipped run | Unknown outcomes and explicit run state; export a new run. |
| Limits/deadline / E_LIMIT | Exit 4; no complete marker; split suite by reviewed scope. |
| I/O/mount/disk/permission / E_IO | Exit 4; null location if unlocatable; no success or path fallback. Preserve partial generation; retry only after verified recovery. |
| Unexpected implementation defect / E_INTERNAL | Exit 4; sanitized diagnostic, no successful report. |

Network failures: N/A for MVP; network access is not part of comparison. No automatic retries
of imports or tool calls; a rerun is explicit and cannot overwrite a complete generation.

### Complex Logic (if applicable)

Importer rejects invalid references before missing-evidence logic. Evaluator iterates the
reviewed expected set, not the intersection of bundles, then separately lists extras.
Matching case_hash is required for comparable outcomes; stable IDs alone are insufficient.
The contract defines exact aggregation, reason precedence, subject/time eligibility, and
evaluated coverage `(pass + fail)/expected` at case/assertion levels. Separate evidence coverage
is deferred; show unknown and defined assertion evidence-gap reason counts without a new ratio.

## Deployment View

### Single Application Deployment

Proposed local CLI execution on the observed arm64 Mac with a separately authorized external
owner-enabled APFS target; none is currently authorized/provisioned. Internal Mac storage is
not selected. Other platforms require separate proof. [B0](../../decisions/001-runtime.md) recommends CPython
3.14.10 and candidate rfc8785 0.1.4 for validation, not tested pins. Native bridge/build and
installer versions remain gated; the currently noowners pendrive is not a valid product target.
No required secrets/environment service. Explicit paths keep evidence and outputs local.
No package publication, installer, signed binary, server, or deployment currently exists.

### Multi-Component Coordination (if applicable)

N/A: one package, no distributed deployment. Schema/evaluator versions travel in reports.
Rollback selects an older compatible package and original inputs, producing a new generation;
never reinterpret a newer schema or rewrite the old report. AI remains disabled by absence.

## Cross-Cutting Concepts

### Pattern Documentation

Existing: [development](../../development.md), CRITICAL, exact delivery evidence and review.
Proposed: [contract](../../evidence-contract.md), CRITICAL, immutable provenance/tri-state rules;
[testing](../../testing.md), HIGH, independent expected outcomes and deterministic replay.

### User Interface & UX (if applicable)

Offline report order: candidate status and scope, failures/unknowns, evaluated coverage and
evidence-gap counts, changed sources,
case comparison, then evidence details. Text labels accompany colors; no percentage-only badge.
Proposed accessibility: semantic headings/tables, keyboard-readable links, sufficient contrast,
no script dependency. N/A: account navigation, design-system framework, live web state.

#### UI Visualization Guide

```text
ReleaseLens | imported evidence only | evaluator + input hashes
Candidate: UNKNOWN | 20 expected | 17 pass | 0 fail | 3 unknown
Coverage loss: 2 | changed definitions: 1 | extra cases: 1
Case | baseline | candidate | delta | reason | evidence
refund-7 | pass | unknown | incomparable | missing effect | refs
```

Illustrative values only. CLI states: validating → comparing → publishing → complete;
fatal errors exit without a complete marker. Static HTML needs no client-side state machine.

### System-Wide Patterns

Data-only parsing, escaped rendering, no embedded executable HTML/JS, no remote resources,
no credential lookup, and no telemetry. Verified owner-private filesystem access is required;
it is not encryption or protection from privileged/same-account access.
Log only counts, IDs, versions, reason codes, and durations; even IDs can be sensitive.
English UI initially; preserve original Unicode evidence without localization transformations.
Bounded single-process evaluation avoids background workers; performance targets require measurement.

### Multi-Component Patterns (if applicable)

N/A for distributed consistency, service discovery, circuit breakers, or tracing infrastructure.
In-process immutable values and bundle/result hashes correlate stages. No global mutable verdict state.

## Architecture Decisions

B0 research/direction was accepted in PR #11; the entries below track remaining architecture
gates, not a request to reapprove that research. The [B0a protocol](../../decisions/002-storage-protocol.md)
records proposed requirement decisions D1–D4 and untested storage obligations. Runtime work
cannot begin under open gates, and the AI deferral does not authorize AI implementation.

- [ ] ADR-1 Runtime/package: **conditionally recommend** CPython 3.14.10 modular CLI per
  [B0](../../decisions/001-runtime.md); **blocked** on JCS/native-storage/build validation.
  Python reduces tooling and exposes dir_fd operations; Node 26.13.1 has easier ECMAScript
  serialization but a larger native I/O gap. User confirmed: **Pending**.
- [ ] ADR-2 Storage/identity: propose JSON snapshots, RFC 8785 + SHA-256, explicit references,
  immutable reports instead of SQLite. Easy inspection/offline portability; larger duplicated
  files and bounded scale. **Recommended**, with parser/JCS conformance and numeric-token
  edge handling **blocked** pending validation; no relaxed JSON. User confirmed: **Pending**.
- [ ] ADR-3 Evaluation/authority: propose exact tri-state rules, pinned business sources,
  reviewed-suite denominator, no live execution. Avoids false certainty; manual exports and
  exporter authenticity remain user responsibilities. **Recommended**, no semantics change.
  User confirmed: **Pending**.
- [ ] ADR-4 Packaging/resources: propose local package, static HTML/JSON, contract bounds,
  60-second deadline and no hosted service. Low operating cost; slower onboarding and no
  shared dashboard. **Blocked**: B0's noowners mount observation and unproven native bridge,
  effective-access, mount-race/publication and deadline guarantees prevent readiness.
  Unsupported volumes fail closed; T-09 remains required. User confirmed: **Pending**.
- [ ] ADR-5 AI/agent boundary: propose defer until deterministic pilot evidence. Later compare
  local runtime/model candidates or existing customer-owned inference at zero incremental
  founder cost; no model/runtime, license, quantization, context window, or capability selected.
  **Deferred** beyond deterministic/pilot gates; this is the recommended MVP disposition.
  Grounded explanations may help triage but add nondeterminism and evaluation work. No agent
  business authority; any expansion requires a new approved ADR. User confirmed: **Pending**.

## Quality Requirements

All targets proposed and unmeasured. Q1: identical Result hashes across 10 identical runs
(T-06). Q2: no missing-evidence pass in reviewed negative corpus (T-03/04/05). Q3: 100-case,
10-assertion/case, <=10 MiB total input comparison <=10 seconds and <=512 MiB peak RSS in
10 trials on the observed Mac (T-08); record cold/warm disk conditions, not just averages.
Q4: enforce contract limits/60-second deadline with no complete partial report (T-08/09).
Q5: zero outbound requests and zero script execution during comparison/report inspection
(T-07). Q6: first synthetic comparison <=15 minutes, triage <=10 minutes in four of six
pilot sessions (T-10). Q7: costs $0 new hosting/inference (T-12); no paid CI expansion.

## Acceptance Criteria

- [ ] WHEN a reviewed suite is supplied, THE SYSTEM SHALL validate identity, sources, hashes,
  and reference integrity before evaluating (RL-001, RL-002, RL-003; T-01/02).
- [ ] IF evidence is insufficient, THEN THE SYSTEM SHALL preserve unknown and distinguish
  tool request, completion, and eligible same-record subject/value evidence (RL-004, RL-005; T-03/04).
- [ ] WHEN comparing imports, THE SYSTEM SHALL retain every expected case and expose
  missing/changed/extra cases and candidate failures (RL-006, RL-007; T-05).
- [ ] WHEN output completes, THE SYSTEM SHALL provide offline evidence-backed HTML/JSON
  with exact namespace-qualified citations, evaluated coverage, defined evidence-gap counts,
  and deterministic semantic identity (RL-008, RL-009; T-06/07).
- [ ] WHILE importing/rendering, THE SYSTEM SHALL treat all input as bounded inert data
  and publish only complete generations (RL-010, RL-011; T-07/08/09).
- [ ] THE SYSTEM SHALL support documented local recovery without new inference/hosting
  spend (RL-012; T-09/10/12).
- [ ] WHERE future AI is enabled after approval, THE SYSTEM SHALL cite evidence, abstain
  when unsupported, and remain within reviewed authority (RL-013, RL-014; T-11).

## Risks and Technical Debt

### Known Technical Issues

No product defects can be measured before implementation. Design risks: forged exports,
misleading source labels, incomplete traces, contradictory policy versions, and narrow rules
that miss semantic regressions. Hash integrity cannot cure these; pilot review must expose them.

### Technical Debt

No inherited application debt. Proposed deliberate limitations: manual import format,
single attempt/case, no incremental store, exact string rules, and no multi-user workflow.
Revisit only with measured pilot friction; avoid premature SDK/vendor abstractions.

### Implementation Gotchas

Reject duplicate JSON keys before ordinary parsing loses them. Null evidence differs from a
reference to a null JSON value. Case hashes bind referenced source metadata, not only text.
Filesystem rename/flush behavior on the mounted volume needs verification; a marker is not
a backup. Redaction changes hashes. Sorting report rows must not reorder source event arrays.

## Glossary

### Domain Terms

| Term | Definition | Context |
| --- | --- | --- |
| Baseline / candidate | Imported outputs before / after a change | No live execution implied. |
| Verified effect | Rule satisfied against eligible imported business evidence | Exporter authenticity remains unverified. |
| Unknown | Insufficient eligible evidence for a verdict | Never counted as pass. |

### Technical Terms

| Term | Definition | Context |
| --- | --- | --- |
| JCS | RFC 8785 JSON Canonicalization Scheme | Semantic content hashing. |
| Generation | New immutable report directory | Completion marker identifies finished output. |

### API/Interface Terms

| Term | Definition | Context |
| --- | --- | --- |
| Ref | Artifact ID plus exact JSON pointer or text selector | No network/path dereference. |
| Proposed CLI | Unimplemented command grammar | Not an available project command. |
