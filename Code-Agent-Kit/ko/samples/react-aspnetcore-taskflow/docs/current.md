---
scope: project-summary
status: active
code-verified: "2026-07-14 @uncommitted-release-candidate"
last-pr: "none"
updated: "2026-07-14T00:00:00Z"
---

# Current Project State

> Project Summary입니다. Feature 변경은 Project Map이 Routing하는 Feature Current에서 시작합니다.

## Project 목적

- React 및 ASP.NET Core로 Evidence-First Workflow 시연
- Stack Knowledge와 Governance Core 분리
- Frontend, Backend, Browser, Color, Source Asset, Scope, State의 결정론적 Gate 제공

## Features

| Feature | Current | History | Active Worklog |
|---|---|---|---|
| task-flow | `features/task-flow.current.md` | `features/task-flow.history.md` | 없음 |

## Architecture State

- System: `architecture/system.current.md`
- Database: `architecture/database.current.md`

## Project Validation 요약

- Python Workflow Tool: PASS
- Stack Readiness: PASS
- 정적 CSS Contrast: PASS, 18/18
- Reference Image Self-test: PASS
- SPA 구조 및 빈 Visual Block Self-test: PASS
- Frontend v0.1.3 기준선: PASS
- Frontend v0.1.5 새 Install/Build: Local 또는 CI PENDING
- Backend Restore/Build/Test: Local 또는 CI PENDING
- Browser Runtime 및 axe: Local 또는 CI PENDING
- Docker: Local 또는 CI PENDING

## Known Project 제약

- 공개 Sample은 In-memory Repository 사용
- Authentication 및 Production Database Policy는 의도적으로 미정의
- 적용 Project는 자체 Stack Inputs와 Capability Decision을 완료해야 함

## 다음 Project 작업

1. Node, .NET 10, Playwright Chromium, Docker가 있는 환경에서 전체 Pre-commit Validation
2. 결과 Commit을 Project 및 Feature Current에 기록
3. 새 Worklog에서 Priority-field 실험 실행
