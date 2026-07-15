# Stack 입력 요구사항

Generic Workflow는 Stack 고유 Fact를 안전하게 지어낼 수 없습니다. 각 Stack Profile은 자동 Detection과 사용자 또는 Project Owner가 제공·확인하는 정보를 결합합니다.

## Readiness 상태

| 상태 | 의미 |
|---|---|
| ready | 필수 입력이 Detection, 확인 또는 명시적 Not Applicable 상태 |
| provisional | 미확인 입력에 의존하지 않는 작업만 진행 가능 |
| blocked | 필수 Unknown이 요청 구현에 영향을 줌 |

필수 정보가 Unknown이면 다음처럼 기록합니다.

```text
⟨확인 필요: 입력, 확인할 사람, 확인 방법⟩
```

## Tool이 보통 자동 확인할 수 있는 것

- Package 및 Project Manifest
- Runtime 또는 SDK Version File
- Import Package와 Namespace
- Shared Client, Generated Code, Config, Skeleton 존재 여부
- Repository에 저장된 Build/Test 명령
- Framework File 확장자와 Project Layout
- 기존 Authentication, Data Access, UI Library Reference

경로 존재는 Evidence지만 조직의 의도된 Policy까지 증명하지는 않습니다.

## 사용자 또는 Project Owner가 보통 제공·확인해야 하는 것

| 입력 | 필요한 이유 |
|---|---|
| 지원 Runtime 및 SDK Version | Example Version 복사와 사용할 수 없는 API 방지 |
| 정본 문서와 설치 Artifact | 모델이 추론할 수 없는 Fact Grounding |
| Golden Skeleton 또는 정상 Framework File | Schema, Metadata, Project 구조 환각 방지 |
| Feature Boundary와 Action Model | 이 Stack에서 Feature 하나가 무엇인지 정의 |
| 사내 Naming 및 File Convention | 일관되지 않은 Artifact 방지 |
| Communication 및 Data Contract | Entry Point, DTO/Data Mapping, Error Shape, Generated Client Ownership 정의 |
| Capability 분기 Rule | Shared Library, Client, Auth, ORM, Design System 유무에 따른 경로 정의 |
| Validation 명령과 실패 신호 | 완료를 결정론적 Gate로 변환 |
| Known Pitfall과 교정된 가정 | 같은 환각 반복 방지 |
| 보안 등급 | 비공개 Reference와 Asset의 공개 저장소 유입 방지 |
| Reference UI Asset과 Binding 기대 | 구조, Content, Color, 실데이터 치환 검증 |

## 최소 Stack Pack

```text
stacks/<stack>/
├─ STACK.md
├─ STACK-INPUTS.md
├─ STACK-READINESS.json
├─ AGENTS.stack.md
├─ SKILL.md
├─ capability-detection.md
├─ feature-model.md
├─ artifact-contract.md
├─ communication-contract.md
├─ evidence-provenance.md
├─ references/
│  ├─ _index.md
│  ├─ pitfalls.md
│  └─ verified-facts.md
├─ skeletons/
│  └─ README.md
└─ validation/
   └─ validation-profile.md
```

## 3층 강제

Code 생성 방식을 바꾸는 Capability는 다음 세 곳에 나타납니다.

1. Project Map Capability Table
2. Gate Analysis의 `Environment Capability Decision`
3. 확인 전 해당 Pattern을 금지하는 Stack Rule

## Onboarding 순서

1. `templates/stack-profile/` 복사
2. `STACK-INPUTS.md` 작성
3. 정본 Source와 Skeleton 추가
4. `STACK-READINESS.json` 완료
5. 실행:

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/<stack>
```

6. Blocking Unknown 해결
7. 선택된 Capability를 Project Map에 기록
8. 이후 Stack 의존 구현 시작

Validator는 Framework Fact의 정확성을 증명하지 않습니다. 필요한 Evidence와 Decision이 조용히 빠지지 않았음을 증명합니다.
