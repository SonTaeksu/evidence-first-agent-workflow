# Validation Profile — Rust

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그 명령이 갖는 형태:

- Build: `cargo build --locked`. `--locked`가 중요합니다. Lock File을 조용히 갱신하는 Build는 그 자체로 변경입니다.
- Test와 Lint: `cargo test --locked`, 그리고 설정되어 있다면 `cargo clippy`. Exit Code를 기록합니다.
- 선언된 MSRV와 나란히 `rustc --version`을 기록합니다.

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
