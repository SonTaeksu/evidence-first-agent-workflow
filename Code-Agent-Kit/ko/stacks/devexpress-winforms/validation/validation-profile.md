# Validation Profile — DevExpress WinForms

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그 명령들이 갖는 형태는 다음과 같습니다.

- **Restore.** DevExpress Assembly를 쓸 수 있게 만드는 것이면 무엇이든 — Package Feed, 설치된 제품, 또는 둘 다. `⟨확인 필요: 그중 어느 것인지, 그리고 Build Agent에 무엇이 필요한지⟩` Lock File을 바꾸는 Restore는 변경이며 반드시 보고해야 합니다.
- **Build.** Project의 Format이 허용하는 명령입니다. `../../csharp-winforms/capability-detection.md`를 참고합니다. SDK-style Project와 Legacy Project는 같은 방식으로 Build되지 않기 때문입니다. 판정은 Exit Code입니다.
- **Test.** 구성된 Runner입니다. 없으면 통과로 가정하지 않고 없다고 보고합니다.
- **Lint 및 Analyzer.** 구성되어 있는 것을 실행합니다.

## 통과 기준

언제나 **Exit Code**입니다. Exit Code가 0이 아닌데 성공 Message가 보이는 것은 실패이며,
그 Message를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진 실수입니다.

## 어느 Machine이 실행했는가

기록합니다. 대부분의 Stack에서 이것은 사소한 배려지만 여기서는 결정적입니다. DevExpress
License는 Source가 아니라 Machine의 속성이기 때문입니다. Machine이 명시되지 않은 "Build가
통과한다"는 누군가의 Laptop에 관한 주장입니다.

## Rendered Output Evidence

Windows Forms는 Rendering된 문서를 만들지 않고, DevExpress를 더해도 생기지 않습니다.
Evidence 경로는
[`../../csharp-winforms/references/ui-evidence-contract.md`](../../csharp-winforms/references/ui-evidence-contract.md)가
서술하는 그대로 Designer Control Tree입니다.

단서가 하나 있고, 아직 해결되지 않았습니다. 그 경로는 `*.Designer.cs`를 Parsing해 Control
Tree를 추출하는데, DevExpress Designer 출력은 Control과 그 포함 관계를 순수 Windows Forms와
다르게 선언합니다.
`⟨확인 필요: csharp-winforms/tools/extract_designer_tree.py가 DevExpress Designer File을
올바르게 Parsing하는지 — 실제 File에 대해 실행하고 추출된 Tree를 그 File과 비교할 것⟩`
그 답이 나오기 전까지, DevExpress Form에 그 Tool을 돌려 얻은 Rendered Output 결과는
통과가 아니라 미확인으로 취급합니다.

## Layer와 각각이 증명하는 것

| Layer | Evidence | 실행할 수 없을 때 |
|---|---|---|
| Artifact / Compile | Machine을 명시한 Build Exit Code와 Log | 절대 건너뛰지 않음 |
| Rendered Output | 위 단서가 적용되는 Designer Control Tree | 사유를 기록한 `PENDING` |
| Runtime Behaviour | Capability가 확인된 경우에만 UI Automation | 사유를 기록한 `PENDING` |
| Accessibility / 색상 | Automation 또는 Screenshot Evidence | 사유를 기록한 `PENDING` |

실행할 수 없는 Layer는 사유와 함께 `PENDING`으로 남습니다. 절대 `PASS`로 기록하지 않습니다.

## 장기 실행 Process

수동 확인을 위해 Application을 띄우는 것은 장기 실행 Process입니다.
`tools/run-managed-service/run_service.py`(또는 그 PowerShell 짝)를 통해 시작하고
중지합니다. 이 Tool은 PID와 시작 시각으로 Process를 추적하며 그 Process Tree만 중지합니다.

이미지 이름으로 Process를 중지하지 않습니다. `Get-Process node | Stop-Process`나
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 죽입니다.

## 결과 기록

명령, Exit Code, Machine, 그리고 두 Version — .NET Target과 DevExpress Release. 그것들이
없으면 이 결과를 나중의 어떤 것과도 비교할 수 없습니다.
