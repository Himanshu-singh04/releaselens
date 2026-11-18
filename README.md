# ReleaseLens

**See what changed before shipping.**

Local-first regression testing for AI support agents after changes to policies, prompts, models, or tools.

## Initial goal

Compare a baseline and candidate agent against reviewed scenarios and produce an evidence-backed local report. Distinguish tool requests, completed calls, and verified business effects; missing evidence must remain explicit.

## Status

Repository initialized. Product design, implementation, and the dedicated OpenCode project session are pending. No application or test commands exist yet.

## Development workspace

Local checkout: `/Volumes/AIWorkspace/projects/releaselens`.

Execution will use existing local or customer-owned resources, with no new initial founder hosting or inference expenditure. This product has an independent repository and release lifecycle.

## Git workflow

- Commit source, documentation, reviewed fixtures, and dependency lockfiles.
- Keep credentials, OpenCode databases, model weights, caches, and raw customer evidence outside Git.
- Complete a bounded task, run its relevant checks, inspect the diff, then commit and push the intended files.
- Report the commit and push result to the coordinator. A local commit is not a remote backup until the push succeeds.
- Use task branches for substantive implementation work and preserve unrelated changes.

Detailed plans and project-specific working instructions will follow during project planning.
