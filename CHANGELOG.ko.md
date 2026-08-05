# 변경 이력

[English](CHANGELOG.md) | **한국어**


## v0.1.9-alpha — 데스크톱 Stack, 자기검사하는 킷, 입문자용 진입점 (2026-08-04)

### 추가 — C# Windows Forms Stack (ready)
- .NET Framework 4.7.2 이상용 `stacks/csharp-winforms/`: 필수 문서 14개 전부, Reference Skeleton(`skeletons/MinimalApp/` — SDK-style `net472` Project, `App.config`의 per-monitor v2 DPI, Windows 10 Manifest 선언, Designer/Behaviour 분리, 단일 Service 경계), MSBuild·VSTest Validation Profile. `check_stack_readiness`가 양쪽 Mirror에서 `READY`·exit 0.
- `references/ui-evidence-contract.md`와 `tools/extract_designer_tree.py`·`check_designer_spec.py`: Windows Forms에는 Rendered 문서가 없으므로, Rendered Output Layer가 Designer Control Tree를 읽어 Gate §1에서 작성한 화면 명세와 대조합니다. 판정 전 주석을 길이 보존 방식으로 지우고 문자열 Literal은 보존합니다. Self-test 14케이스이고 절반은 무언가가 **남아야 한다**를 확인합니다.
- `references/verified-facts.md`와 `evidence-provenance.md`의 Version 민감 Fact는 전부 Microsoft Learn 출처와 확인일을 답니다.

### 추가 — 킷이 자기 자신을 검사한다
- `tools/check-kit-selfcheck/`: 문서가 지시한 복사 원본을 지시된 대로 복사해 킷 자신의 Readiness Validator에 돌립니다. 빈 Seed는 `blocked`가 나오는 것이 **정상**이므로 미확인 Input은 무시하고 구조적 실패만 셉니다. `ready`를 선언한 모든 Stack이 실제로 ready인지도 확인합니다.
- `tools/check-mirror-parity/`: Mirror 간 상대 경로 집합 일치, 산문이 아닌 File의 Byte 동일, 문서가 적은 수치와 실측 대조. 세는 규칙이 기록되지 않은 수치는 FAIL이 아니라 WARN입니다 — 문서에 적히지 않은 규칙 아래에서는 맞을 수 있기 때문입니다. Build 잔재는 측정에서 제외하고 경고합니다.
- 두 Tool 모두 `docs/core/enforcement-matrix.md`·`KIT-MANIFEST.json`·`check_kit_installation.py`에 등록했습니다.

### 추가 — Gate 설계 원칙
- `docs/core/gate-design-principles.md` (en/ko): 새 결정적 검사가 무언가를 차단할 수 있게 되기 전에 만족해야 할 조건. 비공개 킷의 강제 설계 원칙과 12세션 관찰 기록을 스택 중립으로 일반화했습니다.
- 비공개 킷이 모든 Rule을 도출한 **관찰된 3가지 사실**을 근거로 둡니다 — 문서에 적어도 안 읽는다(모델 급과 무관), Context 압축이 Rule을 지우므로 상주 File과 Hook으로 무게를 옮겨야 한다, "완료" 자기보고는 믿을 수 없고 위험한 형태는 실패의 합리화다.
- 원칙 9개: 문서는 강제하지 못하고 기계 판정으로 옮긴 것만 지켜졌다 / 확실한 것만 BLOCK / 애매하면 WARN — **단 침묵 실패는 BLOCK**이어야 가장 위험한 것이 가장 약하게 막히지 않는다 / 탈출구는 사람이 적은 명시적 Marker이고 암묵 면제가 아니다 / Rule ID는 모델이 아니라 Tool의 소유다 / 판정 근거는 Project 문서에 둔다 / 판단을 없애면 실행률이 오르므로 Runner는 흔한 경우에 인자를 요구하지 않는다 / Compile·Test 통과는 동작이 아니다 / 내 산출물도 같은 실패를 하므로 실측으로 검증하고 문서는 diff·카운트로 생성한다.
- 마지막 절은 정직한 한계를 감추지 말고 공개할 것을 요구합니다. 어떤 원칙도 없애지 못하는 구조적 벽 셋 포함 — 검사는 무언가가 발동시켜야만 돌고, CI가 없으면 비협조적 모델을 이길 수 없으며, Context 압축은 Tool로 못 막습니다.

