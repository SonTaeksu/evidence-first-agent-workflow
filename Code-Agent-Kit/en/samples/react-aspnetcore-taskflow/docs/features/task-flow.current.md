---
feature: task-flow
status: stable
code-verified: "2026-07-14 @uncommitted-release-candidate"
last-pr: "none"
updated: "2026-07-14T00:00:00Z"
stack: react-aspnetcore
---

# Feature Current State — Task Flow

> Mandatory starting state for every later Task Flow modification.

## Current Behavior

- Lists tasks.
- Creates tasks with title, description, and assignee.
- Enforces controlled status transitions.
- Supports approval and rejection paths.
- Displays loading, empty, error, and status-action states.

## Feature Boundary and Actions

- Boundary: one vertical Task Flow slice spanning frontend UI, JSON REST API, domain rules, repository, and tests.
- Actions: list, create, start, submit for approval, approve, reject, and resume rejected work.
- Approved is terminal.

## Contracts

| Contract | Direction | Definition |
|---|---|---|
| task list | API → frontend | `TaskItemResponse` ↔ frontend `TaskItem` |
| create task | frontend → API | `CreateTaskRequest` |
| update status | frontend → API | `UpdateTaskStatusRequest` |
| error | API → frontend | established problem response |

## Related Files by Role

### Entry Points

- `frontend/src/App.tsx` — feature state and UI composition
- `backend/TaskFlow.Api/Program.cs` — API endpoints

### Contracts

- `frontend/src/types.ts`
- `frontend/src/api.ts`
- `backend/TaskFlow.Api/Contracts/`

### Implementation

- `frontend/src/components/TaskForm.tsx`
- `frontend/src/components/TaskList.tsx`
- `backend/TaskFlow.Api/Domain/`
- `backend/TaskFlow.Api/Repositories/`

### Validation

- `frontend/src/App.test.tsx`
- `frontend/e2e/taskflow.spec.ts`
- `frontend/e2e/color-gate.spec.ts`
- `backend/TaskFlow.Api.Tests/TaskApiTests.cs`
- `scripts/validate.ps1`
- `scripts/validate.sh`

## Shared Dependencies

| Shared File or Service | Other Features | Risk | Required Regression |
|---|---|---|---|
| `frontend/src/api.ts` | future API-backed features | contract/client | TypeScript, component, E2E |
| `frontend/src/styles.css` | all sample UI | visual regression | static color, runtime color, screenshot review |
| `backend/TaskFlow.Api/Program.cs` | all sample endpoints | routing/error contract | backend integration tests |

## Environment Capability Decisions

| Capability | Status | Evidence | Selected Path |
|---|---|---|---|
| frontend shared API client | present | `frontend/src/api.ts` | reuse module |
| generated OpenAPI client | absent | stack capability profile | typed manual adapter |
| backend style | present | Minimal API in `Program.cs` | preserve Minimal API |
| data access | present | in-memory repository | preserve sample repository |
| authentication | not-applicable | public sample scope | no auth assumptions |

## Validation State

| Layer | Result | Evidence |
|---|---|---|
| Artifact / Compile | baseline PASS v0.1.3; v0.1.5 PENDING | generated evidence |
| Rendered Output | tool self-tests PASS; app runtime PENDING | SPA and visual-block tools |
| Runtime Behavior | PENDING local/CI | Playwright and backend tests |
| Accessibility / Color | static PASS; runtime PENDING | contrast evidence |

## Known Issues

- Data resets when the API restarts.
- Production persistence, authentication, and deployment policy are outside this sample.
- Backend and browser runtime require local or CI validation.

## Next Candidate Work

1. Priority field experiment.
2. Persistence adapter experiment.
3. Authentication remains blocked until an owner-defined policy exists.
