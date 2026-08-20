# Validation Profile — WPF (.NET Framework 4.7.2+)

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그 명령이 갖는 형태:

- Build: Project 자체의 Target Framework를 대상으로 하는 MSBuild. 판정은 Exit Code이며, Exit가 0이 아닌데 나오는 `Build succeeded` 줄은 판정이 아닙니다.
- Test: Project에 구성된 Runner. 명령과 Exit Code를 기록합니다.
- UI: 화면 명세를 Rendering된 창과 비교합니다. 비교할 대상이 없는 Screenshot은 Evidence가 아닙니다.

## 합격 기준

모든 경우에 **Exit Code**입니다. Exit가 0이 아닌데 성공 Message가 나오면 그것은
실패이고, 그 Message를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진
잘못입니다.

## Long-running Process

개발 Server나 Test 대상 Service는 `tools/run-managed-service/run_service.py`(또는
그 PowerShell 짝)로 시작하고 중지합니다. 이 도구는 PID와 시작 시각으로 Process를
추적하며 그 Process Tree만 중지합니다.

이미지 이름으로 Process를 중지하지 마십시오. `Get-Process node | Stop-Process`와
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 함께
죽입니다.

## 결과 기록하기

명령, Exit Code, 그리고 그 Machine의 Toolchain Version. Version이 없으면 나중에
어떤 결과와도 비교할 수 없습니다.