### 수정
- `docs/core/honesty-and-correction.md` (en)이 "Correct code with a wrong d"에서 문장 중간에 잘려 있었습니다. 온전한 한국어 Mirror를 기준으로 복구했습니다.
- `templates/stack-profile/`에 자기 `STACK-READINESS.json`이 필수로 요구하는 `validation/validation-profile.md`가 없었습니다. `docs/getting-started/using-another-stack.md`가 지시한 대로 복사하면 Readiness Validation이 실패하는 상태였습니다. 함께 `SKILL.md`가 참조하지만 존재하지 않던 `mcp/source-routing.md`도 추가했습니다.
- `docs/core/enforcement-matrix.md`가 `check-portable-kit`이라는 Tool을 인용했으나 디스크의 Tool 이름은 `check-kit-installation`입니다.
- `KIT-MANIFEST.json`의 `mirrored_file_count: 270`이 어떤 계산 규칙으로도 실측과 맞지 않았습니다. `mirrored_file_count_rule`을 추가하고 값을 실측으로 맞췄습니다. 이제 기계가 대조합니다.

### 변경 — 문서 진입점
- `README.md`·`README.ko.md`를 "프로그래밍은 하지만 AI 코딩 에이전트는 처음인 사람" 기준으로 다시 썼습니다: 문제, 3단계 시작, 무엇이 달라지나, 무엇을 얻나, **무엇을 치르게 되나**(9개 항목 — Gate가 우회 가능하다는 점과 거짓 경보가 진짜 위험이라는 점 포함), 내 Stack 추가법, 어떤 장비·모델에서 돌아가나.
- `OVERVIEW.md`·`OVERVIEW.ko.md`(신규)가 이전 README의 전체 참조 내용을 담고, "정직한 경계" 절을 추가했습니다.
- `QUICKSTART`·`CONTRIBUTING`·`ADOPTION`을 양쪽 언어로 갱신했습니다. `CONTRIBUTING`은 새 Stack Profile에 File 4개가 필요하다고 적혀 있었는데 실제로는 14개이고, 옛 문구대로 따라가면 Validation에 실패하는 Stack이 나왔습니다.
- `ADOPTION`이 이제 모델, Agent Tool, GPU·VRAM, RAM, 양자화, 컨텍스트 창, 관측 속도, 어디까지 갔는지를 묻습니다. "작은 모델로도 된다"는 주장에는 관리자 장비 말고 다른 장비의 근거가 필요하기 때문입니다.

### 보고 — 저사양 실행
- Pi Agent + Qwen3.6 35B A3B Compact, 노트북 6 GB VRAM·32 GB RAM에서 사람 개입을 포함해 기능 하나를 끝까지 완성했습니다. 처음 약 45 tokens/second에서 컨텍스트가 길어지며 대략 21 tokens/second까지 떨어졌습니다. 벤치마크가 아닌 가벼운 시험이며, 이 공개 릴리스가 아니라 원래의 사내 버전에서 돌린 것입니다. 개입은 비공개 Stack의 서버 호출 관례와 클라이언트 쪽 표시 문제였고 워크플로우 자체 때문이 아니었습니다.

### 검증
- 게이트 19개 실행, 실패 0: Stack Readiness(2 Stack × 2 Mirror), Kit Self-check(2), Kit Installation(2), Mirror Parity, Self-test 5종, 양쪽 Mirror의 Designer Tool.
- `check_sanitization` 689개 File: CLEAN, 경고 0.
- Python 64개 File 컴파일 통과.
- Mirror 실측 각 327개, 경로 일치, Shared Script 68개 전부 Byte 동일.


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
