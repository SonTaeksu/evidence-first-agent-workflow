# Validation Profile — Go

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 대체로 이런 모양입니다.

- Build: `go build ./...`. exit code가 판정입니다.
- Vet과 Test: `go vet ./...`과 `go test ./...`. 두 exit code를 모두 기록합니다.
- Validation 장비의 `go version`을 `go` Directive와 함께 기록합니다.

## 통과 기준

언제나 **exit code**입니다. exit가 0이 아닌데 성공 메시지가 나왔다면 그것은
실패이고, 메시지를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진
실수입니다.

## 오래 도는 Process

Development Server나 Test 대상 Service는
`tools/run-managed-service/run_service.py`(또는 같은 역할의 PowerShell Script)로
시작하고 멈춥니다. 이 Tool은 PID와 시작 시각으로 Process를 추적해 그 Process Tree만
멈춥니다.

Image 이름으로 Process를 멈추지 마십시오. `Get-Process node | Stop-Process`와
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 함께
죽입니다.

## 결과 기록하기

명령, exit code, 그리고 그 장비의 Toolchain Version. Version이 없으면 그 결과는
나중에 어떤 것과도 비교할 수 없습니다.
