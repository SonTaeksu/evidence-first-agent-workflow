# 변경 이력

[English](CHANGELOG.md) | **한국어**


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

## v0.1.5-alpha — State Model 및 Verified Stack 입력 복원

- Design Concepts Ledger와 Architecture Decision을 추가했습니다.
- Feature Current 우선 Routing과 Append-only History를 복원했습니다.
- Stack Owner 입력, Readiness Manifest, 결정론적 Readiness Validation을 추가했습니다.
- Shared Reverse Dependency, Git State 연결, Architecture State를 추가했습니다.
- Visual Block Empty Detection과 Generic Output/Build Validator Contract를 추가했습니다.
- Agent Adapter를 Pointer로 축소했습니다.

## v0.1.4-alpha — Code Agent Kit 운영 기능 통합

- 보류 상태였던 Rendered SPA 입력 분기를 구현했습니다.
- Screen 완전성 검사, Prompt Routing, Worklog, 사람용 Guide 경계를 추가했습니다.
- Git Scope Validation을 보강했습니다.
- 기존 Image Manifest를 Primary로 유지하고 Kit Palette Tool을 Backup으로 추가했습니다.
- Generic Skill Routing과 Demo 격리를 추가했습니다.

## v0.1.3-alpha — 멀티모달 변환 이전 Reference Image Evidence

- 정확한 원본 파일 및 Decoded Pixel Hash를 추가했습니다.
- ICC, EXIF, Palette, Pixel Grid, 이름 있는 영역 증거를 추가했습니다.
- 정규화 무손실 PNG를 추가했습니다.
- Runtime Computed Color와 ΔE00 비교를 추가했습니다.
- 자체 검사와 실행 Wrapper를 추가했습니다.
- 준비된 대표 Package가 제공될 때까지 SPA HTML 입력은 예약 상태로 두었습니다.

## v0.1.2-alpha — 다중 에이전트 설정과 UI 색상 게이트

- Codex, Roo Code, Zoo Code, Cline, Claude Code 설정을 추가했습니다.
- 공통 MCP 설정과 설정 검사 도구를 추가했습니다.
- 정적 및 Runtime UI 색상 게이트를 추가했습니다.
- 한 번에 실행하는 커밋 전 Validation Script와 실제 상태를 구분한 보고서를 추가했습니다.
- 작은 모델용 Computed Color 증거를 추가했습니다.
- 새 게이트가 발견한 Contrast 실패 두 곳을 수정했습니다.
- 실행할 수 없었던 Backend/Browser 결과는 PASS로 주장하지 않고 제한 사항으로 기록했습니다.

## v0.1.1-alpha — 전체 한국어 문서 지원

- 사람이 읽는 모든 공개 Markdown 문서에 한국어 대응 문서를 추가했습니다.
- 영문과 한국어 문서 사이의 상호 이동 링크를 추가했습니다.
- 전체 한국어 문서 색인을 추가했습니다.
- 원본을 유지해야 하는 Validation 증거에는 한국어 요약을 추가했습니다.
- 공식 영문 라이선스 원문을 유지하면서 한국어 설명을 추가했습니다.
- GitHub Issue Form을 영문·한국어 병기로 변경했습니다.
- 번역 운영 정책과 언어 문서 지원 범위 자동 검사를 추가했습니다.
- GitHub 기본 진입 언어는 영어를 유지합니다.

## v0.1.0-alpha

- 최초 핵심 워크플로우를 공개했습니다.
- React + ASP.NET Core TaskFlow 샘플을 추가했습니다.
- Microsoft Learn MCP와 Context7 라우팅을 추가했습니다.
- 결정론적 Validation 보조 도구를 추가했습니다.
- 영문 기본·한국어 대응 AI Workflow Design Review를 추가했습니다.
