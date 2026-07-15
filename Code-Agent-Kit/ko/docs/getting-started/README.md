# 시작하기

## 1. 설계와 State Model 읽기

다음부터 시작합니다.

- `DESIGN-CONCEPTS.md`
- `AGENTS.md`
- `docs/core/state-and-memory-model.md`
- `docs/getting-started/stack-input-requirements.md`

## 2. Git 및 Project Route 확인

```bash
git status
```

Sample에서는 다음을 읽습니다.

```text
samples/react-aspnetcore-taskflow/docs/project-map.md
samples/react-aspnetcore-taskflow/docs/features/task-flow.current.md
```

Project-level `docs/current.md`는 Summary입니다. Feature 수정은 Feature Current에서 시작합니다.

## 3. Stack Readiness 확인

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

다른 Project에서는 Stack Template을 복사하고 구현 전에 Owner 입력을 제공해야 합니다.

## 4. MCP 확인

Codex:

```bash
codex mcp list
```

예상:

- `microsoft_learn`
- `context7`

MCP는 Knowledge Source입니다. 조회 Fact는 압축하여 Evidence Provenance에 기록합니다.

## 5. 작업 시작

신규 Feature 또는 수정:

1. `prompts/0-sync-and-orient.md` 실행
2. `prompts/`의 상황별 Prompt 사용
3. `templates/core/worklog.md`에서 Worklog 생성
4. 필수 5단계 Gate Header 전부 사용
5. Code 전에 Blocking Capability 해결

미완료 작업:

```text
Worklog Header
→ Git
→ Project Map
→ Feature Current
→ Current Related Files
→ 전체 Worklog
→ 재개
```

## 6. TaskFlow Sample 실행

Backend:

```bash
cd samples/react-aspnetcore-taskflow/backend/TaskFlow.Api
dotnet run
```

Frontend:

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm install
npm run dev
```

`http://localhost:5173`을 엽니다.

## 7. 권장 첫 실험

Task Priority Field를 추가합니다.

Agent는:

1. Task Flow Current 및 Shared Dependency 읽기
2. React/.NET Stack Readiness 확인
3. 새 Worklog 생성
4. Version 민감 Fact 검증
5. Frontend/Backend Contract 함께 갱신
6. Artifact, Rendered Output, Runtime, Color Gate 실행
7. 검증 Commit을 Feature Current에 기록
8. Feature History Append
9. Project Map 및 Reverse Index 갱신
10. 최종 Diff 검토

## 8. Validation 실행

전체 Repository Gate:

```powershell
./scripts/pre-commit-validate.ps1
```

Sample Gate:

```powershell
./samples/react-aspnetcore-taskflow/scripts/validate.ps1
```

Bash Script도 제공합니다.
