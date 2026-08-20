# Stack Profile — DevExpress WinForms

Windows Forms Desktop Application 위의 DevExpress Control이며, v24.2 이상이 대상입니다.

## `csharp-winforms`와의 관계

이 Profile은 [`../csharp-winforms`](../csharp-winforms/)의 대체가 아니라 **동반**
Profile입니다. 순수 Windows Forms 규칙은 그대로입니다. Designer가 `*.Designer.cs`를
소유하고, `.resx`는 Designer를 통해 편집하며, Control은 자신을 만든 Thread에 속하고,
Project Format이 `dotnet build`를 쓸 수 있는지 자체를 결정합니다. 아래 내용은 그중 어느
것도 폐기하지 않습니다. 아래는 전부 DevExpress가 더하는 것입니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것 — .NET Target, 그리고 지원 범위가 아니라 Package 또는 Assembly
참조에서 읽은 DevExpress Version⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## DevExpress Version

`⟨확인 필요: 이 Project가 실제로 참조하는 DevExpress Release, 그리고 Build하는 Machine에
같은 Release가 설치되어 있는지 여부⟩`

이것은 세부 사항이 아니라 첫 번째 분기입니다. 어떤 문서 Endpoint가 답하는지를 결정합니다 —
v24.2 Project에는 `dxdocs24_2`이고, Project가 정말로 최신 Release일 때만 `dxdocs`입니다.
`mcp/source-routing.md`를 참고합니다.

## 디렉터리 구조

순수 WinForms Layout 그대로입니다. Behaviour는 Form의 Partial Class에, Layout은 Designer
File에, Resource는 `.resx`에 둡니다.

`⟨확인 필요: 이 Project 자체의 관례 — Form이 어디에 사는지, 공유 Base Form이나 공유 외관
Module이 있는지, Application 전역 시작 구성이 어디서 수행되는지⟩`

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준, 그리고 DevExpress Assembly를
Build Machine에서 쓸 수 있게 만드는 방법⟩`

DevExpress Assembly는 .NET SDK의 일부가 아니라 License가 걸린 의존성이므로, 개발자
Machine에서는 되고 Agent에서는 실패하는 Build는 여기서 정상적인 결과이며, Code 결함이
아니라 구성에 관한 Finding입니다.

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다. 하나같이 Member 이름 없이 서술한 것은
의도한 것입니다. 그 이름들이야말로 기억이 아니라 조회해야 하는 대상입니다.

- **Control과 View는 서로 다른 Object입니다.** `GridControl`은 Data Source를 갖는 Binding
  Container이고, `GridView`는 그 위의 View이며, Column Layout, 편집, 정렬, Grouping,
  Behaviour가 사는 곳은 View입니다. Behaviour 설정을 Control에 적용하면 Compile되고 아무
  일도 일어나지 않으며, 이 Stack에서 작업이 사라지는 가장 흔한 방식이 바로 이것입니다.
- **Grid에는 View가 둘 이상 있을 수 있습니다.** `⟨확인 필요: 이 Project가 Master-Detail이나
  다중 View Level을 쓰는지, 그리고 주어진 변경이 어느 View를 대상으로 하는지⟩` 그런 경우
  "그 View"는 기본값이 아니라 질문입니다.
- **Command 표면은 Form이 아니라 Component가 소유합니다.** `RibbonControl`이나 `BarManager`가
  자기 Collection에 Item을 소유합니다. Command를 추가한다는 것은 그 Component가 Item을 두는
  곳에 추가한다는 뜻이고, 다른 곳에 추가된 Command는 존재하되 보이지 않습니다.
- **Ribbon과 `BarManager`는 Layer가 아니라 택일입니다.** Form이 어느 쪽을 쓰는지는 Project의
  결정입니다. `⟨확인 필요: 이 Project가 어떤 Command 표면을 쓰는지, 그리고 두 가지가 섞여
  있는 곳이 있는지⟩`
- **`LayoutControl`이 위치를 소유합니다.** 자식은 Layout Item을 통해 배치되므로 자식에
  설정한 좌표는 버려집니다. Error는 없습니다. Control은 그저 Layout이 정한 자리에
  나타납니다.
- **외관은 Control이 아니라 Skin이 결정합니다.** `XtraForm`과 Skin이 적용된 Control에서
  하드코딩된 색상이나 Font는 Theme의 재정의이며, 아무 효과가 없거나 아니면 나머지
  Application과 혼자만 다른 Control 하나를 만들어 냅니다.
- **Application 전역 외관 설정은 시작 시점 설정입니다.** `WindowsFormsSettings`가 그중 여럿이
  사는 곳이고, 이런 종류의 설정은 적용된 뒤에 만들어진 Control에만 효력을 갖습니다.
  `⟨확인 필요: 이 Project가 어떤 설정을 적용하는지, 정확한 Member, 그리고 문서가 요구하는
  호출 순서⟩`
- **`DevExpress.Utils`는 Control들이 공유합니다.** 거기 있는 외관 및 Utility Type을 여러
  Control이 동시에 쓰므로, 그곳의 변경은 Control을 가로지르는 변경이고 그 파급 범위는 해당
  Type을 쓰는 모든 화면입니다. `⟨확인 필요: 이 Project가 그중 어떤 Type을 실제로 쓰는지⟩`
- **Designer가 생성한 Code는 여기서 더 적지 않고 더 많습니다.** DevExpress Form은 순수
  Form보다 훨씬 많은 `InitializeComponent` 내용을 생성하고, Designer는 여전히 그 전부를 다시
  씁니다. 수기 편집은 여전히 사라집니다.
- **Licensing은 Build 시점의 Fact이자 Runtime의 Fact입니다.** DevExpress는 상용 Library이고,
  Windows Forms는 Component License를 `licenses.licx`에 기록하는데 이것은 Source Code가 아니라
  Build 입력입니다. `⟨확인 필요: 이 Project에 License File이 있는지, 그것이 Source Control에
  들어 있는지, 그리고 Build Agent가 Compile하려면 무엇이 필요한지⟩`
