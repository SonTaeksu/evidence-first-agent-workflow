# Design Example: Add Task Priority

> This is an experiment template, not an implemented feature.

## Request

Add task priority with `Low`, `Normal`, and `High` values. Allow selecting priority during creation and show it on each task card.

## Current Evidence

- Task creation contract: `backend/TaskFlow.Api/Contracts/CreateTaskRequest.cs`
- Domain entity: `backend/TaskFlow.Api/Domain/TaskItem.cs`
- Response contract: `backend/TaskFlow.Api/Contracts/TaskItemResponse.cs`
- Frontend type: `frontend/src/types.ts`
- Form: `frontend/src/components/TaskForm.tsx`
- Card: `frontend/src/components/TaskList.tsx`

## Assumptions

- Default priority is `Normal`.
- Priority does not affect status transitions.
- Existing seed items use `Normal`.

## Out of Scope

- priority filtering;
- sorting by priority;
- database persistence;
- per-user priority policy.

## Impact

The API and frontend contract both change. Tests and Project Map must be updated.

## Expected Files

- `backend/TaskFlow.Api/Domain/TaskPriority.cs`
- `backend/TaskFlow.Api/Domain/TaskItem.cs`
- `backend/TaskFlow.Api/Contracts/CreateTaskRequest.cs`
- `backend/TaskFlow.Api/Contracts/TaskItemResponse.cs`
- `backend/TaskFlow.Api/Repositories/InMemoryTaskRepository.cs`
- `backend/TaskFlow.Api.Tests/TaskApiTests.cs`
- `frontend/src/types.ts`
- `frontend/src/components/TaskForm.tsx`
- `frontend/src/components/TaskList.tsx`
- `frontend/src/styles.css`
- `frontend/src/App.test.tsx`
- `frontend/e2e/taskflow.spec.ts`
- `docs/current.md`
- `docs/history.md`
- `docs/project-map.md`

## Tasks

1. Add backend priority enum and contract.
2. Add frontend priority type and input.
3. Display priority on cards.
4. Update tests.
5. Validate.
6. Update state documents.

## Todos

- [ ] Verify React controlled-select guidance through Context7.
- [ ] Verify ASP.NET Core enum JSON behavior through Microsoft Learn.
- [ ] Implement backend.
- [ ] Implement frontend.
- [ ] Update tests.
- [ ] Run full validation.
- [ ] Review final Git Diff.

## Validation Checklist

- [ ] New task defaults or submits priority correctly.
- [ ] API returns priority as a string.
- [ ] UI displays priority.
- [ ] existing status workflow still works.
- [ ] all deterministic validation passes.
- [ ] unexpected file changes have documented reason and impact.
