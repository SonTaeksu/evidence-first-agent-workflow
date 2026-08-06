# Feature Model — Node.js

## Feature 하나가 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 스스로 도출할 수 없습니다. 추측한 Feature 경계는 아무것도 서술하지 못하는
State 문서를 만들고, 그러면 Project Map이 쓸모를 잃습니다.

## Feature가 건드릴 수 있는 범위

경계가 확정되기 전까지는 아래를 작업 Rule로 삼고, 여기서 벗어나는 경우는 모두
기록합니다.

- Feature 하나는 자기 디렉터리나 Module을 소유하고, 이미 존재하는 Interface를 통해서만
  공유합니다;
- 두 Feature가 공유하는 것을 바꾸는 일은 Shared File 변경이며 Project Map의 역인덱스에
  기록합니다;
- Capability 결정은 그것을 처음 필요로 한 Feature에 속하고, 반복하지 않고 기록합니다.

## Naming 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
