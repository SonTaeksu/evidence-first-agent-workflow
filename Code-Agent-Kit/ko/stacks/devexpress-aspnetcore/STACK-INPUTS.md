# Stack Inputs — DevExpress for ASP.NET Core

이 파일은 아무것도 채워져 있지 않으며, 그것은 누락이 아니라 현재 상태입니다. 각 행은 Kit이
도출할 수 없는 *당신의* Project에 관한 사실이고, Evidence로 답변되기 전까지
`STACK-READINESS.json`은 `blocked`를 선언합니다.

Evidence는 **측정됩니다**. `check-stack-readiness`가 각 경로를 Tree에 대해 해석하므로,
존재하지 않는 경로는 Evidence가 아닙니다.

**이 표와 `STACK-READINESS.json`은 일치해야 합니다.** 둘은 `Key` 열로 Join되어 비교되고,
불일치는 보고됩니다. 그 보고가 경고이고 경고는 `provisional`을 도출하므로, 두 파일이
불일치하는 상태에서 `ready`를 선언하는 Stack은 실패합니다. 둘 다 채우거나, Interview
Prompt(`prompts/8-fill-stack.md`)를 실행해 Agent가 둘을 맞춰 나가도록 합니다.

이 Stack에는 다른 Stack에 없는 입력이 하나 있습니다. DevExpress Package가 **자격 증명이
필요한 Private Feed**에서 온다는 것입니다. 그래서 `devexpress-package-source`는 Detection이
해결할 수 있는 것이 아니라 Owner가 답해야 하는 필수 입력입니다. 따뜻한 Package Cache를
가진 머신은 문제없이 Restore하지만 Feed에 대해 아무것도 증명하지 못합니다.

## Owner 확인

| 입력 | Key | 필수 | 값 또는 경로 | Evidence | 상태 |
|---|---|---:|---|---|---|
| 정확한 .NET Target Framework와 SDK, 그리고 정확한 DevExpress Package Version — 지원 범위가 아닙니다. Project File, Restore 출력, 그리고 Validation을 실행하는 머신의 Toolchain에서 읽습니다. | `runtime-sdk-versions` | yes | | | unknown |
| 이 Project가 어느 DevExpress Feed에서 Restore하는지, 자격 증명이 어디서 오는지, 그리고 Build Agent가 그것을 가지고 있는지. 개발자 머신에서 성공한 Restore는 Feed가 설정되어 있다는 Evidence가 아닙니다. | `devexpress-package-source` | yes | | | unknown |
| DevExpress에 대해 어떤 문서 Source가 권위 있고 평범한 ASP.NET Core에 대해서는 어느 것이며, 둘 중 어느 쪽에도 참조하면 안 되는 것은 무엇인지. mcp/source-routing.md에 기록합니다. | `authoritative-sources` | yes | | | unknown |
| 이 Codebase에서 무엇이 하나의 Feature이고 Feature가 무엇을 건드릴 수 있는지 — Report 정의가 Feature에 속하는지 자체 수명주기를 갖는지 포함. | `feature-model` | yes | | | unknown |
| 정확한 Build, Test, Lint 명령과 그 실패가 어떤 모습인지. 아무도 실행해 보지 않은 명령은 Validation Profile이 아닙니다. | `validation-profile` | yes | | | unknown |
| 이 Stack의 자료가 공개 Repository에 나타나도 되는지. Report 정의는 연결 정보를 담고 있으며, 라이선스 키가 또 다른 흔한 유출 경로입니다. | `confidentiality` | yes | | | unknown |

## Capability 결정

아래 각 Capability는 Evidence와 함께 `present`, `absent`, `not-applicable` 중 하나로
해결되어야 합니다. 그전까지는 `capability-detection.md`의 Unknown Rule이 적용되며, 추측
대신 의존 작업을 차단합니다.

| Capability | 결정 | Evidence | 상태 |
|---|---|---|---|
| `devexpress-version` | | | unknown |
| `ui-component-layer` | | | unknown |
| `page-model` | | | unknown |
| `reporting-host` | | | unknown |
| `report-storage` | | | unknown |
| `client-resource-delivery` | | | unknown |

## 자동으로 Detection되는 Evidence

| 항목 | Detection 방법 | 결과 | Evidence |
|---|---|---|---|
| Project File과 그 Package 참조 | Repository에서 읽음 | | |
| NuGet이 실제로 읽는 Feed 설정 | Repository와 Build Agent에서 읽음 | | |
| Application 시작과 Service 등록 | Repository에서 읽음 | | |
| View, Layout, 그리고 그것들이 참조하는 Asset | Repository에서 읽음 | | |
| Report 정의와 그것이 저장되는 위치 | Repository에서 읽음 | | |
| Toolchain Version | Validation 머신에서 실행 | | |
| 기존 Test와 Build Script | Repository에서 읽음 | | |

## 차단하는 Unknown

- `⟨확인 필요: 위의 모든 행⟩`
