# Stack Profile — DevExpress WPF (v24.2+)

WPF Application 안에서 동작하는 DevExpress WPF Control이며 v24.2 이상입니다.

**[`../csharp-wpf`](../csharp-wpf)와 함께 쓰는 짝입니다.** 평범한 WPF와 MVVM Rule은
여기서 반복하지 않으며 여기서 뒤집히지도 않습니다. XAML Compile, Dependency Property,
Routed Event, Resource 조회, Dispatcher, Binding 실패는 `csharp-wpf`가 관할합니다. 이
문서는 DevExpress가 답을 바꾸는 지점만 다룹니다. DevExpress Type을 지목하지 않고도 답할
수 있는 질문이라면 그것은 다른 Profile의 몫입니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것 — .NET Target, 그리고 누군가 설치해 둔 Version이 아니라 Build가
해석한 DevExpress Version⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

구조상 이것은 WPF Application이므로 배치는 `../csharp-wpf/STACK.md`가 설명합니다. 알아 둘
만한 추가 사항:

- `App.xaml` / `App.xaml.cs` — DevExpress Theme이 적용되는 곳이고, 따라서 아래의 순서
  제약이 사는 곳입니다.
- DevExpress Control을 담는 `*.xaml` View — `GridControl`은 자기 `View`를 자식 Element로
  선언하므로, 화면의 동작은 Control이 아니라 그 Element에 있습니다.
- Project 또는 Package File — DevExpress Assembly는 한 묶음으로 Version이 매겨지고
  Licence가 걸린 Feed에서 복원됩니다. 그래서 이 File은 Version에 민감하면서 동시에
  사소한 사항이 아니라 Build의 선행 조건입니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

DevExpress Build에는 그 답에서 짚어 둘 만한 실패 방식이 하나 더 있습니다. 복원입니다.
`validation/validation-profile.md`를 참고합니다.

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다. 어느 하나에 대해 실제로 손을 쓰려면
정확한 Type이나 Member 이름이 필요한 경우, 기억으로 적지 않고 표시해 두었습니다.

### `GridControl`은 자기 `View`에 위임한다

`GridControl`은 Data와 선택 상태를 들고 있을 뿐, 행을 어떻게 그리고 어떻게 편집할지는
정하지 않습니다. 그것을 정하는 것은 View이며 — 여기서 이름을 대는 둘은 `TableView`와
`CardView`입니다 — View는 Grid 안에 선언됩니다. 그 결과는 이론이 아니라 실무의 문제입니다.
개발자가 구성하고 싶어 하는 것 대부분이 View에 있으므로, Grid에서 찾는 설정은 대개 그냥
없고, 어떤 View Type을 위해 쓰인 답은 둘 다 "그 Grid"인데도 다른 View Type으로 옮겨가지
않습니다. Grid에 관한 답을 적용하기 전에 항상 View Type을 먼저 확정하십시오.
`⟨확인 필요: 이 Project가 쓰는 View Type과 거기서 구성하는 Member — Project의 XAML과
dxdocs에서 확인⟩`

### `DXWindow` / `ThemedWindow`와 Theme 적재 순서

DevExpress Theme은 창이 DevExpress Theming에 참여할 때만 그 창에 적용되며, 참여하는 창
Type이 `DXWindow`와 `ThemedWindow`입니다. 같은 Application 안의 평범한 `Window`는 같은
방식으로 Theme이 적용되지 않으므로, 섞인 Application은 아무것도 실패하지 않은 채로
일관성 없이 보입니다.

Theme 선택은 순서에 의존합니다. 창은 생성될 때 자기 외형을 해석하므로, 첫 Themed Window가
만들어지기 전에 Theme이 정해져 있어야 합니다. 나중에 설정하는 것은 오류가 아니고 아무런
Message도 내지 않습니다. 이미 만들어진 창들이 그냥 가지고 있던 것을 유지할 뿐입니다.
`⟨확인 필요: 이 Project가 Theme을 선택하는 데 쓰는 정확한 API와 그것이 실행되는 시작
시점 — App.xaml.cs와 dxdocs에서 확인⟩`

### Theme Assembly는 배포 입력이다

