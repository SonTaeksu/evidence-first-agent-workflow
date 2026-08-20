# Pitfalls — DevExpress for ASP.NET Core

아래 각 항목은 기술 자체의 성질이며 어떤 Project와도 무관하게 확인할 수 있습니다. 이것들을
모아 둔 이유는 한 가지 특징을 공유하기 때문입니다. **실패가 조용하거나, Error Message가
원인이 아닌 다른 것을 가리킵니다.** 실패가 스스로를 알리는 Stack에는 이런 목록이 필요
없습니다.

## 두 Component 제품군이 한 브랜드를 공유합니다

DevExpress는 ASP.NET Core용 tag helper를 가진 Server-side Control을 제공하고, DevExtreme의
Client-side Widget도 제공합니다. 둘 다 "DevExpress Component"이고, 둘 다 같은 문서 사이트에
나오며, 둘 다 정답처럼 보이는 Sample을 가지고 있습니다. 잘못된 제품군의 조각은 스스로를
알리지 않습니다. 이 Project가 쓰지 않는 제품에 대해서는 유효한 Code이기 때문입니다.
무엇이든 쓰기 전에 `ui-component-layer`를 정합니다 — `capability-detection.md`를
참고합니다.

## Cache에서의 Restore는 Feed에 대해 아무것도 증명하지 않습니다

DevExpress Package는 자격 증명이 필요한 Private Feed에서 옵니다. Package가 이미 로컬
Cache에 있는 개발자 머신은 Feed에 접속하지 않고 Restore하므로, 깨졌거나 인증되지 않은 Feed
설정은 깨끗한 Agent가 시도하기 전까지 보이지 않습니다. 그때 실패는 CI에서, 다른 사람의
변경에서 도착합니다.

확인 방법은 따뜻한 Cache 없는 Restore를 문제의 그 머신에서 실행하는 것입니다.
`⟨확인 필요: 이 Project가 그것을 어떻게 수행하는지, 그리고 어느 Agent에서 하는지⟩`

## Reporting Package를 참조한다고 Reporting이 Hosting되지 않습니다

Report Designer와 Document Viewer는 **명시적 Service 등록**이 필요합니다. Package 참조를
추가하면 Compile되고 Application도 시작됩니다. 빠진 것은 요청이 실제로 그 Service를 필요로
할 때 드러나며, 그때는 배포 이후이고 Build에서 아무도 실행해 보지 않은 페이지에서입니다.

`⟨확인 필요: 이 Project의 DevExpress Version이 요구하는 정확한 등록. dxdocs로 조회할 것 —
기억으로 쓰지 말 것⟩`

## Client Asset 없는 등록은 빈 페이지를 Rendering합니다

Viewer와 Designer는 브라우저 Component입니다. 필요한 정적 또는 Bundling된 리소스가
제공되지 않으면 Server는 상태 200으로 페이지를 반환하고, 요청 Log는 건강해 보이며,
Component는 그냥 거기 없습니다. 진단은 Application Log가 아니라 브라우저 Console에
있습니다.

각각만으로는 충분하지 않으므로 두 가지를 따로 확인합니다. Asset이 배포된 출력물에
존재한다는 것, 그리고 Application이 페이지가 요청하는 경로에서 그것을 제공하도록 설정되어
있다는 것입니다.

## `ReportStorageWebExtension`은 확장점이지 기본값이 아닙니다

Report Storage는 Project가 구현하는 것입니다. 구현하기 전까지 Designer는 Report를 열 곳도
저장할 곳도 없습니다. 이 실패의 특징적인 모습은 부분적이라는 점입니다. 구현되지 않은
Member는 Build Error가 아니므로 Designer는 로딩되고, 아무것도 나열하지 않거나 무언가를
나열하며, 그러다 사용자가 저장을 누르는 순간 실패합니다. 결함이 심어진 시점이 아니라
사용자의 작업이 사라지는 시점입니다.

확장점이 정의하는 모든 Member를 구현하고, 저장 경로를 특별히 Test합니다. 아무도 실행해
보지 않는 것이 그것입니다.

## Report 정의는 Field 이름에 Binding되고, 아무것도 그것을 확인하지 않습니다

Report는 Binding할 Field의 이름을 지정합니다. 열 이름을 바꾸거나 결과 형태를 바꾸거나 View
Model을 재구성하면 Compiler는 만족하지만 Report는 Rendering 시점에 실패합니다. 게다가
Report는 보통 Schema 변경과 같은 Review에 있지 않으므로, 사용자가 Report를 열기 전까지
둘은 만나지 않습니다.

Report가 소비하는 Data 형태의 모든 변경은 Report의 변경입니다. 공유 파일 변경으로 다룹니다.
이유는 `feature-model.md`가 설명합니다.

## Desktop Host를 위해 작성된 Report는 같은 질문이 아닙니다

DevExpress Reporting은 Desktop과 Web을 아우릅니다. WinForms나 WPF Host에서 쓸 수 있는
Capability — 상호작용, Export 경로, Designer 동작 — 는 기본적으로 Web Host로 이전되지
않으며, 한쪽을 위해 쓰인 답은 다른 쪽에 성립하지 않습니다. 이 Profile은 Web Host만
다룹니다.

## 잘못된 `technologies` 값으로 한 문서 검색도 답을 내놓습니다

`devexpress_docs_search`는 닫힌 enum을 받고, Reporting은 **별개의** 값입니다. `AspNetCore`
안의 무언가가 아니라 `XtraReports`입니다. `AspNetCore` 하나로 보낸 Reporting 질문은 실패하지
않습니다. Component 말뭉치를 검색해 Component 항목을 돌려주고, 그것은 엉뚱한 주제에 관한
진짜 DevExpress 문서입니다. 이 실수는 답에서는 보이지 않고 인자에서만 보입니다. Reporting
에는 두 값을 함께 보내고, 측정된 enum은 `mcp/source-routing.md`를 참고합니다. 집합에 *없는*
값은 다르게, 그리고 더 친절하게 동작합니다. 답이 오는 대신 Schema에 대해 거부됩니다.

## 문서의 Version 고정은 v24.2에서 멈춥니다

문서 Endpoint는 v24.2보다 이른 Version 고정을 받지 않습니다. 더 오래된 Codebase에서는
고정할 지원 방법이 없으므로, 조회는 현행 문서가 말하는 무엇이든 돌려주고 그 불일치는
알려지지 않습니다. 그것은 우회할 방법이 아니라, 그런 Project에서 Version에 민감한 모든
답을 미해결로 다룰 이유입니다. `mcp/source-routing.md`를 참고합니다.
