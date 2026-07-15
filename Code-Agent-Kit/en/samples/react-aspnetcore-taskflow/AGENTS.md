# TaskFlow Sample Agent Rules

Follow repository root `AGENTS.md` and `stacks/react-aspnetcore/AGENTS.stack.md`.

## Feature routing

Task Flow work starts with:

1. `docs/project-map.md`
2. `docs/features/task-flow.current.md`
3. current's Related Files and Shared Dependencies
4. active worklog when unfinished

Project-level `docs/current.md` is a summary and does not replace feature current.

## Capability prohibitions

- Reuse `frontend/src/api.ts`; do not create a second API client.
- Preserve Minimal API unless Project Map records a confirmed replacement.
- Do not introduce database, authentication, generated clients, state libraries, or design systems while the capability is unknown.

## Source-driven UI

- Images require a Reference Image Manifest.
- SPA references require rendered-DOM extraction.
- Compare reference and implementation screen specifications.
- Missing or empty grids, rows, controls, buttons, KPI cards, charts, matrices, panels, or required visual blocks fail the task.

## Validation

Run the stack profile:

- stack readiness;
- frontend type check, tests, and build;
- backend restore, build, and tests;
- rendered-output completeness;
- E2E runtime;
- color and accessibility;
- Git scope and state-model validation.

Record commands and exit codes. Unexecuted checks are PENDING.

## Completion

- update `docs/features/task-flow.current.md` with the verified commit;
- append `docs/features/task-flow.history.md`;
- update `docs/project-map.md`, including Shared File Reverse Index;
- update project summary only when project-level state changes;
- close or archive the worklog;
- review final Git Diff.
