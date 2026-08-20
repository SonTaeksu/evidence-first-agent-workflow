# Feature Model — DevExpress WPF (v24.2+)

## Feature 하나란 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 도출할 수 없습니다. 추측으로 정한 Feature 경계는 아무것도 설명하지 못하는
State 문서를 만들고, Project Map은 쓸모없어집니다.

## Feature가 건드릴 수 있는 것

경계가 확정되기 전까지는 다음을 작업 규칙으로 삼고, 여기서 벗어나는 경우는 모두
기록합니다.

- Feature 하나는 자기 디렉터리 또는 Module을 소유하고, 공유는 이미 존재하는 Interface를
  통해서만 한다;
- 두 Feature가 공유하는 것을 바꾸면 Shared File 변경이며, Project Map의 역인덱스에
  기록한다;
- Capability 결정은 그것이 처음 필요한 Feature에 속하며, 반복하지 않고 기록한다.

이 Stack에서 두 가지는 구조상 공유되며, 아무리 작아 보여도 Shared File 변경입니다.

- **Theme.** 시작 시 한 번 적용되고 모든 Themed Window가 그것을 물려받으므로, Theme 변경은
  Application 전체의 변경이며 호소할 만한 국소적 영향 범위가 없습니다.
- **저장된 Docking Layout.** Panel은 그것을 도입한 Feature가 아니라 Layout에 속합니다.
  하나를 더하거나 빼는 것은 저장된 모든 Layout의 의미를 바꾸며, 여기에는 이전 Build가
  저장한 Layout도 포함됩니다.

## 명명 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
