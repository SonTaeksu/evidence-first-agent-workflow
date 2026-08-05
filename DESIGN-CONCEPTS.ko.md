# 설계 개념 원장

[English](DESIGN-CONCEPTS.md) | **한국어**

이 문서는 Workflow가 **왜** 이런 형태로 설계됐는지 기록합니다. 실제 실행 규칙은 `AGENTS.md`, `prompts/`, Stack Profile, Tool에 있습니다. 아래 개념을 의도적으로 바꾸는 경우 Architecture Decision에 이유를 남겨야 합니다.

## 0. 이 Workflow가 해결하는 문제

세 가지 반복 문제에서 출발합니다.

1. **모델은 니치·레거시·사내 Framework 사실을 안정적으로 추론할 수 없습니다.**  
   그럴듯한 API 이름은 Evidence가 아닙니다. Framework 지식은 검증된 Reference, 설치된 Artifact, 실제 Skeleton, Source 검사 또는 공식 문서에서 가져와야 합니다.

2. **소형·폐쇄망 모델은 규칙이 많아질수록 지시 준수가 무너집니다.**  
   수동 안내만으로 부족합니다. 짧은 Routing 문서, 고정 출력 Skeleton, 필수 Gate, Program Exit Code를 사용합니다.

3. **장기 Project의 비용은 상태 복원과 인수인계에서 커집니다.**  
   구현 상태, History, Evidence, 완료 기준을 Chat Session이 아니라 File에 저장합니다.

재사용 모델:

```text
Framework 비종속 Governance Core
+
검증된 Stack 또는 조직 Knowledge Pack
```

## A. Governance Model

### A1. 기억의 외부화와 점진적 공개

매 작업마다 Repository 전체를 다시 읽지 않습니다.

```text
Project Map
→ 기능 Current State
→ 역할별 Related Files
→ 미완료 작업이면 Active Worklog
→ 실제 Source
→ Evidence가 부족할 때만 Search
```

Project Map은 Routing하고, Feature Current는 검증된 현재 구현을 설명합니다. Code와 결정론적 Evidence가 최종 진실입니다.

### A2. 얇은 Root Rule과 선택 Routing

항상 읽는 `AGENTS.md`는 짧게 유지합니다. 세부 절차는 다음에 둡니다.

- `prompts/`
- `docs/core/`
- `stacks/<stack>/`
- `tools/*/README.md`

Stack `SKILL.md`는 가장 작은 관련 Reference로 Routing합니다. 모델이 이미 알고 있는 일반 Framework Tutorial을 단지 존재한다는 이유로 Knowledge Pack에 복사하지 않습니다.

### A3. 필수 5단계 Gate

File을 만드는 모든 작업은 다음을 따릅니다.

```text
1 Analysis
→ 2 Task
→ 3 Todo와 Micro-Verify
→ 4 Checklist
→ 5 Verification
```

다섯 Header는 권장 사항이 아니라 출력 Skeleton입니다. 단계가 빠지면 Gate를 완료하지 않은 것입니다.

Todo 내부의 작은 실패는 그 Todo만 반복합니다. 가정·범위·Capability가 잘못됐으면 Analysis로 돌아갑니다.

### A4. Current, History, Worklog는 서로 다른 문서

```text
current
= 기능의 지속적이고 검증된 현재 상태
= 이후 수정 작업의 필수 시작점

history
= Append-only 변경 기록
= 이전 Entry를 조용히 수정하거나 삭제하지 않음

worklog
= 미완료 작업의 임시 Checkpoint
= Gate 진행, Todo, 추출 Evidence, Resume Point
= current를 대체하지 않음
```

새 Session에서 Worklog로 대상 기능을 확인할 수 있지만, 재개 전에 Git 상태, Project Map, Feature Current를 다시 읽습니다.

### A5. Definition of Done

완료에는 다음이 필요합니다.

- 결정론적 Validation
- Current State 갱신 및 검증 Commit 연결
- 가능한 경우 Commit과 PR을 포함한 Append-only History
- Project Map과 Shared File Reverse Index 갱신
- Active Worklog 완료 또는 Archive
- 최종 Git Diff 검토
- 해결되지 않은 검사는 `PASS`가 아니라 `PENDING`

### A6. Routing 및 영향 분석용 Project Map

Project Map에는 다음이 있습니다.

- Feature Routing
- Current/History/Worklog 경로
- Entry Point
- Architecture State 문서
- Environment Capability 결정
- Shared File Reverse Dependency와 필요한 Regression

## B. 정직성과 Evidence

### B1. 정직한 불확실성

확인되지 않은 정보는 다음처럼 기록합니다.

```text
⟨확인 필요: 무엇을 어떻게 확인할지⟩
```

값을 추측하는 것은 진척이 아닙니다. 이전 진단이 틀렸음을 발견하면 계속하기 전에 Correction을 기록합니다. 결과만 맞고 설명이 틀리면 검증된 것으로 보지 않습니다.

### B2. Artifact, Rendered Output, Runtime은 별도 Gate

```text
Artifact 또는 Compile 성공
≠ Rendered Output 충실도
≠ Runtime 동작
```

