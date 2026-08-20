# Artifact Contract — Next.js

이 Stack이 무엇을 만들어 내는지, 그리고 그것이 만들어졌다는 Evidence로 무엇을 인정하는지.

## Build 산출물

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact와 그 위치⟩`

## Evidence인 것

- 그것을 만들어 낸 명령과 함께 제시된 Build 또는 Test **Exit Code**. Exit Code가 0이 아닌데
  성공했다고 적힌 Log 한 줄은 Evidence가 아니라, 이 Kit이 잡으려고 존재하는 바로 그 실패
  방식입니다.
- 명시된 경로에 실제로 존재하는 File. `check-stack-readiness`가 Evidence 경로를 해석하므로,
  존재하지 않는 경로를 인용하면 없는 것으로 간주됩니다.

## Evidence가 아닌 것

- 명령이 없는 자기 보고.
- 개발 Server의 출력. 개발 Mode에서 성공했다고 Production Build가 동작한다는 뜻은 아닙니다.
- 비교 대상이 없는 Screenshot.
