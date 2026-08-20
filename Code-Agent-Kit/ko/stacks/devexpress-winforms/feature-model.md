# Feature Model — DevExpress WinForms

## Feature 하나란 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 도출할 수 없습니다. 추측으로 정한 Feature 경계는 아무것도 설명하지 못하는
State 문서를 만들고, Project Map은 쓸모없어집니다.

## Feature가 건드릴 수 있는 것

경계가 확정되기 전까지는 다음을 작업 규칙으로 삼고, 여기서 벗어나는 경우는 모두
기록합니다.

- Feature 하나는 자기 화면 — Form 또는 Modal Dialog — 을 그 Service 경계, Designer File,
  Test와 함께 소유한다;
- 같은 화면 State를 공유하는 동작은 한 Feature에 함께 둔다: Load, Filter, 편집, Validation,
  저장, 취소;
- 두 Feature가 공유하는 것을 바꾸면 Shared File 변경이며, Project Map의 역인덱스에
  기록한다;
- Capability 결정은 그것이 처음 필요한 Feature에 속하며, 반복하지 않고 기록한다.

## 선언해야 하는 공유 의존성

이들 중 어느 것을 바꾸든 영향받는 화면과 실행한 Regression 검사를 함께 제시합니다. 앞의
세 가지가 이 Stack을 순수 Windows Forms와 다르게 만드는 지점입니다. DevExpress는 여러
결정을 화면에서 Application으로 옮깁니다.

- Application 전역 Skin 또는 외관 구성 — 모든 화면에 도달합니다;
- `DevExpress.Utils`의 공유 외관 또는 Utility Type으로, 둘 이상의 Control이 쓰는 것;
- 공유 Command 표면: 둘 이상의 Form이 상속하거나 재사용하는 Ribbon 또는 Bar Layout;
- Behaviour를 소유하고 둘 이상의 화면이 소비하는 재사용 User Control;
- Form이 호출하는 Service Interface;
- Base Form 또는 공유 Designer Partial.

## 명명 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`

## 분해 기준

Core Gate는 작업이 복잡도 기준을 넘을 때 Code보다 먼저 Todo Block 목록을 요구합니다. 이
Stack에서는 다음 중 하나라도 해당하면 Block 목록을 만듭니다:

- 한 화면에 Data Binding된 Grid나 List가 둘 이상이거나, Grid 하나에 View가 둘 이상인 경우;
- 저장되는 State를 바꾸는 사용자 동작이 셋 이상인 경우;
- 새 화면과 기존 Service Contract 변경이 함께 있는 경우;
- Control 하나가 아니라 Container 계층을 건드리는 Layout 변경;
- 공유 외관 구성이나 공유 Command 표면에 대한 모든 변경.
