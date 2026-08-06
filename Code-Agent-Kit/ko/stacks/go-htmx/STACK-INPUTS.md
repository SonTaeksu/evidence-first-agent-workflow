# Stack 입력 — Go + HTMX

이 File은 아무것도 채워져 있지 않으며, 그것은 빠뜨린 것이 아니라 현재 상태입니다.
각 행은 Kit이 스스로 도출할 수 없는 *당신의* Project에 관한 Fact이고,
`STACK-READINESS.json`은 그 답이 Evidence와 함께 채워질 때까지 `blocked`를
선언합니다.

Evidence는 **측정**됩니다. `check-stack-readiness`가 각 경로를 Tree에 대해 실제로
찾아보므로, 존재하지 않는 경로는 Evidence가 아닙니다.

**이 표와 `STACK-READINESS.json`은 서로 일치해야 합니다.** 두 File은 `Key` 열을
기준으로 Join되어 비교되고, 어긋나면 보고됩니다. 그 보고는 Warning이고 Warning은
`provisional`을 도출하므로, 두 File이 어긋난 채 `ready`를 선언한 Stack은
실패합니다. 둘 다 채우거나, Interview Prompt(`prompts/8-fill-stack.md`)를 실행해
Agent가 둘을 맞춰 두게 하십시오.

## Owner 확인

| 입력 | Key | 필수 | 값 또는 경로 | Evidence | 상태 |
|---|---|---:|---|---|---|
| 지원 범위가 아니라 실제로 쓰는 정확한 Version. Project 자체의 Manifest와 Validation을 실행하는 Machine의 Toolchain에서 읽습니다. | `runtime-sdk-versions` | yes | | | unknown |
| 이 Stack의 정본 문서 Source는 무엇이고, 어떤 Source를 이 Stack에 대해 참고해서는 안 되는지. mcp/source-routing.md에 기록합니다. | `authoritative-sources` | yes | | | unknown |
| 이 Codebase에서 Feature 하나로 치는 단위는 무엇이고, Feature가 건드려도 되는 범위는 어디까지인지. | `feature-model` | yes | | | unknown |
| 정확한 Build, Test, Lint 명령과 그 실패가 어떤 모습인지. 아무도 실행해 본 적 없는 명령은 Validation Profile이 아닙니다. | `validation-profile` | yes | | | unknown |
| 이 Stack의 내용이 공개 Repository에 나타나도 되는지 여부. | `confidentiality` | yes | | | unknown |

## Capability 결정

아래 Capability는 각각 Evidence와 함께 `present`, `absent`, `not-applicable` 중
하나로 확정되어야 합니다. 그 전까지는 `capability-detection.md`의 Unknown Rule이
적용되며, 추측하는 대신 의존하는 작업을 차단합니다.

| Capability | 결정 | Evidence | 상태 |
|---|---|---|---|
| `language-version` | | | unknown |
| `htmx-version` | | | unknown |
| `template-engine` | | | unknown |
| `fragment-convention` | | | unknown |

## 자동으로 Detection된 Evidence

| 항목 | Detection 방법 | 결과 | Evidence |
|---|---|---|---|
| Package 또는 Project Manifest | Repository에서 읽음 | | |
| Toolchain Version | Validation을 실행하는 Machine에서 실행 | | |
| 기존 Test와 Build Script | Repository에서 읽음 | | |

## Blocking Unknown

- `⟨확인 필요: 위의 모든 행⟩`
