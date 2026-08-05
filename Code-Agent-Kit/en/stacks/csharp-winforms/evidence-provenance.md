# C# Windows Forms Evidence Provenance

| Claim | Source type | Source | Verification method | Verified |
|---|---|---|---|---|
| The TFM for .NET Framework 4.7.2 in an SDK-style project is `net472` | official docs | Microsoft Learn, *Overview of porting from .NET Framework to .NET* | documentation lookup | 2026-08-02 |
| A legacy project uses `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>` instead | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| `UseWindowsForms` belongs to the .NET Desktop SDK and requires a `net<n>.0-windows` target | official docs | Microsoft Learn, *MSBuild reference for .NET Desktop SDK projects* | documentation lookup | 2026-08-02 |
| Enhanced high DPI support is opt-in from .NET Framework 4.7 | official docs | Microsoft Learn, *High DPI support in Windows Forms* | documentation lookup | 2026-08-02 |
| DPI awareness is configured by `DpiAwareness=PerMonitorV2` in `App.config` | official docs | Microsoft Learn, *Windows Forms Add Configuration Element* | documentation lookup | 2026-08-02 |
| The manifest DPI route is no longer recommended because it overrides `App.config` | official docs | Microsoft Learn, *High DPI support in Windows Forms* | documentation lookup | 2026-08-02 |
| Windows 10 compatibility must be declared in the manifest before the DPI key applies | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| `EnableVisualStyles` must be the first call in the entry point | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| Controls are bound to their creating thread; only `Invoke`, `BeginInvoke`, `EndInvoke`, and `CreateGraphics` are thread-safe | official docs | Microsoft Learn, `Control.InvokeRequired` remarks | documentation lookup | 2026-08-02 |
| `InvokeRequired` returns `false` when the handle does not exist yet | official docs | Microsoft Learn, same page | documentation lookup | 2026-08-02 |
| A cross-thread control access raises `InvalidOperationException` | official docs | Microsoft Learn, *How to handle cross-thread operations with controls* | documentation lookup | 2026-08-02 |
| A form `.resx` must be edited through the designer or changes can be lost | official docs | Microsoft Learn, *What is Windows Forms Designer?* | documentation lookup | 2026-08-02 |
| `.resx` payloads may be serialized with `BinaryFormatter`, which presents deserialization risk | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| From .NET Framework 4.7 the TLS stack defers to the operating system, so the protocol version need not be hard-coded | official docs | Microsoft Learn, *What's new in .NET Framework* | documentation lookup | 2026-08-02 |
| The reference skeleton targets `net472` and configures per-monitor v2 DPI | installed artifact | `skeletons/MinimalApp/MinimalApp.csproj`, `App.config` | file inspection | 2026-08-02 |
| The reference skeleton declares five controls in one container hierarchy | installed artifact | `skeletons/MinimalApp/MainForm.Designer.cs` | `tools/extract_designer_tree.py` | 2026-08-02 |

Version-sensitive implementation still requires a current lookup through `mcp/source-routing.md`. A row in this table records what was verified and when, not a permanent guarantee.

Unverified claims remain `⟨verification required: what and how⟩`.
