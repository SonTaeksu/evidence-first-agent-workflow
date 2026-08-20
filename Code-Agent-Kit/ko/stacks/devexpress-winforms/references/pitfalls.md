# Pitfall — DevExpress WinForms

여기 있는 것은 모두 기술 자체의 속성이며 어떤 Project와도 무관하게 검증할 수 있습니다.
한 가지 특징을 공유하기 때문에 모아 두었습니다. **실패가 조용하거나, Error Message가 원인이
아닌 다른 것을 지목합니다.** 실패가 스스로를 알리는 Stack에는 이런 목록이 필요 없습니다.

[`../../csharp-winforms/references/pitfalls.md`](../../csharp-winforms/references/pitfalls.md)의
순수 Windows Forms Pitfall은 여전히 적용됩니다. 아래는 DevExpress가 더하는 것입니다.

## View 대신 Control을 구성하기

`GridControl`은 Data를 갖고, View가 Column Layout, 편집, Behaviour를 갖습니다. Control에
적용한 Behaviour 설정은 Compile되고 아무 효과가 없으므로, 증상은 Error가 아니라 "바꿨는데
아무 일도 안 일어난다"입니다 — 그리고 보통 다음 수순은 같은 잘못된 변경을 더 세게 하는
것입니다.

## Grid에 View가 정확히 하나라고 가정하기

Master-Detail이나 여러 Level이 있으면 "그 View"는 모호합니다. 잘못된 View에 적용된 변경은
사용자가 보고 있지 않은 표면에 성공적으로 적용됩니다.

## `LayoutControl`의 자식을 좌표로 배치하기

위치는 Layout Item에 속합니다. 자식의 좌표를 설정하면 Error 없이 버려지고, Control은 Layout이
놓은 자리에 나타납니다 — 이것은 Designer가 편집을 무시하는 것처럼 읽힙니다.

## Command Component 대신 Form에 Command 추가하기

`RibbonControl`이나 `BarManager`가 자기 Collection에 Item을 소유합니다. 그 밖에서 만들어져
남겨진 Item은 Code에 존재하고 화면에는 결코 나타나지 않습니다. 실패하는 것은 없습니다.
그저 그 Command가 없을 뿐입니다.

## Skin 아래에서 외관을 하드코딩하기

색상과 Font는 Skin이 결정합니다. Control 수준의 재정의는 Skin에 지거나, 이기고서
Application과 혼자만 다른 Control 하나를 만들어 냅니다 — 그리고 둘 중 어느 쪽이 일어나는지는
Code를 읽어서는 분명하지 않습니다.

## Application 전역 외관 설정을 너무 늦게 적용하기

이런 종류의 설정은 그 뒤에 만들어진 Control에 적용되므로, Form이 이미 생성된 뒤의 호출은
Exception이 아니라 일부만 Theme가 입혀진 Application을 만들어 냅니다. `⟨확인 필요: 이
Release에서 이것이 적용되는 설정이 무엇인지, 정확한 Member, 그리고 문서가 요구하는 호출
순서⟩`

## 이름이 비슷한 Windows Forms Type으로부터 추론하기

DevExpress Control은 그것이 닮은 `System.Windows.Forms` Control이 아닙니다. `GridControl`은
`DataGridView`가 아니며 Member는 이어지지 않습니다. 좋은 경우는 Compile Error이고, 나쁜
경우는 양쪽에 다 존재하면서 다른 것을 뜻하는 Member입니다.

## 고정된 Project에서 고정되지 않은 Endpoint를 참조하기

`dxdocs`는 최신 Release에서 답합니다. v24.2 Project에서 그것은 나중에 추가된 Member를 마치
사용 가능한 것처럼 서술합니다. 조회 시점에는 아무 Error도 나지 않습니다 — 비용은 Compile
시점에, 또는 그보다 늦게 도착합니다.

## Browser의 `405`를 장애로 취급하기

`https://api.devexpress.com/mcp/docs`는 Streamable HTTP만 씁니다. Browser GET은
`405 Method Not Allowed`를 반환하며, 문서는 그것이 예상된 응답이라고 적고 있습니다. 정상
동작하는 Server가 잘못된 Verb에 돌려주는 것이므로, Health Check도 아니고 결함도 아닙니다.

## Build Agent에 개발자 Machine과 같은 것이 있다고 가정하기

DevExpress에는 License가 걸려 있습니다. Local에서는 통과하고 Agent에서 실패하는 Build는
Code 결함이 아니라 Licensing 또는 Feed 구성에 관한 Finding이며, 그것을 Code 결함으로 읽으면
다음 변경이 엉뚱한 방향으로 갑니다.

## Build를 통과시키려고 `licenses.licx`를 수기 편집하기

그것은 생성된 Build 입력입니다. 편집은 License가 없는 이유를 고치는 것이 아니라 Licensing
Artifact를 바꾸는 일이고, 원래의 실패는 다음 Machine에서 되돌아옵니다.
