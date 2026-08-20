# Artifact Contract — Node.js

이 Stack이 무엇을 만들어 내는지, 그리고 그것이 만들어졌다는 Evidence가 무엇인지.

## Build 산출물

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact와 그 위치⟩`

## Evidence인 것

- Build 또는 Test의 **Exit Code**와 그것을 만든 명령. Exit Code가 0이 아닌데 Log에
  성공이라고 적힌 것은 Evidence가 아닙니다. 그것이 바로 이 Kit이 잡으려는
  실패 양상입니다.
- 명시한 경로에 실제로 존재하는 File. `check-stack-readiness`는 Evidence 경로를
  직접 확인하므로, 존재하지 않는 경로를 인용하면 없는 것으로 처리됩니다.

## Evidence가 아닌 것

- 명령 없는 자기 보고.
- Development Server의 출력. Development Mode에서 잘 돌아간다고 해서 Production
  Build가 된다는 근거가 되지 않습니다.
- 비교 대상이 없는 Screenshot.
