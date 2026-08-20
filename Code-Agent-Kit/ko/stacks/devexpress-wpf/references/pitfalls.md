# Pitfall — DevExpress WPF (v24.2+)

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

`../../csharp-wpf/references/pitfalls.md`의 평범한 WPF 목록도 그대로 적용됩니다. 조용한
Binding 실패, 상속되는 `DataContext`, Thread 밖에서의 Collection 갱신, Resource 조회 순서가
그것입니다. 이 File은 DevExpress가 더하는 것만 담습니다.

## View가 아니라 Grid를 구성한다

`GridControl`은 Data를 들고 있고, 표현과 편집을 정하는 것은 View — `TableView`, `CardView` —
입니다. 어떤 View Type을 위해 찾은 답이 다른 View Type이나 Grid에서도 받아들여지면서
읽는 사람이 기대한 일은 하지 않는 경우가 잦습니다. 증상은 적용된 것처럼 보이는데 아무런
효과가 없는 설정입니다.

## 끝내 배포되지 않은 Theme Assembly

Theme Assembly는 Runtime에 이름으로 해석되므로, Compile된 참조가 그것을 가리키지 않고
Build는 그것이 없다는 것을 알아채지 못합니다. Application은 시작되고, 실행되고, 잘못 보입니다.
개발자 Machine에서는 이것이 보이지 않습니다. 그 Disk에 전체 설치본이 있기 때문입니다.

## 첫 창이 만들어진 뒤에 적용한 Theme

창은 생성될 때 자기 외형을 해석합니다. 그 시점 이후에 Theme을 설정하는 것은 오류가 아니고
아무런 Message도 내지 않습니다. 이미 만들어진 창들은 그냥 가지고 있던 것을 유지합니다.
결과는, 가장 중요한 창 하나 — 첫 창 — 만 빼고 Theme이 적용된 Application입니다.

## Theme이 걸린 Application 속의 평범한 `Window`

DevExpress Theming에 참여하는 창만 그 Theme이 적용됩니다. 나중에 추가한 평범한 `Window`는
아니고, 아무도 불평하지 않습니다. Application은 망가져 보이는 것이 아니라 덜 만들어진 것처럼
보이고, 그래서 그대로 출시됩니다.

## 한 View 안에 섞인 Binding 방언

DevExpress Binding과 Command Markup Extension은 식을 받고, 평범한 `Binding`은 Property
Path를 받습니다. 둘 다 같은 File에서 유효합니다. 한 방언의 Rule을 다른 방언의 줄에 적용한
독자는 — 사람이든 Agent든 — Parsing은 되면서 다른 일을 하는 구성을 얻습니다.
`⟨확인 필요: 이 Project에서 실패한 DevExpress Binding 식이 어디에 보고되는지 — 일부러
하나를 망가뜨려 관찰해서 확정⟩`

## POCO View Model은 당신이 작성한 Class가 아니다

DevExpress POCO 방식은 평범한 Class로부터 Runtime에 확장된 Type을 만들어 냅니다. 따라서
Reflection, 직렬화, 구체 Type에 의한 동등성 비교, 선언된 Class에 대한 Pattern Matching이
모두 Source File이 시사하는 것과 다르게 동작할 수 있으며, 어느 지점에서도 오류는 나지
않습니다.

## 한 Solution 안의 MVVM Framework 둘

DevExpress MVVM Framework와 제3자 Framework를 모두 참조하는 Project에는 Command Type이 둘,
알림 Base가 둘 있습니다. View Model 사이에서 복사된 Code는 Compile된 다음 알림을 내지
않거나 활성화를 하지 않으며, 그 이유는 Diff 어디에도 보이지 않습니다.

## 복원된 Docking Layout이 XAML을 덮어쓴다

Docking Layout을 사용자별로 저장했다가 시작할 때 복원하는 곳에서는, XAML에서 한 Layout
변경이 더 오래된 저장 Layout으로 조용히 대체되고, XAML에서 지운 Panel이 다시 나타날 수
있습니다. 개발자가 내리는 결론 — "내 변경이 안 먹었다" — 은 원인을 잘못 지목하고, 이어지는
통상적인 다음 단계는 그 변경을 다시 하는 것입니다.

## 엉뚱한 Version에서 온 DevExpress 답

DevExpress는 .NET과 무관하게 자기 Control에 Version을 매깁니다. 다른 Version의 Member가
여전히 존재하는 경우가 잦고, 그래서 Code는 Compile되고 차이는 동작으로 드러납니다.
`mcp/source-routing.md`가 최신을 조회하지 말고 문서 Server를 고정하라고 고집하는 이유는
오직 이것입니다.
