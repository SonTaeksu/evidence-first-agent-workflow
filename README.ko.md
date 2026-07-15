# Evidence-First Agent Workflow

[English](README.md) | **한국어**

> **처음이세요? [QUICKSTART.ko.md](QUICKSTART.ko.md)부터 보세요 — 한 페이지, 3단계로 결과.** 이 README는 전체 레퍼런스입니다.

> 소형 모델, 폐쇄망, 장기 Project, 추론이 아니라 검증 지식이 필요한 Stack을 위한 Tool 비종속 Context Management 및 Development Governance Workflow입니다.

## 상태

**Alpha 단계**입니다. 공개 평가를 권장하지만 완전 자율 개발이나 모델과 무관한 보편 품질을 주장하지 않습니다.

## 두 축의 모델

```text
Framework 비종속 Governance Core
+
검증된 Stack 또는 조직 Knowledge Pack
```

Core는 기억 외부화, Context Routing, 5단계 Gate, 결정론적 Tool 검증을 제공합니다. Stack Pack은 Core가 지어낼 수 없는 Fact, Skeleton, Capability, Contract, Pitfall을 제공합니다.

[설계 개념 원장](DESIGN-CONCEPTS.ko.md)을 참고하세요.

## Portable Code Agent Kit

실행 Package를 Repository History 및 Evaluation 자료와 물리적으로 분리했습니다.

```text
Code-Agent-Kit/
├─ en/   # 독립 복사 가능한 영문 Mirror
└─ ko/   # 독립 복사 가능한 한국어 Mirror
```

두 Mirror는 상대 경로가 완전히 같습니다. 한국어 File도 `AGENTS.md`, `worklog.md`처럼 일반 이름을 사용하며 `.ko.md` 접미사가 없습니다.

각 Mirror에는 필요한 `docs/`, `demos/`, Prompt, Template, Stack, Tool, Script, Reference Asset, Hidden Agent Adapter, License, 선택형 Sample이 포함됩니다. 과거 Design Review와 Evaluation 보고서는 Portable Package 밖에 유지합니다.

[Portable Code Agent Kit 구조](Code-Agent-Kit/ko/docs/getting-started/portable-code-agent-kit.md)를 참고하세요.

## 지속 State와 Session Handoff

```text
Project Map
→ Feature Current
→ Related Files 및 Shared Dependencies
→ 미완료 작업일 때만 Active Worklog
→ Source
```

- **Feature Current**는 이후 모든 수정 작업의 지속적이고 검증된 시작 State입니다.
- **Feature History**는 Append-only이며 Commit과 PR의 Index입니다.
- **Worklog**는 Gate 진행, Evidence, Resume Point를 담는 임시 Checkpoint입니다.
- Worklog는 Current State를 대체하지 않습니다.

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
- 보안 등급

필수 입력과 Blocking Capability가 해결되기 전에는 Stack이 Ready가 아닙니다.

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

[Stack 입력 요구사항](Code-Agent-Kit/ko/docs/getting-started/stack-input-requirements.md)을 참고하세요.

## 필수 실행 모델

```text
1 Analysis
→ 2 Task
→ 3 Todo와 Micro-Verify
→ 4 Checklist
→ 5 Verification
```

다섯 Header는 필수 출력 Skeleton입니다. Todo 내부 실패는 해당 Todo만 반복합니다. 잘못된 가정, Scope 문제, Source 충돌, Unknown Capability는 Analysis로 돌아갑니다.

[필수 Gate](Code-Agent-Kit/ko/prompts/GATE.md)를 참고하세요.

## 결정론적 Evidence

포함 Tool:

- Stack Readiness Validation
- State Model Validation
- Git Scope 및 Document Sync
- Generic Build Log Scanner
- Rendered SPA 추출
- Grid, Form, Button, KPI, Card, Chart, Matrix, Panel Evidence
- 빈 Visual Block 실패 처리
- Reference Image Hash, ICC, EXIF, Palette, Region, ΔE00 비교
- Static 및 Runtime Color Contrast
- Playwright E2E 및 선택형 Visual Baseline

