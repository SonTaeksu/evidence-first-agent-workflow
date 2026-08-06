# Feature Model — Go

## Feature 하나란 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 스스로 알아낼 수 없습니다. 추측으로 정한 Feature 경계는 아무것도
설명하지 못하는 State 문서를 만들고, Project Map은 쓸모를 잃습니다.

## Feature가 건드릴 수 있는 범위

경계가 확인되기 전까지는 다음을 잠정 규칙으로 삼고, 여기서 벗어난 경우는 빠짐없이
기록합니다.

- Feature 하나는 자신의 Directory나 Module을 소유하고, 이미 존재하는 Interface로만
  공유합니다;
- 두 Feature가 공유하는 것을 바꾸면 Shared-file 변경이며, Project Map의 역Index에
  기록합니다;
- Capability 결정은 그것을 처음 필요로 한 Feature에 속하며, 반복하지 않고 기록합니다.

## 명명 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
