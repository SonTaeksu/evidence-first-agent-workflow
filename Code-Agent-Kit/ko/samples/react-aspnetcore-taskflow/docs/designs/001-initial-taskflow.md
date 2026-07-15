# 설계: 최초 TaskFlow 샘플

## 요청

조직 또는 제품을 식별할 수 있는 세부 정보를 남기지 않으면서 워크플로우를 시연하는 공개 React + ASP.NET Core 샘플을 만듭니다.

## 현재 증거

- 핵심 워크플로우와 이중 언어 Design Review가 이미 존재합니다.
- Microsoft 기술에 사용할 공개 Microsoft Learn MCP가 있습니다.
- Context7이 React 및 관련 라이브러리 문서를 제공합니다.
- 주류 스택을 사용하면 기술의 비주류성이라는 교란 변수를 줄일 수 있습니다.

## 가정

- 첫 샘플은 외부 데이터베이스 없이 실행돼야 합니다.
- 영속성은 이후 실험입니다.
- 영어를 기본 공개 언어로 사용합니다.
- 대조군/적용군 비교 작업을 할 수 있을 정도로 샘플을 작게 유지합니다.

## 제외 범위

- Authentication 및 Authorization
- 영속 데이터베이스
- 다중 사용자 동시성
- Production Deployment 강화
- 완전한 Visual Design System

## 영향

- 첫 실행 가능한 Stack Sample 추가
- Stack 전용 Validation과 MCP Routing 추가
- 이후 Rust, Go + HTMX, Elixir 프로필을 위한 확장 규격 수립

## 예상 파일

- `AGENTS.md`
- `README.md`
- `docker-compose.yml`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/components/TaskForm.tsx`
- `frontend/src/components/TaskList.tsx`
- `frontend/e2e/taskflow.spec.ts`
- `backend/TaskFlow.Api/Program.cs`
- `backend/TaskFlow.Api/Domain/TaskItem.cs`
- `backend/TaskFlow.Api/Repositories/InMemoryTaskRepository.cs`
- `backend/TaskFlow.Api.Tests/TaskApiTests.cs`
- `docs/current.md`
- `docs/history.md`
- `docs/project-map.md`
- `scripts/validate.ps1`
- `scripts/validate.sh`

## Tasks

1. Backend API와 Domain Rule을 만듭니다.
2. React Frontend를 만듭니다.
3. Frontend, Backend, E2E Test를 추가합니다.
4. 결정론적 Validation Script를 추가합니다.
5. 샘플 Workflow State를 추가합니다.
6. Docker 실행 구성을 추가합니다.

## Todos

- [x] Status Workflow 정의
- [x] API 구현
- [x] Frontend 구현
- [x] Test Source 추가
- [x] State Document 추가
- [ ] Local 또는 CI Validation 실행
- [ ] Validation Evidence 기록

## Validation Checklist

- [ ] `dotnet build` PASS
- [ ] `dotnet test` PASS
- [x] `npm run lint` PASS
- [x] `npm run test` PASS
- [x] `npm run build` PASS
- [ ] `npm run e2e` PASS
- [ ] Docker Build PASS
- [ ] 최종 Diff에 작업과 무관한 변경 없음
