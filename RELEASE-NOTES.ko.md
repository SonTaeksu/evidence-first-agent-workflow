# Alpha Release Note

[English](RELEASE-NOTES.md) | **한국어**

## v0.1.9-alpha — 데스크톱 Stack, 자기검사하는 킷, 입문자용 진입점 (2026-08-04)

### 핵심

세 가지이고, 그중 하나는 불편한 내용입니다.

**두 번째 ready Stack.** .NET Framework 4.7.2 이상의 C# Windows Forms. Reference Skeleton과 Validation Profile을 갖췄습니다. 교육용 사례이기도 합니다 — Windows Forms에는 Rendered 문서가 없어서 흔히 쓰는 "화면이 정말 그려졌나" 검사가 볼 대상 자체가 없습니다. 그 Layer를 조용히 빼는 대신, 이 팩은 Form의 Designer File을 읽어 선언된 Control을 코드가 존재하기 전에 작성된 명세와 대조합니다.

**킷이 자기 자신을 검사합니다.** `check-kit-selfcheck`는 킷이 복사하라고 지시한 Template을 복사해 킷 자신의 Validator에 돌립니다. `check-mirror-parity`는 두 언어 Mirror를 대조하고, 문서가 적은 수치를 실측과 대조합니다.

**불편한 부분: 그 자기검사가 첫 실행에서 실제 결함을 잡았습니다.** `using-another-stack.md`가 복사하라고 지시하는 `templates/stack-profile/` 폴더에, 자기 Manifest가 필수로 적어둔 File이 없었습니다. 문서대로 따라간 사람은 자기 잘못이 아닌 Readiness 실패를 겪었습니다. 그 결함이 그동안 배포되고 있었습니다. 수정했고, 그것을 잡았을 검사가 이제 돕니다.

### ⚠️ 행동 변화

새로 차단되는 것은 없지만, 두 가지 주장이 이제 기계로 검사됩니다.

| 변경 | 방향 | 새로 실패하는 것 |
|---|---|---|
| `mirrored_file_count`를 실측과 대조 | 엄격해짐 | `mirrored_file_count_rule`이 있는데 수치가 틀린 Manifest |
| `ready`를 선언한 Stack은 실제로 ready여야 함 | 엄격해짐 | 도달할 수 없는 상태로 배포된 Stack Pack |
| Seed Template에 필수 문서 누락이 없어야 함 | 엄격해짐 | 킷 자신의 검사를 통과하지 못하는 Scaffold |

Fork를 유지하신다면 갱신 후가 아니라 **갱신 전에** `check-mirror-parity`와 `check-kit-selfcheck`를 돌려 보세요.

### 추가
- `stacks/csharp-winforms/` — ready, 양쪽 Mirror, `check_stack_readiness` exit 0.
- `tools/check-kit-selfcheck/`, `tools/check-mirror-parity/` — Self-test 포함.
- `docs/core/gate-design-principles.md` — 새 검사가 무언가를 차단할 수 있게 되기 전에 만족해야 할 조건.
- `OVERVIEW.md`·`OVERVIEW.ko.md` — README에서 분리한 전체 참조.

### 수정
- `docs/core/honesty-and-correction.md` (en)이 문장 중간에 잘려 있었습니다.
- `templates/stack-profile/`에 File 2개가 없었고, 그중 하나는 자기 Manifest가 필수로 요구하는 것이었습니다.
- `enforcement-matrix.md`가 존재하지 않는 Tool을 인용했습니다.
- `KIT-MANIFEST.json`이 어떤 계산 규칙과도 맞지 않는 File 개수를 싣고 있었습니다.

### 변경
- `README`를 AI 코딩 에이전트가 처음인 독자 기준으로 다시 썼고, 비용·위험 9개 항목을 명시했습니다.
- `CONTRIBUTING` 정정: 새 Stack Profile은 File 4개가 아니라 14개 문서가 필요합니다.
- `ADOPTION`이 이제 모델, GPU, VRAM, RAM, 컨텍스트 창, 관측 속도를 묻습니다.

