# Stack 입력 — Vue.js

이 File에는 아무것도 채워져 있지 않습니다. 누락이 아니라 그것이 현재 상태입니다. 각 행은 Kit이 도출할
수 없는 *당신의* Project에 대한 Fact이고, Evidence로 답이 채워지기 전까지 `STACK-READINESS.json`은
`blocked`을 선언합니다.

Evidence는 **측정**됩니다. `check-stack-readiness`가 각 경로를 Tree에 대조하므로, 존재하지 않는
경로는 Evidence가 아닙니다.

**이 표와 `STACK-READINESS.json`은 일치해야 합니다.** 둘은 `Key` 열로 Join되어 비교되고, 어긋나면
보고됩니다. 그 보고는 Warning이고 Warning은 `provisional`을 도출하므로, 두 File이 어긋난 채 `ready`를
선언하는 Stack은 실패합니다. 양쪽을 함께 채우거나, Interview Prompt(`prompts/8-fill-stack.md`)를
실행해 Agent가 둘을 맞춰 두게 합니다.

## Owner 확인

| 입력 | Key | 필수 | 값 또는 경로 | Evidence | 상태 |
|---|---|---:|---|---|---|
| 지원 범위가 아니라 실제로 쓰는 정확한 Version. Project 자체 Manifest와 Validation을 실행하는 장비의 Toolchain에서 읽습니다. | `runtime-sdk-versions` | yes | | | unknown |
| 이 Stack에서 어떤 문서 Source가 Authoritative이고 어떤 것을 참조하면 안 되는지. mcp/source-routing.md에 기록합니다. | `authoritative-sources` | yes | | | unknown |
| 이 Codebase에서 무엇을 Feature 하나로 치는지, 그리고 Feature가 무엇을 건드릴 수 있는지. | `feature-model` | yes | | | unknown |
| 정확한 Build, Test, Lint 명령과 그 실패의 모습. 아무도 실행해 본 적 없는 명령은 Validation Profile이 아닙니다. | `validation-profile` | yes | | | unknown |
| 이 Stack의 자료를 공개 Repository에 둘 수 있는지 여부. | `confidentiality` | yes | | | unknown |

## Capability 결정

아래 Capability는 각각 Evidence와 함께 `present`, `absent`, `not-applicable` 중 하나로 확정되어야
합니다. 그전까지는 `capability-detection.md`의 Unknown Rule이 적용되어, 추측 대신 의존 작업을
차단합니다.

| Capability | 결정 | Evidence | 상태 |
|---|---|---|---|
| `major-version` | | | unknown |
| `build-tool` | | | unknown |
| `state-management` | | | unknown |
| `test-runner` | | | unknown |
| `typescript` | | | unknown |

## 자동으로 Detection된 Evidence

| 항목 | Detection 방법 | 결과 | Evidence |
|---|---|---|---|
| Package 또는 Project Manifest | Repository에서 읽음 | | |
| Toolchain Version | Validation 실행 장비에서 실행 | | |
| 기존 Test와 Build Script | Repository에서 읽음 | | |

## 차단 중인 Unknown

- `⟨확인 필요: 위의 모든 행⟩`
