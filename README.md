# ReleaseLens

**See what changed before shipping.**

Local-first regression testing for AI support agents after changes to policies, prompts, models, or tools.

## Initial goal

Compare a baseline and candidate agent against reviewed scenarios and produce an evidence-backed local report. Distinguish tool requests, completed calls, and verified business effects; missing evidence must remain explicit.

## Status

Repository foundation checks exist. The planning set merged in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6), and App-rename corrections merged in [PR #8](https://github.com/Himanshu-singh04/releaselens/pull/8). [B0 research](docs/decisions/001-runtime.md) was conditionally accepted in PR #11; product pins and M0 remain unvalidated. [B0a storage documentation](docs/decisions/002-storage-protocol.md) was accepted in [PR #13](https://github.com/Himanshu-singh04/releaselens/pull/13); customer implementation remains NO-GO. [B0b JSON/JCS research](docs/decisions/003-json-conformance.md) exercises finite synthetic vectors on installed Python. No application commands, product tests, model integration, or release artifacts exist.

The accepted [B0c packet](docs/decisions/004-mvp-decision.md) is historical. The founder later
adopted exact N1–N4 and a synthetic-terminal scope/sequence exception with AI deferred;
[B0d](docs/decisions/005-adopted-policy-reconciliation.md) records those decisions and this
pending normative reconciliation. Enforcement and runtime qualification remain unverified.
Only separately authorized synthetic work can use the exception; customer implementation stays
blocked. D1–D4 remain unadopted, noowners storage ineligible, and M0/M1–M4 incomplete.

## Product planning

- [Product requirements](docs/product.md): user workflow, stable requirement IDs, scope, and demand/pricing hypotheses.
- [MVP solution design](docs/specs/001-mvp/solution-design.md): proposed architecture, interfaces, pending ADRs, and acceptance mapping.
- [Evidence contract](docs/evidence-contract.md): provenance, reference integrity, tri-state results, and comparison coverage.
- [Roadmap](docs/roadmap.md): ordered milestones and bounded proposed tasks.
- [Testing and evaluation](docs/testing.md): planned product checks, AI gates, and unmeasured targets.
- [Local operations](docs/operations.md): actual storage placement, proposed packaging, recovery, and cost constraints.
- [B0 runtime recommendation](docs/decisions/001-runtime.md): Python/Node comparison, observed storage blocker, candidate pins and pending ADR dispositions.
- [B0a storage protocol](docs/decisions/002-storage-protocol.md): proposed native ABI, target eligibility, fault matrix and explicit no-go guarantees.
- [Adopted policy and reconciliation](docs/decisions/005-adopted-policy-reconciliation.md): exact authority, clause/file trace, synthetic exception and retained customer gates.

## Development workspace

Local checkout: `/Volumes/AIWorkspace/projects/releaselens`.

Execution will use existing local or customer-owned resources, with no new initial founder hosting or inference expenditure. This product has an independent repository and release lifecycle.

Source and docs are on the pendrive; execution uses Mac CPU/RAM. The persistent development worker and restart/routing continuity are verified in [issue #9](https://github.com/Himanshu-singh04/releaselens/issues/9). Worker history and OpenAI OAuth share the pendrive database outside Git by explicit founder decision; coordinator history and the GitHub App key remain on the Mac. Authenticated localhost API access does not establish filesystem confidentiality: other-account database access is untested, and ownership-based privacy cannot be assumed on this `noowners` mount. Development inference uses the existing subscription allowance; it is not product-local inference. See [operations](docs/operations.md) for paths and limits. No product model/runtime is installed or approved by this provisioning record.

## Git workflow

See [contributing](CONTRIBUTING.md), [development and delivery](docs/development.md),
and the [foundation record](docs/foundation.md) for checks, authenticated review,
agent attribution, and evidence requirements.

- Commit source, documentation, reviewed fixtures, and dependency lockfiles.
- Keep credentials, OpenCode databases, model weights, caches, and raw customer evidence outside Git.
- Complete a bounded task, run its relevant checks, inspect the diff, then commit and push the intended files.
- Report the commit and push result to the coordinator. A local commit is not a remote backup until the push succeeds.
- Use task branches for substantive implementation work and preserve unrelated changes.

Foundation checks are in [CONTRIBUTING](CONTRIBUTING.md); finite [B0b research controls](docs/decisions/003-json-conformance.md) have separate reproduction commands. Proposed product interfaces in the planning documents are not runnable commands.
