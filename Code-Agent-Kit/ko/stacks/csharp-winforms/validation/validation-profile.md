# C# Windows Forms Validation Profile

## Verification 명령 (필수)

Completion(`prompts/GATE.md` §5)은 이것들이 통과해야 도달합니다. 자체 보고는 Exit Code를 대체하지 못합니다.

| Gate | 명령 (복사-붙여넣기) | 통과 기준 |
|---|---|---|
| Stack Readiness | `python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/csharp-winforms` | exit 0 |
| Restore | `msbuild {PROJECT}.csproj /t:Restore` | exit 0 |
| Build / Compile | `msbuild {PROJECT}.csproj /t:Build /p:Configuration=Release` | exit 0 **그리고** Log에 `error`나 `warning as error` 표식 없음 |
| Unit / Integration | `vstest.console.exe {OUTDIR}\{PROJECT}.Tests.dll` | exit 0, 대상 Test 전부 통과 |
| Rendered Output | `python stacks/csharp-winforms/tools/extract_designer_tree.py --designer {FORM}.Designer.cs --output {EVIDENCE}\tree.json` 다음 `python stacks/csharp-winforms/tools/check_designer_spec.py --tree {EVIDENCE}\tree.json --spec {EVIDENCE}\spec.json` | exit 0 |
| Tool Self-test | `python stacks/csharp-winforms/tools/self_test.py` | exit 0 |
| Scope / State | Git-scope와 Document-sync Tool | exit 0 |

SDK-style Project는 `dotnet build`와 `dotnet test`로 대체할 수 있습니다. Legacy `.csproj`는 그럴 수 없습니다. 선택하기 전에 `capability-detection.md`에서 `project-format`을 확인합니다.

경로는 `{PLACEHOLDERS}`로 유지합니다. 절대 SDK, Vendor, 사용자 경로를 Commit하지 않습니다 — Sanitization Gate가 차단합니다.

## Layer와 각 Layer가 증명하는 것

| Layer | Evidence | 실행할 수 없을 때 |
|---|---|---|
| Artifact / compile | MSBuild Exit Code와 Log | 결코 건너뛰지 않음 |
| Rendered output | Designer-tree 비교 | 결코 건너뛰지 않음; Tree는 항상 사용 가능 |
| Runtime behaviour | Capability가 확인될 때만 UI Automation | 사유를 기록한 `PENDING` |
| Accessibility / colour | Automation 또는 Screenshot Evidence | 사유를 기록한 `PENDING` |

실행할 수 없는 Layer는 사유와 함께 `PENDING`으로 남습니다. 결코 `PASS`로 기록하지 않습니다.

## 장기 실행 Process

수동 점검을 위해 Application을 실행하는 것은 장기 실행 Process입니다. Managed Runner를 통해 시작하고 그 Process만 중지합니다; 이미지 이름으로 종료하지 않습니다.

```bash
python tools/run-managed-service/run_service.py start --name app --cwd {dir} -- {OUTDIR}\{PROJECT}.exe
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name app
```

## Build Log에서 읽을 실패 신호

- `MSB3644` — 선언된 Framework의 Targeting Pack이 설치되지 않았습니다. Code가 결함이 아닙니다.
- Windows Forms Type에서 `CS0246` — `System.Windows.Forms` 참조가 없거나, Project Format이 잘못 Detection되었습니다.
- `MSB4803` — Legacy Project에서 `dotnet build`가 지원하지 않는 MSBuild Task. MSBuild를 사용합니다.
- Build는 성공했는데 Designer-tree 검사가 실패 — Compile은 화면 내용을 결코 증명하지 못했습니다.
