# Overview — 전체 레퍼런스

[English](OVERVIEW.md) | **한국어**

> 처음이세요? [README.ko.md](README.ko.md)를 먼저 읽고 [QUICKSTART.ko.md](QUICKSTART.ko.md)로 가세요. 이 문서는 완전한 레퍼런스이며, 이 프로젝트가 무엇을 위한 것인지 이미 안다고 전제합니다.

> 소형 모델, 폐쇄망, 장기 Project, 추론이 아니라 검증된 지식이 필요한 Stack을 위한 Tool 비종속 Context Management 및 Development Governance Workflow입니다.

## 상태

**Alpha 단계**입니다. 공개 평가를 권장하지만 완전 자율 개발이나 모델과 무관한 보편 품질을 주장하지 않습니다.

## 두 축의 모델

```text
Framework-agnostic governance core
+
Verified stack or organization knowledge pack
```

Core는 기억을 외부화하고, Context를 Routing하며, 5단계 Gate를 강제하고, 판단을 결정론적 Tool에 위임합니다. Stack Pack은 Core가 지어낼 수 없는 Fact, Skeleton, Capability, Contract, Pitfall을 공급합니다.

[설계 개념 원장](DESIGN-CONCEPTS.ko.md)을 참고하세요.

## Portable Code Agent Kit

실행 Package는 Repository History 및 Evaluation 자료와 물리적으로 분리돼 있습니다.

```text
Code-Agent-Kit/
├─ en/   # independently copyable English mirror
└─ ko/   # independently copyable Korean mirror
```

두 Mirror는 상대 경로가 동일하며 각각 독립적으로 복사할 수 있습니다. `tools/check-mirror-parity`가 그것을 강제합니다. 고아 경로, Mirror 사이에서 어긋난 Shared Script, 실측과 모순되는 수치 주장은 exit 2로 실패합니다.

각 Mirror에는 필요한 `docs/`, `demos/`, Prompt, Template, Stack, Tool, Script, Reference Asset, Hidden Agent Adapter, License, 선택형 Sample이 포함됩니다. 과거 Design Review와 Evaluation 보고서는 Portable Package 밖에 유지합니다.

[Portable Code Agent Kit 구조](Code-Agent-Kit/ko/docs/getting-started/portable-code-agent-kit.md)를 참고하세요.

## 지속 State와 Session Handoff

```text
Project Map
→ feature current
→ related files and shared dependencies
→ active worklog only when unfinished
→ source
```

- **Feature current**는 이후 모든 수정 작업의 지속적이고 검증된 시작 State입니다.
- **Feature history**는 Append-only이며 Commit과 PR을 Index합니다.
- **Worklog**는 Gate 진행, Evidence, Resume Point를 담는 임시 Checkpoint입니다.
- Worklog는 절대 Current State를 대체하지 않습니다.

[State 및 Memory Model](Code-Agent-Kit/ko/docs/core/state-and-memory-model.md)을 참고하세요.

## Stack마다 사용자 입력이 필요합니다

Generic Core는 File과 Package를 Detection할 수 있지만 다음을 안전하게 지어낼 수 없습니다.

- 지원 SDK 및 Runtime Policy
- 정본 Framework Reference
- Golden Skeleton File
- Feature Boundary
- 사내 Convention
- Communication 및 Data Contract
- Capability 분기 Rule
- Validation 명령과 실패 신호
- 기밀 등급 Policy

필수 입력과 Blocking Capability가 해결되기 전에는 Stack이 Ready가 아닙니다.

```bash
python Code-Agent-Kit/en/tools/check-stack-readiness/check_stack_readiness.py \
  --stack Code-Agent-Kit/en/stacks/react-aspnetcore
```

[Stack 입력 요구사항](Code-Agent-Kit/ko/docs/getting-started/stack-input-requirements.md)을 참고하세요.

## 필수 실행 모델

```text
1 Analysis
→ 2 Task
→ 3 Todo and Micro-Verify
→ 4 Checklist
→ 5 Verification
```

다섯 Header는 필수 출력 Scaffold입니다. Todo 내부의 국소 실패는 해당 Todo를 반복합니다. 잘못된 가정, Scope 문제, Source 충돌, Unknown Capability는 Analysis로 돌아갑니다.

[필수 Gate](Code-Agent-Kit/ko/prompts/GATE.md)를 참고하세요.

## 결정론적 Evidence

Workflow에 포함된 것:

