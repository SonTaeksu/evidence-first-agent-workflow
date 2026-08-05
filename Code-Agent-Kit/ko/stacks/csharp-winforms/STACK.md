# C# Windows Forms Stack

## 지원 Baseline

| Item | Value |
|---|---|
| Language | C# |
| Target Framework | .NET Framework 4.7.2 이상 — TFM `net472`, `net48`, `net481` |
| UI | Windows Forms (`System.Windows.Forms`) |
| Project Format | Reference Skeleton에서는 SDK-style `Microsoft.NET.Sdk`; Legacy `.csproj`는 Capability Detection을 통해 지원 |
| Build | MSBuild |
| Test | VSTest |
| Platform | Windows 전용 |

Reference Skeleton은 이 Profile이 지원하는 가장 낮은 Baseline이기 때문에 `net472`을 고정합니다. Per-monitor DPI Awareness는 .NET Framework 4.7 이상과 Windows 10 Creators Update 이상을 요구합니다.

## Architecture

```text
skeletons/MinimalApp/
├─ MinimalApp.csproj      SDK-style, net472, WinExe
├─ App.config             runtime version and DPI awareness
├─ app.manifest           Windows 10 compatibility declaration
├─ Program.cs             entry point
├─ MainForm.cs            behaviour, hand-written
├─ MainForm.Designer.cs   layout, designer-generated
└─ Services/
   ├─ IGreetingService.cs the form's only route outside itself
   └─ GreetingService.cs  no UI thread affinity
```

## 명령

```bash
msbuild MinimalApp.csproj /t:Restore,Build /p:Configuration=Release
vstest.console.exe bin\Release\MinimalApp.Tests.dll
```

`net472`을 대상으로 하는 SDK-style Project는 .NET SDK와 .NET Framework Targeting Pack이 설치되어 있으면 `dotnet build`와 `dotnet test`로도 Build됩니다. Legacy `.csproj`는 MSBuild가 필요합니다. Project가 어느 경로를 쓰는지 Project Map에 기록하고, 둘 다 동작한다고 가정하지 않습니다.

## 알려진 제약

- Windows 전용입니다. Cross-platform Build나 Test 경로는 없습니다.
- Designer가 `*.Designer.cs`를 소유하고 다시 씁니다. 수기 편집은 사라집니다.
- Form `.resx` File은 반드시 Designer를 통해 편집해야 합니다.
- `UseWindowsForms`는 .NET Desktop SDK 소속이며 `net<n>.0-windows` Target에 적용됩니다. `net472`에서는 Windows Forms Assembly를 직접 참조합니다.
- 살펴볼 Rendered Document가 없습니다. UI Automation Harness가 확인되지 않는 한, Rendered Output Evidence는 실행 중인 창이 아니라 Designer Control Tree에서 나옵니다.