### 보고 — VRAM 6 GB에서 돌리기

Pi Agent + Qwen3.6 35B A3B Compact, 노트북, 6 GB VRAM, 32 GB RAM: 사람 개입을 포함해 기능 하나를 끝까지 완성했고, 속도는 약 45 tokens/second에서 컨텍스트가 길어지며 대략 21까지 떨어졌습니다.

주의사항이 중요합니다. 벤치마크가 아니라 가벼운 시험이고, 이 공개 릴리스가 아니라 원래의 사내 버전에서 돌렸으며, 비공개 Stack의 서버 호출 관례와 클라이언트 쪽 표시 문제에 사람이 개입해야 했고, 긴 컨텍스트에서 21 tokens/second는 체감될 만큼 느립니다.

### 검증

게이트 19개, 실패 0. `check_sanitization` 689개 File CLEAN. Python 64개 File 컴파일 통과. 양쪽 Mirror 실측 각 327개, 경로 일치, Shared Script 68개 Byte 동일.

주장하지 않는 것: 브라우저·.NET SDK·Docker가 필요한 애플리케이션 수준 게이트는 이전과 마찬가지로 생성 환경에서 `PENDING`입니다. `PRE-COMMIT-VALIDATION.ko.md` 참고.

## v0.1.8-alpha — 강제된 정직·프로세스 안전·스택 온램프 (2026-07-15)

### 추가 — 정직·증거 규칙 (AGENTS.md, 항상 로드)
- "정직이 완료보다 우선"을 `AGENTS.md`와 `docs/core/honesty-and-correction.md` 최상단으로: 자기 실수 보고, 불확실하면 추측 대신 멈춤.
- 완료 어휘 규제: "완료/끝/done"은 GATE §5 통과 때만; 중간 단계는 "N단계까지 진행함".
- 주장이 아니라 증거: 검증 단계는 실제 명령·Exit Code를 인용하고 각 GATE 단계를 넘어가기 전에 보고; 명령·Exit 없는 `PASS`는 `PENDING`으로 간주.
- 완료는 커밋에 앵커링: 검증 커밋과 해시 기록 전엔 `완료` 아님; 그 전엔 `verified, pending commit`.
- 스택/Capability 결정을 Analysis에 명시적으로 기록.

### 추가 — 기계 강제화
- 커밋 게이트 + CI 잡(`tools/enforce-agent-gates/`): 워크로그·5단계 GATE·상태 동기화 없이 소스를 스테이징한 커밋 차단; 명령·Exit 없는 워크로그 `PASS` 거부.
- 공개 릴리스 세척 게이트(`tools/check-sanitization/`): 조직·독점 명칭 차단(exit 2).

### 추가 — 명령·프로세스 안전
- `docs/core/command-and-process-safety.md`: 이미지 이름 일괄 종료 금지(`Get-Process node | Stop-Process`, `killall node`, `pkill -f npx`) — 에이전트 자신의 MCP 서버까지 죽임.
- 관리 실행 러너 `tools/run-managed-service/run_service.py`: dev 서버를 PID+포트로 시작/중지하고 포트 해제 확인. AGENTS·스택 템플릿에 연결.

### 추가 — 색/테마 충실도 (react-aspnetcore)
- `stacks/react-aspnetcore/references/color-contract.md`: 참조 스크린샷이 진실 기준 → 팔레트 추출 → CSS 변수 토큰 바인딩 → ΔE 검증; `extract_palette`를 1급 도구로 승격.

