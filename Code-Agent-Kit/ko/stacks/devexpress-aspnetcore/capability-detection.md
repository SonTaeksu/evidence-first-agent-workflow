# Capability Detection — DevExpress for ASP.NET Core

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이 확정적이지
않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다. 한 번의 잘못된 추측이 잠시
멈추는 것보다 비쌉니다.

이 Stack은 선택적인 부분이 더 많기 때문에 대부분의 Stack보다 Capability가 많습니다.
Project File의 DevExpress 참조 하나는 그 자체로 거의 아무것도 말해 주지 않습니다. 어느
Component 제품군을 쓰는지도, Reporting이 Hosting되는지도, Reporting에 필요한 조각들이
있는지도 말해 주지 않습니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | Restore 출력이나 Lock File에서 해석된 DevExpress Package Version — Project File의 범위가 아님 | 그 Version의 규칙 안에서 답하고 문서 조회를 거기에 고정 | Owner에게 확인 | Version에 민감한 모든 API 사용 차단; MCP 문서 Version 고정 차단 |
| ui-component-layer | 어떤 DevExpress Package가 참조되는지, 그리고 View가 Server에서 Component를 설정하는지 Script가 브라우저에서 Widget을 설정하는지 | Codebase의 그 영역에서 이미 쓰이는 Layer를 따름 | 둘 중 하나를 도입하기 전에 Owner에게 확인 | 어느 종류든 Component 추가 차단 |
| page-model | Project에 View를 가진 Controller가 있는지, Page Model이 있는지, 둘 다인지 | 그 영역의 기존 Model을 따름 | Owner에게 확인 | Page나 Controller 추가 차단 |
| reporting-host | Application 시작의 Reporting Service 등록, 그리고 Viewer와 Designer가 제공되는 Endpoint 또는 Handler | 기존 Host를 확장 | Host를 추가하는 대신 Reporting이 Hosting되지 않는다고 보고 | Report Viewer나 Designer Host의 추가 또는 변경 차단 |
| report-storage | `ReportStorageWebExtension`에서 파생된 구현과 그 등록 | 기존 Storage와 그 주소 지정 관례를 사용 | Storage가 없다고 보고 — Designer는 그것 없이 열지도 저장하지도 못함 | Designer에서 Report를 열거나 저장하는 것 차단 |
| client-resource-delivery | 정적 및 Bundling된 Asset이 브라우저에 도달하는 방식: 정적 파일 설정, Layout, 그리고 Bundling 설정 | 기존 메커니즘을 통해 Asset 추가 | Owner에게 확인 | Client-side Asset이 필요한 Component 추가 차단 |

## `ui-component-layer`가 먼저인 이유

DevExpress for ASP.NET Core는 한 브랜드 아래의 두 제품입니다. Server에서 설정되고
Rendering되는 tag helper 기반 Server-side Control, 그리고 JavaScript로 설정되고 브라우저에서
Rendering되는 DevExtreme의 Client-side Widget입니다. 문서도, 설정 표면도, 실패 양상도
따로입니다.

Project가 어느 쪽을 쓰는지 정하지 않은 Agent는 읽기에 맞고 경우에 따라 Compile되지만 다른
제품에 속하는 Code를 만들어 냅니다. 이 Capability가 경고가 아니라 차단하는 이유입니다.

한 Project가 영역별로 둘 다 쓸 수도 있습니다. 그래서 Detection은 Codebase의 영역별로
이루어지고, 답도 Repository 전체에 한 번이 아니라 영역별로 기록됩니다.

## Detection은 읽는 것이지 추론하는 것이 아닙니다

- Package 참조는 그 Package가 참조된다는 Evidence입니다. 거기서 나온 Component가
  쓰인다는 Evidence도, Reporting이 Hosting된다는 Evidence도 아닙니다.
- 시작 지점의 등록 호출은 무언가가 등록되었다는 Evidence입니다. 그것이 무엇을 등록하는지는
  Version에 민감한 사실이며, 기억이 아니라 조회로 확인합니다.
- Layout에서 참조되는 Asset은 Layout이 그것을 요청한다는 Evidence입니다. 실제로
  제공되는지는 별개의 확인입니다.

`⟨확인 필요: 이 Project가 사용하는 정확한 Package 식별자, 등록 호출, Asset 경로 — Project
에서 읽고, API 이름은 이 문서가 아니라 dxdocs로 확인할 것⟩`

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서 다시
언급되어야 합니다. 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수 있어야 하기
때문입니다.
