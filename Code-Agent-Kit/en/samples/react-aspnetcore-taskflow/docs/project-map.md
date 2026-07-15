# Project Map

## Project Summary

- Repository: React + ASP.NET Core TaskFlow sample
- Default branch: repository default
- Primary stack: `stacks/react-aspnetcore`
- Project current: `current.md`
- Last map verification: 2026-07-14

## Features

| Feature Key | Current | History | Active Worklog | Entry Points | Stack |
|---|---|---|---|---|---|
| task-flow | `features/task-flow.current.md` | `features/task-flow.history.md` | none | `frontend/src/App.tsx`, `backend/TaskFlow.Api/Program.cs` | react-aspnetcore |

## Architecture State

| Area | Current | History |
|---|---|---|
| System | `architecture/system.current.md` | `architecture/system.history.md` |
| Database | `architecture/database.current.md` | `architecture/database.history.md` |

## Environment Capabilities

| Capability | Status | Evidence | Selected Path | Verified |
|---|---|---|---|---|
| frontend shared API client | present | `frontend/src/api.ts` | reuse module | 2026-07-14 |
| generated OpenAPI client | absent | stack profile | typed manual adapter | 2026-07-14 |
| backend style | present | `backend/TaskFlow.Api/Program.cs` | Minimal API | 2026-07-14 |
| data access | present | `InMemoryTaskRepository.cs` | in-memory sample | 2026-07-14 |
| authentication | not-applicable | public sample scope | no auth assumptions | 2026-07-14 |

## Shared File Reverse Index

| Shared File | Used By Features | Risk | Required Regression |
|---|---|---|---|
| `frontend/src/api.ts` | task-flow, future API features | API contract/client | TypeScript, component, E2E |
| `frontend/src/types.ts` | task-flow, future API features | shared type contract | frontend build and E2E |
| `frontend/src/styles.css` | all frontend features | visual regression | color gates and screenshot review |
| `backend/TaskFlow.Api/Program.cs` | all API features | routing and error shape | backend integration tests |
| `backend/TaskFlow.Api/Contracts/` | task-flow, future clients | data contract | backend, frontend, E2E |

## Global Entry Points

- UI: `frontend/src/main.tsx`
- API: `backend/TaskFlow.Api/Program.cs`
- Tests: frontend, backend tests, and Playwright
- Validation: `scripts/validate.ps1`, `scripts/validate.sh`

## Evidence and Tool Routing

- Reference image: `../../tools/reference-image-manifest/`
- SPA structure: `../../tools/spa-screen-extractor/`
- Stack readiness: `../../tools/check-stack-readiness/`
- Git scope: `../../tools/check-git-scope/`
- Document sync: `../../tools/check-document-sync/`
