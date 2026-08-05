# C# Windows Forms Capability Detection

| Capability | Detection | Present path | Absent path | Unknown rule |
|---|---|---|---|---|
| project-format | `Sdk` attribute on `<Project>` versus a legacy `ToolsVersion` project | SDK-style: MSBuild or `dotnet build` | legacy: MSBuild only | block every build and test command |
| package-management | `PackageReference` items versus a `packages.config` file | use the detected mechanism | — | block package changes |
| designer-generated-code | `*.Designer.cs` containing `InitializeComponent` | designer owns layout; behaviour goes in the partial class | hand-built layout in code; record the decision | block layout edits |
| dpi-awareness | `System.Windows.Forms.ApplicationConfigurationSection` in `App.config` and `supportedOS` in the manifest | keep the configured mode | system-aware default; do not add manifest DPI settings | block scaling and layout work |
| ui-automation | automation harness reference in a test project | use it for runtime evidence | designer-tree extraction only; runtime stays `PENDING` with a reason | block runtime claims |
| data-access | provider references, connection strings, generated data sets | reuse the detected provider | owner decision required | block data changes |
| authentication-provider | authentication configuration and middleware-equivalent code | integrate the existing provider | none | block security changes |
| localization | satellite `.resx` files and culture folders | produce the detected cultures | invariant culture only | block resource changes |
| analyzer-policy | `TreatWarningsAsErrors`, analyzer package references, rule sets | honour the detected policy | owner decision required | block warning-suppression changes |

Every capability used by a feature must be recorded in Project Map and repeated in Gate Analysis. Detection reports what the files show; it does not replace owner confirmation of intent.

## Why project-format is the first branch

The build command is not a detail. An SDK-style project targeting `net472` builds with `dotnet build` when the targeting pack is installed; a legacy `.csproj` does not. Writing the wrong command produces a failure that looks like a code defect and sends the next change in the wrong direction.

## Why ui-automation blocks runtime claims

Windows Forms produces no rendered document. Without a confirmed automation harness there is no deterministic way to observe runtime behaviour, and the honest report is `PENDING` with the reason recorded — not `PASS`.
