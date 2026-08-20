# Feature Model — Next.js

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

## 명명 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