모델의 “PASS” 선언은 Evidence가 아닙니다. Program Exit Code와 생성 Artifact가 Evidence입니다.

## 시작 순서

1. [시작하기](Code-Agent-Kit/ko/docs/getting-started/README.md)
2. [설계 개념 원장](DESIGN-CONCEPTS.ko.md)
3. [State 및 Memory Model](Code-Agent-Kit/ko/docs/core/state-and-memory-model.md)
4. [Stack 입력 요구사항](Code-Agent-Kit/ko/docs/getting-started/stack-input-requirements.md)
5. [작업 Prompt Router](Code-Agent-Kit/ko/prompts/README.md)
6. [React + ASP.NET Core Stack Profile](Code-Agent-Kit/ko/stacks/react-aspnetcore/README.md)
7. [TaskFlow Sample](Code-Agent-Kit/ko/samples/react-aspnetcore-taskflow/README.md)
8. [사람용 개발자 Guide](Code-Agent-Kit/ko/docs/human/developer-guide.md)

## 포함 구조

- 영문 기본·한국어 대응 Governance 문서와 Template
- Architecture Decision 및 Rejected Alternative
- Feature Current/History/Worklog Template
- System 및 Database Architecture State Template
- 완전한 Verified Stack Template Contract
- Ready 상태의 React + ASP.NET Core Sample Stack
- Owner 입력 전 Block된 Go + HTMX, Rust, Elixir Placeholder
- Codex, Roo Code, Zoo Code, Cline, Claude Code Adapter
- Project 범위 MCP 예제
- 결정론적 Tool 및 Self-test
- React + ASP.NET Core TaskFlow Sample

## Validation Layer

```text
Artifact / Compile
≠ Rendered Output
≠ Runtime Behavior
≠ Accessibility / Color
```

Build가 통과해도 화면이 비거나 Runtime이 실패할 수 있습니다. 적용되는 Layer를 각각 기록해야 합니다.

## Source Asset

- Image → 멀티모달 변형 전 Reference Image Manifest
- SPA → Rendered DOM 및 Screen Specification
- Static HTML → 원본 보존 및 제한된 구간 검사
- MCP/Search 결과 → Transcript가 아니라 압축 Fact와 Provenance

## Stack Profile

완전한 Stack Pack:

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
references/
skeletons/
validation/
```

사내 Library 이름과 조직 전용 Rule은 Generic Core가 아니라 관련 비공개 Stack Pack에 둡니다.

## 지원 코딩 Agent

- Codex
- Roo Code
- Zoo Code
- Cline
- Claude Code

Tool Adapter는 같은 `AGENTS.md`를 가리키며 Workflow를 다시 정의하지 않습니다.

## 강제화

정직이 우선입니다: 에이전트는 자기 실수를 스스로 보고하고, 불확실하면 추측 대신 멈추며, "완료"를 "검증 통과"로만 간주합니다(`AGENTS.md`). 모델이 자기 채점을 신뢰할 수 없으므로, 규칙은 요청이 아니라 기계로 강제됩니다:

- **커밋 게이트**와 **CI**(`tools/enforce-agent-gates`)가 워크로그·5단계 Gate·상태 동기화 없이 소스를 바꾼 커밋을 차단합니다;
- **세척 게이트**(`tools/check-sanitization`)가 공개 전 조직·독점 명칭을 차단합니다.

커밋 게이트 켜기: `scripts/install-hooks.sh`(Windows는 `install-hooks.ps1`). 자세한 건 enforcement matrix, 선택적 에이전트 스탠스는 `docs/persona.md`.

## 라이선스

프로젝트 전체가 **MIT License**로 배포됩니다([LICENSE](LICENSE)) — 상업적·비공개 사용 자유, 저작권 고지만 유지. 피드백은 환영하지만 의무 아님.

