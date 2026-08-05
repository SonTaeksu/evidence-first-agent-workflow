# C# Windows Forms Stack

## Supported baseline

| Item | Value |
|---|---|
| Language | C# |
| Target framework | .NET Framework 4.7.2 or later — TFM `net472`, `net48`, `net481` |
| UI | Windows Forms (`System.Windows.Forms`) |
| Project format | SDK-style `Microsoft.NET.Sdk` in the reference skeleton; legacy `.csproj` supported through capability detection |
| Build | MSBuild |
| Test | VSTest |
| Platform | Windows only |

The reference skeleton pins `net472` because it is the lowest baseline this profile supports. Per-monitor DPI awareness requires .NET Framework 4.7 or later and Windows 10 Creators Update or later.

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

## Commands

```bash
msbuild MinimalApp.csproj /t:Restore,Build /p:Configuration=Release
vstest.console.exe bin\Release\MinimalApp.Tests.dll
```

An SDK-style project targeting `net472` also builds with `dotnet build` and `dotnet test` when the .NET SDK and the .NET Framework targeting pack are installed. A legacy `.csproj` requires MSBuild. Record which route the project uses in the Project Map; do not assume both work.

## Known constraints

- Windows only. There is no cross-platform build or test route.
- The designer owns `*.Designer.cs` and rewrites it. Hand edits are lost.
- Form `.resx` files must be edited through the designer.
- `UseWindowsForms` belongs to the .NET Desktop SDK and applies to `net<n>.0-windows` targets. On `net472` the Windows Forms assemblies are referenced directly.
- There is no rendered document to inspect. Rendered-output evidence comes from the designer control tree, not from the running window, unless a UI automation harness is confirmed.