DevExpress Theme은 `DevExpress.Xpf.Core` 옆의 Assembly로 배포되며, Compile된 Code는 그것을
이름으로 참조하지 않습니다. Theme이 Runtime에 값으로 선택되기 때문입니다. 따라서 Build의
어느 부분도 그것이 있어야 한다고 요구하지 않습니다. 그것을 빠뜨린 Application은 Build되고
Link되고 시작되고 실행됩니다. Fallback 외형으로, 아무런 진단 없이. 이 Stack에서 "내
Machine에서는 제대로 보였다"가 Evidence가 아닌 이유가 이것입니다. 개발자 Machine에는
전체 설치본이 있습니다.
`⟨확인 필요: 이 Project가 고른 Theme이 요구하는 Theme Assembly가 무엇인지, 그리고 그것이
Build 출력에 존재한다는 Evidence — Project File이 아니라 Publish된 출력에서 확인⟩`

### `DXBinding` / `DXCommand`는 `Binding`이 아니다

DevExpress는 Property Path가 아니라 식을 받는 자체 Markup Extension을 제공합니다. 둘은
줄임말이 아니라 서로 다른 방언입니다. 한쪽에서 유효한 식이 다른 쪽에서 반드시 유효한
Path인 것은 아니며, 둘은 실패를 서로 다른 곳에 보고합니다. 한 View 안에서 방언을 섞는
것은 문법상 허용되며 유지보수의 함정입니다. 읽는 사람이 줄마다 어느 Rule이 적용되는지
알아야 하기 때문입니다.
`⟨확인 필요: 이 Project의 구성에서 실패한 DevExpress Binding 식이 어디에 보고되는지 —
기억이 아니라 일부러 하나를 망가뜨려 관찰해서 확정⟩`

### DevExpress MVVM Framework 대 제3자 Framework

DevExpress는 자체 MVVM Framework를 함께 제공합니다. 통상적인 상속 기반 View Model을 위한
`ViewModelBase`, 그리고 평범한 Class로부터 Runtime에 확장된 Type을 만들어 내는 POCO
방식입니다. POCO 경로에는 사람들을 놀라게 하는 결과가 따릅니다. 실제로 쓰이는 Object가
작성된 그대로의 Class Instance가 아니므로, Reflection, 직렬화, 구체 Type에 의한 동등성
비교, 선언된 Class에 대한 Pattern Matching이 모두 Source가 시사하는 것과 다르게 동작할 수
있습니다.

여기에 제3자 MVVM Library까지 참조하는 Project라면 Command Type이 둘, 알림 Base Class가
둘, 관례가 둘이 되고, Code는 복사·붙여넣기로 그 사이를 오갑니다. 어느 쪽이 관할하는지는
취향이 아니라 Owner의 결정입니다.
`⟨확인 필요: 이 Project가 쓰는 MVVM Framework, 그리고 둘 다 존재하는지 여부 — Package
참조와 View Model Base Type에서 확인⟩`

### `DevExpress.Xpf.Docking`

Docking은 창의 Layout을 관리되는 Layout으로 대체합니다. Panel, Group, Document Host는
평범한 WPF Panel처럼 XAML Tree가 아니라 Docking Layout이 소유합니다. 그 Layout은 직렬화할
수 있고, Application은 흔히 사용자별로 그것을 저장했다가 시작할 때 복원합니다. 그 조합이
함정입니다. XAML에서 한 Layout 변경이 이전 Build에서 저장된 Layout으로 덮어써지므로 변경이
반영되지 않은 것처럼 보이고, XAML에서 지운 Panel이 옛 저장 Layout에 의해 되살아날 수
있습니다. 어느 경우에도 오류는 없습니다.
`⟨확인 필요: 이 Project가 Docking Layout을 저장하고 복원하는지, 어디에 저장하는지,
그리고 Panel 구성이 바뀌었을 때 저장된 Layout이 어떻게 되는지⟩`

### Version 사이로 답은 옮겨가지 않는다

DevExpress는 .NET과 무관하게 자체 주기로 Release합니다. Control의 Member와 기본값은 .NET
Target이 아니라 Build가 해석한 DevExpress Version의 속성입니다. 다른 Version에서 찾은 답은
여전히 Compile되는 경우가 잦고, 그래서 위험합니다. 권위는 Project 자체의 복원 출력에 있는
Version에 있습니다.
