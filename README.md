# ReleaseLens

**See what changed before shipping.**

Local-first regression testing for AI support agents after changes to policies, prompts, models, or tools.

## Initial goal

Compare a baseline and candidate agent against reviewed scenarios and produce an evidence-backed local report. Distinguish tool requests, completed calls, and verified business effects; missing evidence must remain explicit.

## Status

Repository foundation checks exist. The planning set merged in [PR #6](https://github.com/Himanshu-singh04/releaselens/pull/6), and App-rename corrections merged in [PR #8](https://github.com/Himanshu-singh04/releaselens/pull/8). [B0 research merged in PR #11](https://github.com/Himanshu-singh04/releaselens/pull/11): the Python/JCS/native-bridge direction is conditionally accepted, not validated product pins or M0 completion. [B0a / issue #12](https://github.com/Himanshu-singh04/releaselens/issues/12) specifies the storage protocol; implementation remains NO-GO. No application commands, product tests, model integration, or release artifacts exist.

## Product planning

- [Product requirements](docs/product.md): user workflow, stable requirement IDs, scope, and demand/pricing hypotheses.
- [MVP solution design](docs/specs/001-mvp/solution-design.md): proposed architecture, interfaces, pending ADRs, and acceptance mapping.
- [Evidence contract](docs/evidence-contract.md): provenance, reference integrity, tri-state results, and comparison coverage.
- [Roadmap](docs/roadmap.md): ordered milestones and bounded proposed tasks.
- [Testing and evaluation](docs/testing.md): planned product checks, AI gates, and unmeasured targets.
- [Local operations](docs/operations.md): actual storage placement, proposed packaging, recovery, and cost constraints.
- [B0 runtime recommendation](docs/decisions/001-runtime.md): Python/Node comparison, observed storage blocker, candidate pins and pending ADR dispositions.

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

Only foundation checks are available today; use the commands in [CONTRIBUTING](CONTRIBUTING.md). Proposed product interfaces in the planning documents are not runnable commands.
