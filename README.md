# ReleaseLens

**See what changed before shipping.**

Local-first regression testing for AI support agents after changes to policies, prompts, models, or tools.

## Initial goal

Compare a baseline and candidate agent against reviewed scenarios and produce an evidence-backed local report. Distinguish tool requests, completed calls, and verified business effects; missing evidence must remain explicit.

## Status

Repository foundation checks exist. The product planning set for [issue #5](https://github.com/Himanshu-singh04/releaselens/issues/5) is a draft for owner confirmation on the documentation PR. Architecture decisions remain pending; implementation must not start under unresolved gates. No application commands, product tests, model integration, or release artifacts exist.

## Product planning

- [Product requirements](docs/product.md): user workflow, stable requirement IDs, scope, and demand/pricing hypotheses.
- [MVP solution design](docs/specs/001-mvp/solution-design.md): proposed architecture, interfaces, pending ADRs, and acceptance mapping.
- [Evidence contract](docs/evidence-contract.md): provenance, reference integrity, tri-state results, and comparison coverage.
- [Roadmap](docs/roadmap.md): ordered milestones and bounded proposed tasks.
- [Testing and evaluation](docs/testing.md): planned product checks, AI gates, and unmeasured targets.
- [Local operations](docs/operations.md): actual storage placement, proposed packaging, recovery, and cost constraints.

## Development workspace

Local checkout: `/Volumes/AIWorkspace/projects/releaselens`.

Execution will use existing local or customer-owned resources, with no new initial founder hosting or inference expenditure. This product has an independent repository and release lifecycle.

Source and docs are on the pendrive; execution uses Mac CPU/RAM. Coordinator and all current session history remain at `/Users/himanshusingh/.local/share/opencode/opencode.db`; credentials stay on the Mac. Model/cache directories exist but redirection is not configured. Persistent project servers/workers are not provisioned; future history routing needs restart, mount, and effective-path verification.

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
