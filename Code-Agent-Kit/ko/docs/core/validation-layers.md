# Validation Layer

완료는 Boolean 하나가 아닙니다.

| Layer | 질문 | 대표 Evidence |
|---|---|---|
| Artifact / Compile | 정상 Framework Artifact가 생성됐는가 | Compiler, Generator, Schema, Build Exit Code |
| Rendered Output | 필요한 구조와 Content가 실제 표시됐는가 | Screen Specification, 비어 있지 않은 Visual Block, Screenshot Baseline |
| Runtime Behavior | 실제 Interaction과 Contract가 동작하는가 | Integration Test, E2E, Runtime Log |
| Accessibility / Color | Rendering 결과가 읽을 수 있고 Reference와 비교되는가 | axe, Computed Color, Contrast, ΔE00 |

다음 상태는 가능합니다.

```text
Artifact PASS
Rendered Output FAIL
Runtime PENDING
```

이 Feature는 완료가 아닙니다.

Stack은 Layer를 추가할 수 있지만 적용되는 구분을 하나로 합치면 안 됩니다.
