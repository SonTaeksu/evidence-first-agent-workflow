# Project Map

## Project Summary

- Repository: React + ASP.NET Core TaskFlow Sample
- Default Branch: Repository Default
- Primary Stack: `stacks/react-aspnetcore`
- Project Current: `current.md`
- Last Map Verification: 2026-07-14

## Features

| Feature Key | Current | History | Active Worklog | Entry Points | Stack |
|---|---|---|---|---|---|
| task-flow | `features/task-flow.current.md` | `features/task-flow.history.md` | 없음 | `frontend/src/App.tsx`, `backend/TaskFlow.Api/Program.cs` | react-aspnetcore |

## Architecture State

| 영역 | Current | History |
|---|---|---|
| System | `architecture/system.current.md` | `architecture/system.history.md` |
| Database | `architecture/database.current.md` | `architecture/database.history.md` |

## Environment Capabilities

| Capability | 상태 | Evidence | 선택 경로 | Verified |
|---|---|---|---|---|
| Frontend Shared API Client | present | `frontend/src/api.ts` | 기존 Module 재사용 | 2026-07-14 |
| Generated OpenAPI Client | absent | Stack Profile | Typed Manual Adapter | 2026-07-14 |
| Backend Style | present | `backend/TaskFlow.Api/Program.cs` | Minimal API | 2026-07-14 |
| Data Access | present | `InMemoryTaskRepository.cs` | In-memory Sample | 2026-07-14 |
| Authentication | not-applicable | 공개 Sample Scope | Auth 가정 없음 | 2026-07-14 |

## Shared File Reverse Index

| Shared File | 사용하는 Feature | Risk | 필요한 Regression |
|---|---|---|---|
| `frontend/src/api.ts` | task-flow, 향후 API Feature | API Contract/Client | TypeScript, Component, E2E |
| `frontend/src/types.ts` | task-flow, 향후 API Feature | Shared Type Contract | Frontend Build 및 E2E |
| `frontend/src/styles.css` | 전체 Frontend Feature | Visual Regression | Color Gate 및 Screenshot Review |
| `backend/TaskFlow.Api/Program.cs` | 전체 API Feature | Routing 및 Error Shape | Backend Integration Test |
| `backend/TaskFlow.Api/Contracts/` | task-flow, 향후 Client | Data Contract | Backend, Frontend, E2E |

## Global Entry Points

- UI: `frontend/src/main.tsx`
- API: `backend/TaskFlow.Api/Program.cs`
- Test: Frontend, Backend Test, Playwright
- Validation: `scripts/validate.ps1`, `scripts/validate.sh`

## Evidence 및 Tool Routing

- Reference Image: `../../tools/reference-image-manifest/`
- SPA 구조: `../../tools/spa-screen-extractor/`
- Stack Readiness: `../../tools/check-stack-readiness/`
- Git Scope: `../../tools/check-git-scope/`
- Document Sync: `../../tools/check-document-sync/`
