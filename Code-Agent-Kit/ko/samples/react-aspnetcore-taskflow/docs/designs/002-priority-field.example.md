# 설계 예제: 작업 우선순위 추가

> 이 문서는 실험용 템플릿이며 아직 구현된 기능이 아닙니다.

## 요청

`Low`, `Normal`, `High` 값을 가진 작업 우선순위를 추가합니다. 작업 생성 시 우선순위를 선택할 수 있고 각 작업 카드에 표시합니다.

## 현재 증거

- 작업 생성 Contract: `backend/TaskFlow.Api/Contracts/CreateTaskRequest.cs`
- Domain Entity: `backend/TaskFlow.Api/Domain/TaskItem.cs`
- Response Contract: `backend/TaskFlow.Api/Contracts/TaskItemResponse.cs`
- Frontend Type: `frontend/src/types.ts`
- Form: `frontend/src/components/TaskForm.tsx`
- Card: `frontend/src/components/TaskList.tsx`

## 가정

- 기본 Priority는 `Normal`입니다.
- Priority는 Status Transition에 영향을 주지 않습니다.
- 기존 Seed Item은 `Normal`을 사용합니다.

## 제외 범위

- Priority Filter
- Priority Sort
- Database Persistence
- 사용자별 Priority 정책

## 영향

API와 Frontend Contract가 모두 변경됩니다. Test와 Project Map도 갱신해야 합니다.

## 예상 파일

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

1. Backend Priority Enum과 Contract를 추가합니다.
2. Frontend Priority Type과 입력을 추가합니다.
3. Card에 Priority를 표시합니다.
4. Test를 갱신합니다.
5. Validation을 수행합니다.
6. State Document를 갱신합니다.

## Todos

- [ ] Context7로 React Controlled Select 안내 확인
- [ ] Microsoft Learn으로 ASP.NET Core Enum JSON 동작 확인
- [ ] Backend 구현
- [ ] Frontend 구현
- [ ] Test 갱신
- [ ] 전체 Validation 실행
- [ ] 최종 Git Diff 검토

## Validation Checklist

- [ ] 새 작업의 기본값 또는 전달한 Priority가 정확하다.
- [ ] API가 Priority를 문자열로 반환한다.
- [ ] UI에 Priority가 표시된다.
- [ ] 기존 Status Workflow가 계속 동작한다.
- [ ] 모든 결정론적 Validation이 통과한다.
- [ ] 예상하지 못한 파일 변경의 이유와 영향을 기록했다.
