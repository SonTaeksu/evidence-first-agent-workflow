# C# Windows Forms Evidence Provenance

| Claim | Source Type | Source | Verification 방법 | Verified |
|---|---|---|---|---|
| SDK-style Project에서 .NET Framework 4.7.2의 TFM은 `net472`이다 | official docs | Microsoft Learn, *Overview of porting from .NET Framework to .NET* | documentation lookup | 2026-08-02 |
| Legacy Project는 대신 `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`를 쓴다 | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| `UseWindowsForms`는 .NET Desktop SDK 소속이며 `net<n>.0-windows` Target을 요구한다 | official docs | Microsoft Learn, *MSBuild reference for .NET Desktop SDK projects* | documentation lookup | 2026-08-02 |
| Enhanced High DPI 지원은 .NET Framework 4.7부터 Opt-in이다 | official docs | Microsoft Learn, *High DPI support in Windows Forms* | documentation lookup | 2026-08-02 |
| DPI Awareness는 `App.config`의 `DpiAwareness=PerMonitorV2`로 구성된다 | official docs | Microsoft Learn, *Windows Forms Add Configuration Element* | documentation lookup | 2026-08-02 |
| Manifest DPI 경로는 `App.config`를 무시하기 때문에 더 이상 권장되지 않는다 | official docs | Microsoft Learn, *High DPI support in Windows Forms* | documentation lookup | 2026-08-02 |
| DPI Key가 적용되기 전에 Manifest에 Windows 10 호환성이 선언되어야 한다 | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| `EnableVisualStyles`는 Entry Point의 첫 호출이어야 한다 | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| Control은 자신을 만든 Thread에 묶여 있으며, `Invoke`, `BeginInvoke`, `EndInvoke`, `CreateGraphics`만 Thread-safe하다 | official docs | Microsoft Learn, `Control.InvokeRequired` remarks | documentation lookup | 2026-08-02 |
| Handle이 아직 존재하지 않을 때 `InvokeRequired`는 `false`를 반환한다 | official docs | Microsoft Learn, same page | documentation lookup | 2026-08-02 |
| Cross-thread Control 접근은 `InvalidOperationException`을 발생시킨다 | official docs | Microsoft Learn, *How to handle cross-thread operations with controls* | documentation lookup | 2026-08-02 |
| Form `.resx`는 Designer를 통해 편집해야 하며, 그렇지 않으면 변경이 사라질 수 있다 | official docs | Microsoft Learn, *What is Windows Forms Designer?* | documentation lookup | 2026-08-02 |
| `.resx` Payload는 `BinaryFormatter`로 Serialize될 수 있으며, 이는 Deserialization 위험을 갖는다 | official docs | Microsoft Learn, same article | documentation lookup | 2026-08-02 |
| .NET Framework 4.7부터 TLS Stack은 운영체제에 위임하므로 Protocol Version을 하드코딩할 필요가 없다 | official docs | Microsoft Learn, *What's new in .NET Framework* | documentation lookup | 2026-08-02 |
| Reference Skeleton은 `net472`을 Target하고 Per-monitor v2 DPI를 구성한다 | installed artifact | `skeletons/MinimalApp/MinimalApp.csproj`, `App.config` | file inspection | 2026-08-02 |
| Reference Skeleton은 하나의 Container 계층에 다섯 개의 Control을 선언한다 | installed artifact | `skeletons/MinimalApp/MainForm.Designer.cs` | `tools/extract_designer_tree.py` | 2026-08-02 |

Version 민감 구현은 여전히 `mcp/source-routing.md`를 통한 현재 시점 조회가 필요합니다. 이 표의 행은 무엇이 언제 검증되었는지를 기록할 뿐, 영구적인 보증이 아닙니다.

검증되지 않은 주장은 `⟨verification required: what and how⟩`로 남습니다.
