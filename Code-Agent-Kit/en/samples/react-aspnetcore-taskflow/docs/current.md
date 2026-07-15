---
scope: project-summary
status: active
code-verified: "2026-07-14 @uncommitted-release-candidate"
last-pr: "none"
updated: "2026-07-14T00:00:00Z"
---

# Current Project State

> Project summary only. Feature changes start from the feature current document routed by Project Map.

## Project Purpose

- Demonstrate the Evidence-First workflow with React and ASP.NET Core.
- Keep stack knowledge separate from the governance core.
- Provide deterministic frontend, backend, browser, color, source-asset, scope, and state gates.

## Features

| Feature | Current | History | Active Worklog |
|---|---|---|---|
| task-flow | `features/task-flow.current.md` | `features/task-flow.history.md` | none |

## Architecture State

- System: `architecture/system.current.md`
- Database: `architecture/database.current.md`

## Project Validation Summary

- Python workflow tools: PASS
- Stack readiness: PASS
- Static CSS contrast: PASS, 18/18
- Reference image self-test: PASS
- SPA structure and empty visual-block self-test: PASS
- Frontend v0.1.3 baseline: PASS
- Frontend v0.1.5 fresh install/build: PENDING local or CI
- Backend restore/build/test: PENDING local or CI
- Browser runtime and axe: PENDING local or CI
- Docker: PENDING local or CI

## Known Project Constraints

- Public sample uses an in-memory repository.
- Authentication and production database policy are intentionally not defined.
- Adopted projects must complete their own Stack Inputs and Capability Decisions.

## Next Project Actions

1. Run the full pre-commit validation on a machine with Node, .NET 10, Playwright Chromium, and Docker.
2. Record the resulting commit in project and feature current.
3. Run the priority-field experiment from a new worklog.
