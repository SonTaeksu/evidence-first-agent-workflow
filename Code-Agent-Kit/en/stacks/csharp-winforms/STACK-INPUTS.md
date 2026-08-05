# Stack Inputs

## Confirmed for the reference skeleton

The `Key` column joins each row to `STACK-READINESS.json`. The two files are
compared and a disagreement is reported — and because that report is a warning, and
a warning derives `provisional`, a stack declaring `ready` with disagreeing files
fails. Change both, together.

| Input | Key | Value or Path | Evidence | Status |
|---|---|---|---|---|
| Supported runtime and SDK versions | `runtime-sdk-versions` | .NET Framework 4.7.2 (`net472`) | `skeletons/MinimalApp/MinimalApp.csproj`, `skeletons/MinimalApp/App.config` | detected |
| Authoritative documentation | `authoritative-sources` | Microsoft Learn through source routing | `mcp/source-routing.md`, `evidence-provenance.md` | confirmed |
| Golden skeleton files | `golden-skeletons` | `skeletons/MinimalApp/` | `skeletons/README.md` | confirmed |
| Feature boundary and action model | `feature-model` | one form plus its service boundary | `feature-model.md` | confirmed |
| Naming and file conventions | `artifact-contract` | `MainForm.cs` behaviour, `MainForm.Designer.cs` layout | `artifact-contract.md` | confirmed |
| Communication and data contract | `communication-contract` | one service interface, UI thread marshalling rule | `communication-contract.md`, `skeletons/MinimalApp/Services/IGreetingService.cs` | confirmed |
| Capability branch rules | `capability-detection` | project format, designer ownership, DPI, automation | `capability-detection.md` | confirmed |
| Validation commands and failure signals | `validation-profile` | MSBuild, VSTest, designer-tree comparison | `validation/validation-profile.md` | confirmed |
| Known pitfalls | `known-pitfalls` | thread affinity, designer regeneration, DPI precedence | `references/pitfalls.md` | confirmed |
| Confidentiality classification | `confidentiality` | synthetic public skeleton, no organizational content | this file | confirmed |

## Inputs required when adopting this profile in another project

- **Project format.** SDK-style targeting `net472`, or legacy `.csproj` with `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`. This decides whether `dotnet build` is available at all.
- **Package management.** `PackageReference` or `packages.config`. The restore command differs.
- **Data access.** Provider, connection handling, transaction policy, and where connection strings live.
- **Authentication and authorization.** Windows integrated, forms-style, or none.
- **UI automation.** Whether an automation harness exists and may be used for runtime evidence. Without one, runtime behaviour stays `PENDING` with a stated reason.
- **Localization.** Satellite assemblies and the cultures that must be produced.
- **Deployment.** ClickOnce, installer, or copy, and the signing policy.
- **Analyzer policy.** Which warnings are errors, and which analyzer set is authoritative.
- **Confidentiality.** Whether form layouts, screenshots, connection strings, and business terms may leave the network.

Until confirmed, the related capability remains `unknown` and dependent changes are blocked.

## Automatically detected evidence

| Item | Detection method | Result in the reference skeleton |
|---|---|---|
| Project format | root element and `Sdk` attribute of the `.csproj` | SDK-style |
| Target framework | `TargetFramework` or `TargetFrameworkVersion` | `net472` |
| Windows Forms usage | reference to `System.Windows.Forms`, presence of `*.Designer.cs` | present |
| DPI configuration | `System.Windows.Forms.ApplicationConfigurationSection` in `App.config` | `PerMonitorV2` |
| Manifest compatibility | `supportedOS` entry in `app.manifest` | Windows 10 declared |
| Designer-generated files | `*.Designer.cs` containing `InitializeComponent` | present |
| Test projects | test project references and VSTest adapters | absent |
