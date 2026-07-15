# Verified Stack Extension Model

Core는 Stack 고유 Fact를 지어낼 수 없습니다. 완전한 Stack Profile은 문서와 Machine-checked Readiness Manifest를 모두 제공합니다.

```text
stacks/<name>/
├─ README.md
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
├─ mcp/
│  └─ source-routing.md
└─ validation/
   └─ validation-profile.md
```

## 책임 분리

### Core 제공

- State 및 Handoff Model
- 필수 Gate
- Capability 강제 Pattern
- 결정론적 Tool Contract
- Source Asset 전처리
- Git 및 문서 Governance

### Stack Owner 제공 또는 확인

- 지원 Version
- 1차 Source 및 설치 Artifact
- Feature Boundary
- Artifact 및 Communication Contract
- Capability Branch
- 검증 Pitfall 및 Fact
- Skeleton
- Validation 명령과 실패 Pattern
- 보안 Policy

### Tool Detection

- Manifest, Version, Import, File, Client, Generated Code, 기존 명령

자동 Detection은 조직 의도에 대한 Owner 확인을 대체하지 않습니다.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/<name>
```

- `ready`: 필수 입력 해결
- `provisional`: 독립 작업만 진행 가능
- `blocked`: 필수 입력 또는 Capability Unknown

## 3층 Capability 강제

1. Stack Detection Rule이 Evidence와 Branch 정의
2. Project Map이 Project별 결과 저장
3. Gate Analysis가 선택 경로를 반복하고 Stack Rule이 미확인 API 금지

사내 명칭은 비공개 Stack Pack에 남기고 Generic Core에는 재사용 Pattern만 둡니다.