Build가 성공해도 Visual Block이 비거나 Runtime이 실패할 수 있습니다. UI 작업은 적용되는 세 Layer를 각각 기록합니다.

**Stack에 Rendered 문서가 없으면 그 Layer는 대체하는 것이지 없애는 것이 아닙니다.** 데스크톱 UI Framework는 애플리케이션을 띄우지 않고는 프로그램이 검사할 대상을 아무것도 만들지 않을 수 있습니다. 그때 Rendered Output Layer를 "Build 성공"으로 붕괴시키고 싶어지는데, 그것이 바로 이 개념이 막으려는 실패입니다. Stack Pack은 구현 이전에 작성된 명세와 프로그램이 대조할 수 있는 대체 선언을 제공해야 합니다. C# Windows Forms 팩은 Designer File의 Control Tree를 파싱해 이를 해결합니다. `stacks/csharp-winforms/references/ui-evidence-contract.md` 참고.

### B3. 1차 Source Provenance

Stack Fact에 다음을 기록합니다.

- Claim
- Source 유형과 위치
- Version
- Verification Method
- Verification Date
- Confidence
- Evidence가 없을 때 미확인 Placeholder

공식 문서, 설치 SDK File, Source Repository, Binary/API 검사, 공식 Sample, 사용자 제공 정본 자료를 사용할 수 있습니다.

## C. Capability 강제

중요한 환경 분기는 작은 모델이 한 곳의 지시를 무시할 수 있으므로 세 Layer에서 강제합니다.

1. **Project Map**에 Capability와 Evidence 기록
2. **Gate Analysis 출력**에 선택한 구현 경로 기록
3. **Stack Rule**에서 확인 전 API나 Pattern 사용 금지

예:

- Shared API Client
- Generated SDK
- Authentication Provider
- ORM/Data Access 방식
- Runtime 및 SDK Version
- Shared Communication Library
- Design System
- Generated Code Ownership

Capability가 `unknown`이면 그 Capability에 의존하는 구현을 막습니다.

## D. Stack이 소유하는 개념

Generic Core가 모든 Framework Boundary를 결정하지 않습니다. 각 Stack Profile이 다음을 정의합니다.

- Feature Boundary와 Action Model
- 실제 Framework File로 만들어야 하는 Artifact
- 설치 Version 사용 규칙
- Communication 및 Data Contract
- Capability Detection
- 검증된 Fact와 Pitfall
- Skeleton 또는 Golden Reference
- Validation 명령과 실패 신호

Stack 고유 명칭과 사내 Library 이름은 Generic Core가 아니라 해당 공개 또는 비공개 Stack Pack에 둡니다.

## E. 결정론적 입력과 출력

### E1. 입력 전처리

- Image: 원본 Byte, ICC, EXIF, Pixel Hash, Palette, Region, 정규화 무손실 결과 보존
- SPA: JavaScript Rendering 후 Rendered DOM Hash와 구조 Evidence 추출
- Static HTML: 원본 보존 후 제한된 구간으로 읽기
- 큰 MCP/Search 결과: 필요한 Fact와 Provenance만 남기고 긴 원문을 다음 Session에 계속 넣지 않기

### E2. 출력 검사

정직 Rule은 모델이 자기 출력을 평가할 수 있다고 전제하지만, 약한 모델은 빈·깨진 Artifact도 "통과"로 표시합니다. 그래서 모델 자기신고는 결코 Gate가 아니며, Exit Code를 내는 결정론적 Tool이 Gate입니다. 자기평가는 통과 검사를 대체하지 못하고, 그 검사는 Agent가 선택할 때만이 아니라 자동으로(Commit·CI) 실행돼야 합니다. Tool이 다음을 검사합니다.

- Build/Test Exit Code
- 생성 Artifact
- Git Scope
- Screen 구조
- 필수 Column, Row, Control, Button, Visual Block
- 빈 Placeholder
- Color Contrast와 Runtime Color
- Stack Adapter가 지원하는 Binding 또는 Contract Evidence

### E3. Gate 설계와 오탐의 비용

Gate는 "실패 = 실제 결함"이라는 전제 위에서만 삽니다. 거짓 경보가 한 번 나면 그 전제가 깨지고, 운영자는 `--no-verify`를 쓰기 시작하며, Hook 전체가 무력해집니다. 오탐의 비용은 낭비된 1분이 아니라 가진 검사 전부입니다.

이는 통상의 직관을 뒤집습니다. 틀릴 수 있는 검사는 WARN에 두고, `BLOCK`은 실제 산출물에서 오탐 0을 관측한 뒤에만 주장합니다.

그런데 이 Rule을 단순 적용하면 사소한 것은 BLOCK인데 치명적인 것은 경고에 그치는 표가 만들어집니다. 그래서 Rule의 나머지 절반이 앞 절반만큼 중요합니다. **침묵 실패는 BLOCK이어야 합니다.** 시끄러운 실패 — Build 오류, 예외 — 는 다른 것이 드러내 주므로 경고여도 됩니다. 성공을 돌려주면서 0건인 응답, 빈 채로 그려지는 화면, 아무것도 안 하고 exit 0을 내는 실행은 드러내 줄 것이 없습니다. **확실하다는 것이 BLOCK할 수 있는 근거이고, 관측되지 않는다는 것이 BLOCK이어야 하는 이유입니다.**