### 추가 — 문서·온램프
- 선택적 에이전트 스탠스 `docs/persona.md`.
- `QUICKSTART.md` 개편(en/ko): 첫 프로젝트 초기화(신규 vs 기존, 부트스트랩 프롬프트), 실증된 Windows 첫 실행(git 한 줄, `.gitignore`, 최초 임포트 `--no-verify`), 검증 절차, 게이트 우회.
- 새 가이드 `docs/getting-started/using-another-stack.md`(en/ko): 스택 무관 코어 + 갈아끼우는 팩; 누가 무엇을; md vs MCP 출처 지정(실예제); AI로 채우기.
- `CLAUDE.md`가 `@AGENTS.md`를 임포트; Cline/Roo/Codex 어댑터를 비협상 규칙을 담도록 강화.

### 변경
- 저장소 루트를 소개/레퍼런스 문서 + 독립 복사 가능한 `Code-Agent-Kit/en`·`ko` 미러로 재편.
- 프로젝트 전체를 **MIT License**로 재라이선스(© Taeksu.Son and HUENSYSTEM Co., Ltd.).
- `ROADMAP`을 실제 진행에 맞게 갱신(완료 / 다음 / 후보 스택).

## v0.1.6-alpha — 언어 Mirror형 Portable Code Agent Kit

### 추가

- 독립 복사 가능한 `Code-Agent-Kit/en`, `Code-Agent-Kit/ko` 배포본
- 동일 상대 경로
- Agent 문서, 사람용 문서, Demo, Tool, Script, Stack, Reference Asset, Adapter, License, Sample의 자체 포함 구조
- Full/Core Installer Mode
- Portable Kit Mirror 및 Link Validator
- 자동 활성화 Workflow 대신 비활성 CI Template

### Packaging 결정

과거 Design Review/Evaluation 보고서와 생성 Evidence는 Repository에 유지하지만 Portable Kit 밖에 둡니다.

## v0.1.5-alpha — State, 설계 의도, Stack 입력 수정

### 추가

- 공개 설계 개념 원장
- Rejected Alternative를 보존하는 Architecture Decision
- Feature Current, Append-only History, 수정된 Worklog Template
- System 및 Database Architecture Current/History
- Project Map Feature Routing, Capability, Shared File Reverse Index
- Stack 입력 요구사항과 완전한 Verified Stack Template Contract
- Stack Readiness Validator 및 Self-test
- State Model Validator 및 Self-test
- Generic Build Log Scanner 및 Self-test
- Honesty/Correction, Validation Layer, MCP Compaction, Git Workflow, Output Adapter 문서
- KPI, Card, Chart, Matrix, Panel, Empty Visual Block 추출
- Visual Block 완전성 실패 Gate
- Ready 상태 React + ASP.NET Core Stack Manifest
- Blocked 상태의 Go + HTMX, Rust, Elixir 입력 Manifest

### 수정

- Worklog가 Feature Current를 대체하는 것처럼 보이던 문제 수정
- 재개 순서: Worklog Header → Git → Project Map → Feature Current → 전체 Worklog
- Root AGENTS를 얇게 만들고 Tool Adapter는 Pointer로 변경
- Stack 고유 사내 명칭을 Generic Core에서 제거
- Artifact, Rendered Output, Runtime Behavior, Color를 별도 Validation Layer로 구분
- Sample의 Project State와 Feature State 분리

### 생성 환경에서 완료한 Validation

- Agent 설정 및 얇은 Adapter 검사: PASS
- React + ASP.NET Core Stack Readiness: PASS
- Stack Readiness 정상/실패 Self-test: PASS
- Sample State Model Validation: PASS
- State Model 정상/실패 Self-test: PASS
- Build Log 정상/실패 Self-test: PASS
- SPA Grid 및 Visual Block 추출: PASS
- Missing Column 및 Empty Visual Block 실패 경로: PASS, Exit Code 2
- Reference Image Manifest 및 ΔE 비교: PASS
- Python Compile 및 JavaScript Syntax: PASS

### Local 또는 CI에서 필요한 Validation

- Frontend npm 새 Install, Type Check, Test, Build
- ASP.NET Core Restore, Build, Test
- Browser Runtime E2E 및 axe Color Gate
- Docker Build 및 Smoke Test

실행할 수 없었던 결과는 PASS로 보고하지 않습니다.
