# Feature Model — WPF (.NET Framework 4.7.2+)

## Feature 하나란 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 도출할 수 없습니다. 추측한 Feature 경계는 아무것도 서술하지 못하는
상태 문서를 만들어 내고, 그러면 Project Map을 쓸 수 없게 됩니다.

## Feature가 건드려도 되는 범위

경계가 확정되기 전까지는 다음을 잠정 Rule로 삼고, 여기서 벗어나는 경우를 모두
기록합니다.

- Feature 하나는 자기 디렉터리 또는 Module을 소유하고, 이미 존재하는 Interface를
  통해서만 공유합니다;
- 두 Feature가 함께 쓰는 것에 대한 변경은 Shared File 변경이며 Project Map의 역
  Index에 기록합니다;
- Capability 결정은 그것을 처음 필요로 한 Feature에 속하며, 반복하지 않고 기록합니다.

## 명명 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
