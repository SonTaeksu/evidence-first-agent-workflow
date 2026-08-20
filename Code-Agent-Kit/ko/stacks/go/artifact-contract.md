# Artifact Contract — Go

이 Stack이 무엇을 만들어 내는지, 그리고 만들어졌다는 Evidence로 무엇을 인정하는지.

## Build 산출물

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact와 그 위치⟩`

## Evidence로 인정되는 것

- Build 또는 Test의 **exit code**와 그것을 만든 명령. exit code가 0이 아닌데
  성공이라고 적힌 Log 한 줄은 Evidence가 아닙니다. 그것이 바로 이 Kit이 잡으려는
  실패 방식입니다.
- 명시한 경로에 실제로 존재하는 File. `check-stack-readiness`가 Evidence 경로를
  해석하므로, 존재하지 않는 경로를 인용하면 없는 것으로 처리됩니다.

## Evidence가 아닌 것

- 명령 없는 자체 보고.
- Development Server의 출력. Development Mode에서 잘 돌아간다고 해서 Production
  Build가 된다는 뜻은 아닙니다.
- 비교 대상이 없는 Screenshot.
