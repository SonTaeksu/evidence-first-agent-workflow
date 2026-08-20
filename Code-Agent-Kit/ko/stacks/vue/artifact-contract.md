# Artifact Contract — Vue.js

이 Stack이 무엇을 만들고, 무엇이 그것을 만들었다는 Evidence인지 정합니다.

## Build 산출물

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact와 그 위치⟩`

## Evidence인 것

- Build 또는 Test의 **Exit Code**와 그것을 만든 명령. Exit Code가 0이 아닌데 성공이라고 적힌 Log
  한 줄은 Evidence가 아닙니다. 이 Kit이 잡으려고 존재하는 실패 양상 그 자체입니다.
- 명시된 경로에 실재하는 File. `check-stack-readiness`가 Evidence 경로를 확인하므로, 존재하지 않는
  경로를 인용하면 absent로 처리됩니다.

## Evidence가 아닌 것

- 명령 없는 자기 보고.
- 개발 Server 출력. Development Mode 성공은 Production Build가 동작한다는 근거가 아닙니다.
- 비교 대상 없는 Screenshot.
