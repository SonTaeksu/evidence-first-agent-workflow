# Validation Profile — Node.js

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 명령이 갖는 형태는 다음과 같습니다.

- Install: Lock File을 존중하는 설치. Lock File이 바뀌면 그것은 보고 대상 변경입니다.
- Build(있다면)와 Test: 설정된 Script. Exit Code가 판정입니다.
- 그것을 실행한 Machine의 `node --version`을 기록합니다. Manifest의 범위는 Evidence가 아닙니다.

## 통과 기준

모든 경우에 **Exit Code**입니다. Exit이 0이 아닌데 성공 Message가 뜨는 것은 실패이며,
그 Message를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진 실수입니다.

## 장시간 실행 Process

Development Server나 Test 대상 Service는
`tools/run-managed-service/run_service.py`(또는 그 PowerShell 짝)로 시작하고 중지합니다.
이 Tool은 PID와 시작 시각으로 Process를 추적하며 그 Process Tree만 중지합니다.

Image 이름으로 Process를 중지하지 마십시오. `Get-Process node | Stop-Process`와
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 함께
죽입니다.

## 결과 기록

명령, Exit Code, 그리고 그 Machine의 Toolchain Version. Version이 없으면 나중에 나온
결과와 비교할 수 없습니다.
