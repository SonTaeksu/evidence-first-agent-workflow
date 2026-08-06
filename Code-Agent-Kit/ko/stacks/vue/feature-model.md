# Feature Model — Vue.js

## Feature 하나의 정의

`⟨확인 필요: the owner's definition of a feature boundary in this
codebase⟩`

Kit이 도출할 수 없습니다. 추측한 Feature 경계는 아무것도 서술하지 못하는 State 문서를 만들고,
Project Map은 쓸모를 잃습니다.

## Feature가 건드릴 수 있는 범위

경계 확인 전까지는 다음을 잠정 규칙으로 삼고, 이탈은 모두 기록합니다:

- Feature 하나는 자기 디렉터리 또는 Module을 소유하고, 이미 있는 Interface로만 공유합니다;
- 두 Feature가 공유하는 대상의 변경은 Shared File 변경이며 Project Map 역방향 Index에 기록합니다;
- Capability 결정은 그것을 처음 필요로 한 Feature에 속하며, 반복하지 않고 기록합니다.

## 이름 및 File 관례

`⟨확인 필요: 이 Project 자체의 관례⟩`
