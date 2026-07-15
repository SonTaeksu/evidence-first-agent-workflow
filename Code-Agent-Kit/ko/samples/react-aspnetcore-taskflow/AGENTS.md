# TaskFlow Sample Agent Rule

Repository Root `AGENTS.md`와 `stacks/react-aspnetcore/AGENTS.stack.md`를 따릅니다.

## Feature Routing

Task Flow 작업 시작:

1. `docs/project-map.md`
2. `docs/features/task-flow.current.md`
3. Current의 Related Files와 Shared Dependencies
4. 미완료 작업이면 Active Worklog

Project-level `docs/current.md`는 Summary이며 Feature Current를 대체하지 않습니다.

## Capability 금지

- `frontend/src/api.ts`를 재사용하고 두 번째 API Client를 만들지 않습니다.
- Project Map에 확인된 대체 경로가 없으면 Minimal API를 유지합니다.
- Database, Authentication, Generated Client, State Library, Design System Capability가 Unknown이면 도입하지 않습니다.

## Source 기반 UI

- Image는 Reference Image Manifest가 필요합니다.
- SPA Reference는 Rendered DOM 추출이 필요합니다.
- Reference와 구현 Screen Specification을 비교합니다.
- 필수 Grid, Row, Control, Button, KPI Card, Chart, Matrix, Panel, Visual Block이 없거나 비어 있으면 실패합니다.

## Validation

Stack Profile을 실행합니다.

- Stack Readiness
- Frontend Type Check, Test, Build
- Backend Restore, Build, Test
- Rendered Output 완전성
- E2E Runtime
- Color 및 Accessibility
- Git Scope 및 State Model Validation

명령과 Exit Code를 기록합니다. 실행하지 않은 검사는 PENDING입니다.

## 완료

- 검증 Commit을 `docs/features/task-flow.current.md`에 기록
- `docs/features/task-flow.history.md` Append
- Shared File Reverse Index를 포함해 `docs/project-map.md` 갱신
- Project-level State가 바뀐 경우에만 Project Summary 갱신
- Worklog 종료 또는 Archive
- 최종 Git Diff 검토