- Stack Readiness Validation
- State Model Validation
- Git Scope 및 Document Sync 검사
- Generic Build Log Scanning
- Rendered SPA 추출
- Grid, Form, Button, KPI, Card, Chart, Matrix, Panel Evidence
- 빈 Visual Block 거부
- Reference Image Hash, ICC, EXIF, Palette, Region, ΔE00 비교
- Static 및 Runtime Color Contrast
- Playwright E2E 및 선택형 Visual Baseline
- Rendered Document를 만들지 않는 UI Framework를 위한 Windows Forms Designer Control Tree 추출과 Screen Specification 대조

모델이 "PASS"라고 말하는 것은 Evidence가 아닙니다. Program Exit Code와 생성된 Artifact가 Evidence입니다.

## 시작 순서

1. [시작하기](Code-Agent-Kit/ko/docs/getting-started/README.md)
2. [설계 개념 원장](DESIGN-CONCEPTS.ko.md)
3. [State 및 Memory Model](Code-Agent-Kit/ko/docs/core/state-and-memory-model.md)
4. [Stack 입력 요구사항](Code-Agent-Kit/ko/docs/getting-started/stack-input-requirements.md)
5. [작업 Prompt Router](Code-Agent-Kit/ko/prompts/README.md)
6. [React + ASP.NET Core Stack Profile](Code-Agent-Kit/ko/stacks/react-aspnetcore/README.md)
7. [C# Windows Forms Stack Profile](Code-Agent-Kit/ko/stacks/csharp-winforms/README.md)
8. [TaskFlow Sample](Code-Agent-Kit/ko/samples/react-aspnetcore-taskflow/README.md)
9. [Gate 설계 원칙](Code-Agent-Kit/ko/docs/core/gate-design-principles.md)
10. [사람용 개발자 Guide](Code-Agent-Kit/ko/docs/human/developer-guide.md)

## 포함 구조

- 이중 언어 Governance 문서와 Template
- Architecture Decision 및 Rejected Alternative
- Feature current/history/worklog Template
- System 및 Database Architecture State Template
- 완전한 Verified Stack Template Contract
- Ready 상태의 React + ASP.NET Core Sample Stack
- .NET Framework 4.7.2 이상을 위한 Ready 상태의 C# Windows Forms Stack — Reference Skeleton과 Designer Tree Evidence 포함
- Owner 입력이 올 때까지 Blocked 상태로 기다리는 Stack Profile 10개 — WPF, WCF, ASMX, Vue.js, Next.js, Node.js, Go, Go + HTMX, Rust, Elixir. 각각 그 기술의 제약, 조용히 실패하는 함정, Capability 탐지 규칙, 문서 라우팅을 이미 담고 있습니다.
- Codex, Roo Code, Zoo Code, Cline, Claude Code Adapter
- Project 범위 MCP 예제, 그리고 실제로 연결해 호출까지 확인한 공개 문서 서버 14개를 가리키는 Stack별 Profile (`docs/core/mcp-source-verification.md`)
- 결정론적 Tool — 각각 판정이 동일하다고 증명된 Python + PowerShell 쌍으로 출하되며, Tool마다 Self-test 포함
- React + ASP.NET Core TaskFlow Sample

## Validation Layer

```text
Artifact / Compile
≠ Rendered Output
≠ Runtime Behavior
≠ Accessibility / Color
```

Build가 통과해도 화면이 비어 있거나 Runtime 동작이 실패할 수 있습니다. 적용되는 모든 Layer를 각각 따로 기록해야 합니다. 실행할 수 없는 Layer는 사유와 함께 `PENDING`으로 기록하며, 절대 `PASS`로 기록하지 않습니다.

## Source Asset

- Image → 멀티모달 변형 전에 Reference Image Manifest.
- SPA → Rendered DOM과 Screen Specification.
- Static HTML → 원본 보존과 제한된 구간 검사.
- Rendered Document가 없는 Desktop UI → Designer Control Tree와 Screen Specification.
- MCP 또는 Search 결과 → 보관된 Transcript가 아니라 압축된 Fact와 Provenance.

## Stack Profile

완전한 Stack Pack에는 다음이 포함됩니다.

```text
STACK.md
STACK-INPUTS.md
STACK-READINESS.json
AGENTS.stack.md
SKILL.md
capability-detection.md
feature-model.md
artifact-contract.md
communication-contract.md
evidence-provenance.md
mcp-profile.json.example
mcp/source-routing.md
references/
skeletons/
validation/
```

`mcp/source-routing.md`에는 그 Stack에 권위 있는 문서 서버, 권위가 **없는** 서버, 그리고
시험했을 때 각 서버가 실제로 노출한 Tool 이름이 적혀 있습니다. 예시 Profile은 기본
활성이 아닙니다 — 그것을 복사하는 것이 이 질의들이 기계를 떠나는 것을 운영자가 수락하는
행위입니다.

사내 Library 이름과 조직 전용 Rule은 Generic Core가 아니라 해당 비공개 Stack Pack에 둡니다.

## 지원 코딩 Agent

- Codex
- Roo Code
- Zoo Code
- Cline
- Claude Code

Tool Adapter는 같은 `AGENTS.md`를 가리키며 Workflow를 다시 정의하지 않습니다.

## 강제화

정직이 우선입니다. Agent는 자기 실수를 스스로 보고하고, 불확실하면 추측 대신 멈추며, "완료"를 "검증 통과"로만 취급합니다(`AGENTS.md` 참고). 모델은 자기 자신을 신뢰성 있게 채점할 수 없으므로, Rule은 요청이 아니라 기계로 강제됩니다.

- **Commit 시점 Gate**와 **CI Job**(`tools/enforce-agent-gates`)이 필수 Worklog, 5개 Gate 섹션, State 동기화 없이 Source를 바꾼 Commit을 차단합니다.
- **Sanitization Gate**(`tools/check-sanitization`)가 공개 릴리스 전에 독점 문자열이나 조직 식별 문자열을 차단합니다.
- **Mirror Parity 검사**(`tools/check-mirror-parity`)가 고아 경로, 언어 Mirror 사이에서 어긋난 Shared Script, 실측과 모순되는 수치 주장을 차단합니다.
- **Kit Self-check**(`tools/check-kit-selfcheck`)가 킷이 복사하라고 지시한 Template을 킷 자신의 Validation에 돌려, 유일한 출구가 `--no-verify`인 상태로 Scaffold가 배포되지 못하게 합니다.
- **양벌 Parity 검사**(`tools/check-script-parity`)가 모든 Tool의 Python·PowerShell 구현을 사례별로 비교합니다(작성 시점 154건, 현재 수치는 `--status`가 출력). 종료 코드 **와** finding 식별자가 모두 일치해야 하고, 각 사례는 규약이 요구하는 종료 코드까지 못박으므로, 두 구현이 틀린 답에 합의해서 통과하는 일이 불가능합니다.
- **측정된 Stack Readiness**(`tools/check-stack-readiness`)가 인용된 모든 증거 경로를 트리에서 해석합니다. 존재하지 않는 파일을 가리키는 Manifest는 `ready`가 아니라 `blocked`로 도출됩니다.

Commit Gate는 `scripts/install-hooks.sh`(Windows는 `install-hooks.ps1`)로 켜거나, 한 줄로 켭니다: `git config core.hooksPath tools/enforce-agent-gates`.

훅은 **Python 3.11 이상 또는 PowerShell**이 필요합니다 — 있는 쪽을 골라 쓰고, 둘 다 없으면 Commit을 거부합니다. Python 하한이 3.11인 이유는 한 검사가 Codex의 TOML 설정을 읽고 `tomllib`이 그 버전에서 표준 라이브러리에 들어왔기 때문입니다. 더 낮은 인터프리터에서는 그 검사가 크래시하지 않고 요구사항을 알리며 exit 1 합니다.

자세한 내용은 [강제화 표](Code-Agent-Kit/ko/docs/core/enforcement-matrix.md)에 있습니다. 새 검사가 그 표에 자리를 얻기 전에 만족해야 할 조건은 [Gate 설계 원칙](Code-Agent-Kit/ko/docs/core/gate-design-principles.md)에 있습니다. 선택형 Agent Stance는 `docs/persona.md`에 있습니다.

## 정직한 경계

- 인지적 Rule — "먼저 읽었는지", "추측을 피했는지", "근거 우선순위를 지켰는지" — 은 Commit Artifact만으로 검증할 수 없습니다. 강제되는 것은 각 Rule이 남겨야 할 Artifact이며, 그래서 건너뛰면 탐지 가능한 흔적이 남습니다.
- 쓰기 시점 차단(수정이 일어나는 순간 거부)은 여기에 존재하지 않는 Platform Write-hook API를 필요로 합니다. Commit 시점과 CI 차단이 그 대체입니다.
- 오탐은 놓친 결함보다 더 해로운 것으로 취급합니다. 거짓 경보 한 번이 운영자에게 Gate를 영구히 우회하는 법을 가르치기 때문입니다.

## 라이선스

프로젝트 전체가 **MIT License**로 배포됩니다([LICENSE](LICENSE) 참고). 상업적 사용과 비공개 소스 사용이 자유로우며, 저작권 고지만 유지하면 됩니다. 피드백은 환영하지만 의무는 아닙니다.
