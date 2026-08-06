# Validation Profile — Vue.js

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 명령이 취하는 형태:

- Install: Lock File을 존중하는 Project의 Install. Lock File을 바꾸는 Resolution은 변경이며 보고합니다.
- Build와 Test: 설정된 Package Script. Exit Code가 판정입니다.
- Lint와 Type: 설정된 것을 실행합니다. 없으면 통과로 간주하지 않고 없다고 보고합니다.

## 통과 기준

언제나 **Exit Code**입니다. Exit Code가 0이 아닌데 성공 Message가 나오면 그것은 실패이며, Message를
판정으로 받아들이는 것이 이 Kit이 막으려고 만들어진 실수입니다.

## 장시간 실행 Process

개발 Server나 Test 대상 Service는 `tools/run-managed-service/run_service.py`(또는 PowerShell 짝)로
시작하고 중지합니다. PID와 시작 시각으로 Process를 추적해 그 Process Tree만 중지합니다.

Image 이름으로 Process를 중지하지 않습니다. `Get-Process node | Stop-Process`와 `pkill -f node`는
Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 죽입니다.

## 결과 기록

명령, Exit Code, 장비의 Toolchain Version. Version이 없으면 그 결과를 나중 것과 비교할 수 없습니다.