같은 관측에서 나온 나머지 조건들:

- **탈출구는 암묵이 아니라 명시적 Marker입니다.** 모든 검사에는 출구가 필요합니다. 없으면 첫 정당한 예외에서 죽습니다. 그러나 그 출구는 "File이 이미 있으니까" 같은 정황이 아니라 **사람이 적은 의도 선언**입니다. 암묵 면제는 그것이 허용하려던 결함과 구분되지 않습니다.
- **Rule ID는 Tool의 소유입니다.** 검사가 실패할 때 자기 ID를 출력합니다. 모델에게 어떤 Rule을 만족했는지 태깅하게 하는 것은 건너뛰어지는 단계이고, 소형 모델은 항상 건너뜁니다. 모델의 협조 없이 살아남는 추적성만이 가질 가치가 있습니다.
- **판정 근거는 Project 문서에 있습니다.** "이 Project가 X를 쓰는가"를 모델이 판단해야 하는 검사는, 내일 다르게 판단하는 것으로 우회됩니다. 그 결정을 State 문서에 한 번 기록하고 검사가 읽게 합니다.
- **판단을 없애면 실행률이 오릅니다.** 어떤 File을 넘길지 골라야 하는 검사는 실행되지 않습니다. 인자를 정하는 것 자체가 단계이고, 그 단계가 건너뛰어집니다. Runner는 흔한 경우에 인자를 요구하지 않습니다.
- **내 산출물도 같은 실패를 합니다.** 킷이 복사하라고 지시한 Template은 수정 없이 킷 자신의 Validation을 통과해야 하고, 아니면 유일한 출구가 Gate 우회입니다. 산출물은 다시 읽지 말고 실측으로 검증하고, 문서는 diff와 카운트로 생성하세요. 손으로 옮겨 적은 숫자 하나하나가 문서가 조용히 낡는 자리입니다.

각 Rule이 어떤 관측된 실패에서 나왔는지를 포함한 전문은 `docs/core/gate-design-principles.md`에 있습니다.

## F. 버린 대안

다음 접근은 채택하지 않습니다.

- CRUD 동사마다 Current State File 분리
- 같은 Feature State를 공유하는 Action마다 큰 상세 Block 반복
- 모든 Reference를 매 Session 상시 Load
- Capability를 한 곳의 수동 안내로만 처리
- Build 성공을 Visual 또는 Runtime 성공으로 간주
- 사람용 Onboarding Guide를 Agent 기본 Context에 포함
- 예상 밖 변경 File을 조용히 허용
- 용어 현대화만을 위해 안정된 경로를 전면 Rename

버린 결정은 `docs/architecture/decisions/`에 기록해 다음 Agent가 이유 없이 되살리지 못하게 합니다.

## G. 운영 교훈

- 소형 모델은 항상 읽는 Rule을 줄이고 기계 Gate를 늘려야 합니다.
- 모델이 이미 아는 일반 지식은 Signal을 낮출 수 있습니다. Knowledge Pack은 Project 고유 또는 추론하기 어려운 Fact에 집중합니다.
- Session 압축은 설계 결정을 잃게 합니다. Current, History, Worklog, Decision 문서로 보호합니다.
- MCP 조회도 Context를 사용합니다. 검증된 Fact와 Provenance를 요약한 뒤 불필요한 Retrieval 원문은 버립니다.
- 니치 Framework Fact는 1차 Source로 검증해야 합니다.
- 관측은 진단이 아닙니다. 용어가 몇 번 나오는지 세는 것은 Rule에 범위 한정이 있는지에 대해 아무것도 말해주지 않습니다 — 범위 한정이 그 등장 중 하나일 수 있습니다. 위험한 결과는 놓친 결함이 아니라 잘못 읽은 것을 근거로 한 확신에 찬 수정입니다. 그것은 멀쩡한 산출물을 고치기 때문입니다.
- 손으로 적은 수치는 조용히 낡습니다. 생성하거나, 실측할 수 있는 규칙을 기록하세요. 둘 다 없는 수치는 검증 불가이고, 아무리 읽어도 결론이 나지 않습니다.
- 프로젝트가 자기 자신에 대해 쓴 검사는 프로젝트가 볼 수 없던 결함을 찾아냅니다. v0.1.9에서 수정한 결함 네 건 중 두 건을 킷의 새 자기검사가 첫 실행에서 찾았고, 나머지 두 건은 사람이 읽어서 찾았으며 여전히 기계로 검사할 수 없습니다.

## H. 공개 포지셔닝

Core는 Tool 비종속 Context Management 및 Development Governance Workflow입니다. 차별화 증거는 니치·레거시·사내 Stack의 검증 Knowledge Pack에서 나옵니다.

```text
Governance Core
+ 검증된 Stack Knowledge Pack
+ 실행 가능한 Sample
```

Generic Sample은 범용성을 증명하고, 실제 검증 Stack Pack은 왜 이 Workflow가 필요한지를 증명합니다.
