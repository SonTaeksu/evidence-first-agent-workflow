# Validation Profile — DevExpress for ASP.NET Core

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그것들이 취하는 형태:

- Restore: 이 Project의 Package Restore. **따뜻한 Cache가 아니라 Feed를 상대로** 합니다.
  이 Stack이 CI에서 겪는 첫 실패는 인증되지 않은 Private Feed이고, 차가운 Restore만 그것을
  찾아냅니다.
- Build와 Test: Project에 설정된 명령. Exit Code가 판정입니다.
- Lint, Analyzer, Type: 설정된 것은 무엇이든. 없으면 통과로 가정하지 않고 없다고
  보고합니다.
- Rendering: Component나 Report를 건드리는 모든 것에 대해, Build 통과는 판정이 아닙니다.
  아래를 참고합니다.

## 통과 기준

모든 경우에 **Exit Code**입니다. Exit Code가 0이 아닌데 성공 Message가 있으면 실패이며,
그 Message를 판정으로 삼는 것이 이 Kit이 막으려고 만들어진 바로 그 실수입니다.

## 여기서 초록색 Build가 다루지 못하는 것

평소보다 많고, 그래서 이 절이 존재합니다. 이 Stack에서 Build는 다음 상황에서도
만족합니다.

- 빠진 Reporting Service 등록 — Compile 시점에 아무것도 그것을 해결하지 않습니다;
- 제공되지 않는 Client-side Asset — 페이지는 어느 쪽이든 Compile됩니다;
- Report Storage 확장점의 구현되지 않은 Member — Build될 때가 아니라 도달했을 때
  던집니다;
- 더 이상 존재하지 않는 Field에 Binding된 Report — 그 Binding은 Schema에 대해 확인되지
  않습니다.

각각은 Runtime 발견 사항입니다. 이 중 무엇이든 건드리는 변경에는 Build가 아니라 실행에서
나온 Evidence가 필요합니다. 실제로 Rendering된 페이지나 Report, 그리고 기록된 그 실행입니다.
무엇이 인정되는지는 `artifact-contract.md`가 말합니다.

`⟨확인 필요: 이 Project가 그런 실행을 어떻게 만들고 기록하는지⟩`

## 오래 실행되는 Process

개발 Server나 Test 대상 Service는 `tools/run-managed-service/run_service.py`(또는 그
PowerShell 쌍둥이)를 통해 시작하고 중지합니다. 이 도구는 PID와 시작 시각으로 Process를
추적하고 그 Process Tree만 중지합니다.

이미지 이름으로 Process를 중지하지 않습니다. `Get-Process dotnet | Stop-Process`와
`pkill -f dotnet`은 Agent 자신이 의존하는 MCP Server와 Build, 그리고 사용자의 무관한 작업까지
함께 죽입니다.

## 결과 기록하기

명령, Exit Code, 머신의 .NET SDK Version, **그리고 해석된 DevExpress Package Version**.
여기서 마지막 것은 선택이 아닙니다. 둘은 따로 움직이고, 그것 없이는 결과를 나중에 어떤
것과도 비교할 수 없습니다.
