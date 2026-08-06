# Validation Profile — Next.js

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그 명령들이 갖는 형태는 다음과 같습니다.

- Install: Lock File을 존중하는 설치. Lock File이 바뀌었다면 그것은 보고해야 할 변경입니다.
- Build: 개발 Server가 아니라 Production Build. 개발에서만 성공한 것은 Evidence가 아닙니다.
- Test, Lint, Type: 구성되어 있는 것을 실행합니다. 판정은 Exit Code입니다.

## 통과 기준

언제나 **Exit Code**입니다. Exit Code가 0이 아닌데 성공 Message가 보이는 것은 실패이며,
그 Message를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진 실수입니다.

## 장기 실행 Process

개발 Server나 Test 대상 Service는 `tools/run-managed-service/run_service.py`(또는 그
PowerShell 짝)를 통해 시작하고 중지합니다. 이 Tool은 PID와 시작 시각으로 Process를
추적하며 그 Process Tree만 중지합니다.

이미지 이름으로 Process를 중지하지 않습니다. `Get-Process node | Stop-Process`나
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 죽입니다.

## 결과 기록

명령, Exit Code, 그리고 그 Machine의 Toolchain Version. Version이 없으면 이 결과를 나중의
어떤 것과도 비교할 수 없습니다.
