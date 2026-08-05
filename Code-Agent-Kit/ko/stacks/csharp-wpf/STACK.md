# Stack Profile — WPF (.NET Framework 4.7.2+)

Desktop UI on WPF, targeting .NET Framework 4.7.2 or newer.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `App.xaml` / `App.xaml.cs` — application entry, `StartupUri`, application-scope resources.
- `*.xaml` + `*.xaml.cs` — a view and its code-behind; the partial class is completed by a generated `*.g.cs`.
- `ViewModels/` — if an MVVM pattern is in use; the capability table decides, not this document.
- `Properties/AssemblyInfo.cs`, `App.config` — framework-version-sensitive.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- XAML compiles to BAML and is embedded as a resource; a XAML error is a build error, not a runtime one.
- `x:Name` generates a field in the `*.g.cs` partial. Renaming in XAML without rebuilding leaves stale generated code.
- The UI thread must be STA. `[STAThread]` on `Main`, or the generated entry point provides it.
- Build requires the WPF MSBuild targets; a plain library SDK project will not compile XAML.
- **A failed data binding throws nothing.** It is written to the binding trace and the UI simply shows no value.
