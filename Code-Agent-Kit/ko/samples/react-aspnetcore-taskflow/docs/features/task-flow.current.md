---
feature: task-flow
status: stable
code-verified: "2026-07-14 @uncommitted-release-candidate"
last-pr: "none"
updated: "2026-07-14T00:00:00Z"
stack: react-aspnetcore
---

# Feature Current State — Task Flow

> 이후 모든 Task Flow 수정 작업의 필수 시작 State입니다.

## Current Behavior

- Task 목록
- Title, Description, Assignee로 Task 생성
- 통제된 Status Transition
- Approve 및 Reject 경로
- Loading, Empty, Error, Status Action State 표시

## Feature Boundary 및 Action

- Boundary: Frontend UI, JSON REST API, Domain Rule, Repository, Test를 포함한 Vertical Task Flow Slice
- Action: List, Create, Start, Approval 제출, Approve, Reject, Rejected Resume
- Approved는 Terminal

## Contracts

| Contract | 방향 | 정의 |
|---|---|---|
| Task List | API → Frontend | `TaskItemResponse` ↔ Frontend `TaskItem` |
| Create Task | Frontend → API | `CreateTaskRequest` |
| Update Status | Frontend → API | `UpdateTaskStatusRequest` |
| Error | API → Frontend | 기존 Problem Response |

## 역할별 Related Files

### Entry Points

- `frontend/src/App.tsx` — Feature State 및 UI Composition
- `backend/TaskFlow.Api/Program.cs` — API Endpoint

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

| Shared File 또는 Service | 다른 Feature | Risk | 필요한 Regression |
|---|---|---|---|
| `frontend/src/api.ts` | 향후 API Feature | Contract/Client | TypeScript, Component, E2E |
| `frontend/src/styles.css` | 전체 Sample UI | Visual Regression | Static Color, Runtime Color, Screenshot Review |
| `backend/TaskFlow.Api/Program.cs` | 전체 Sample Endpoint | Routing/Error Contract | Backend Integration Test |

## Environment Capability Decisions

| Capability | 상태 | Evidence | 선택 경로 |
|---|---|---|---|
| Frontend Shared API Client | present | `frontend/src/api.ts` | 기존 Module 재사용 |
| Generated OpenAPI Client | absent | Stack Capability Profile | Typed Manual Adapter |
| Backend Style | present | `Program.cs` Minimal API | Minimal API 유지 |
| Data Access | present | In-memory Repository | Sample Repository 유지 |
| Authentication | not-applicable | 공개 Sample Scope | Auth 가정 없음 |

## Validation State

| Layer | 결과 | Evidence |
|---|---|---|
| Artifact / Compile | v0.1.3 기준선 PASS, v0.1.5 PENDING | 생성 Evidence |
| Rendered Output | Tool Self-test PASS, App Runtime PENDING | SPA 및 Visual Block Tool |
| Runtime Behavior | Local/CI PENDING | Playwright 및 Backend Test |
| Accessibility / Color | Static PASS, Runtime PENDING | Contrast Evidence |

## Known Issues

- API Restart 시 Data Reset
- Production Persistence, Authentication, Deployment Policy는 Sample 범위 밖
- Backend 및 Browser Runtime은 Local 또는 CI Validation 필요

## Next Candidate Work

1. Priority Field 실험
2. Persistence Adapter 실험
3. Authentication은 Owner Policy가 정의되기 전까지 Block
