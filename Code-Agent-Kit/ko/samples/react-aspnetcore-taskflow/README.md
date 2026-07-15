# TaskFlow — React + ASP.NET Core 샘플

TaskFlow는 의도적으로 작게 만든 기능 워크플로우 애플리케이션입니다. 다음 내용을 시연합니다.

- Document First 설계
- Git 기준점과 Diff 검토 의무화
- 공식 출처 MCP 라우팅
- 결정론적 백엔드 및 프런트엔드 Validation
- Validation 기반 `current.md` 핸드오프
- `history.md`에 기록하는 기능 변화
- 스택 독립 핵심 워크플로우와 스택 전용 규칙의 분리

## 기능

- 작업 목록 조회
- 작업 생성
- 통제된 상태 변경
- 승인 요청
- 승인 및 반려
- 반응형 UI
- 백엔드 API Test
- 프런트엔드 Component Test
- Playwright E2E 및 좁은 화면 검사

## 요구 환경

- .NET SDK 10.x
- Node.js 22.12 이상
- npm
- E2E 실행 시 Playwright Chromium

## 로컬 실행

백엔드:

```bash
cd backend/TaskFlow.Api
dotnet run
```

프런트엔드:

```bash
cd frontend
npm install
npm run dev
```

브라우저:

```text
http://127.0.0.1:5173
```

## Validation 실행

PowerShell:

```powershell
./scripts/validate.ps1
```

Bash:

```bash
./scripts/validate.sh
```

실행 증거는 다음 위치에 저장됩니다.

```text
docs/evidence/generated/
```

## Docker

```bash
docker compose up --build
```

- UI: `http://localhost:5173`
- API Health: `http://localhost:8080/health`

## 워크플로우 문서

영문 실행 기준:

- [AGENTS.md](AGENTS.md)
- [current.md](docs/current.md)
- [history.md](docs/history.md)
- [Project Map](docs/project-map.md)
- [초기 설계 영문](docs/designs/001-initial-taskflow.md)
- [Priority 실험 설계 영문](docs/designs/002-priority-field.example.md)

한국어 설명:

- [AGENTS 한국어](AGENTS.md)
- [현재 상태 한국어](docs/current.md)
- [이력 한국어](docs/history.md)
- [Project Map 한국어](docs/project-map.md)
- [초기 설계 한국어](docs/designs/001-initial-taskflow.md)
- [Priority 실험 설계 한국어](docs/designs/002-priority-field.example.md)

## 권장 실험

새 에이전트 채팅에서 다음과 같이 요청합니다.

> `Low`, `Normal`, `High` 값을 가진 `priority`를 추가하세요. 작업 생성 시 선택할 수 있고 각 카드에 표시되어야 합니다. `AGENTS.md`를 따르고 결정론적 Validation을 통과하기 전에는 완료하지 마세요.

준비된 설계 예제와 실제 결과를 비교해 볼 수 있습니다.
