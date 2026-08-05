# C# Windows Forms 검증된 Stack Profile

Baseline: .NET Framework 4.7.2 이상(`net472`+)의 C#, Windows Forms Desktop.

이 Profile은 `skeletons/MinimalApp/` 아래 포함된 Reference Skeleton에 대해 **바로 사용할 준비가 되어 있습니다**. 다른 Project에 도입할 때는 자신의 Project Format, Data Access, Authentication, Deployment, UI Evidence 경로를 다시 확인해야 합니다.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/csharp-winforms
```

## 이 Stack이 자체 Evidence 경로가 필요한 이유

Windows Forms에는 DOM이 없습니다. Kit의 Rendered Output Layer는 보통 Rendered Document를 읽지만, 여기서는 Application을 실행하지 않으면 읽을 것이 없습니다. Designer File이 결정론적 대체물입니다. Generated된 File이고, Form이 담고 있는 내용의 유일한 선언이며, Compile 없이 Parsing할 수 있습니다.

```text
source asset
→ screen specification (Gate §1)
→ designer file
→ extracted control tree
→ deterministic comparison
```

`tools/extract_designer_tree.py`와 `tools/check_designer_spec.py`가 이 비교를 구현합니다. [`references/ui-evidence-contract.md`](references/ui-evidence-contract.md)를 참조하십시오.

## Core Files

| File | 목적 |
|---|---|
| `STACK.md` | Baseline, Layout, 명령 |
| `STACK-INPUTS.md` | Reference가 확인하는 것과 도입 Project가 공급해야 하는 것 |
| `capability-detection.md` | Project Format, Designer Ownership, DPI, Automation, Data, Auth |
| `artifact-contract.md` | 어떤 File이 수기 작성이고 어떤 File이 Generated인지 |
| `communication-contract.md` | UI Thread 경계와 단일 Service 진입점 |
| `references/pitfalls.md` | 검증된 실패 양상 |
| `references/verified-facts.md` | 출처가 있는 Version 민감 Fact |
| `validation/validation-profile.md` | Build, Test, UI Gate |

## Reference Skeleton Fact

- `net472`을 대상으로 하는 SDK-style Project, `OutputType`은 `WinExe`
- `App.config`에서 Per-monitor v2 DPI Awareness를 구성, `app.manifest`에서 Windows 10 호환성을 선언
- Layout은 `MainForm.Designer.cs`, Behaviour는 `MainForm.cs`
- Form이 자기 자신 밖으로 나가는 유일한 경로인 Service Interface 하나
- Database 없음, Authentication Provider 없음, Invariant Culture를 넘어서는 Localization 없음

이는 Skeleton Fact이며, 도입 Project를 위한 정책이 아닙니다.

## 다른 Project에서 필요한 Owner 결정

- Project Format: SDK-style `net472` 또는 Legacy `.csproj`, 그리고 Package 관리 방식
- Data Access와 Connection 처리
- Authentication과 Authorization
- UI Automation Harness, 있다면 어떤 것
- Localization과 Satellite Assembly
- Deployment: ClickOnce, MSI, 또는 Copy
- Form, Connection String, Screenshot의 기밀 분류

확인되기 전까지 관련 Capability는 `unknown`으로 남고 의존하는 변경은 차단됩니다.
