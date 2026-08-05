# C# Windows Forms Verified Facts

Only inference-resistant, project-specific, or version-sensitive facts belong here.

| Fact | Version or scope | Evidence | Last verified |
|---|---|---|---|
| The TFM for .NET Framework 4.7.2 is `net472` | SDK-style projects | Microsoft Learn, *Overview of porting from .NET Framework to .NET* | 2026-08-02 |
| Legacy projects use `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>` | legacy `.csproj` | same article | 2026-08-02 |
| `NET472_OR_GREATER` is the preprocessor symbol for a 4.7.2-or-later target | SDK-style projects | Microsoft Learn, *Target frameworks in SDK-style projects* | 2026-08-02 |
| Enhanced high DPI support is opt-in from .NET Framework 4.7 | 4.7 and later, Windows 10 Creators Update and later | Microsoft Learn, *High DPI support in Windows Forms* | 2026-08-02 |
| `DpiAwareness` accepts `PerMonitorV2` or `false`, default `false` | 4.7 and later | Microsoft Learn, *Windows Forms Add Configuration Element* | 2026-08-02 |
| The Windows 10 `supportedOS` identifier is `{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}` | application manifest | Microsoft Learn, *High DPI support in Windows Forms* | 2026-08-02 |
| `DpiChanged`, `DpiChangedBeforeParent`, and `DpiChangedAfterParent` were added in 4.7 | 4.7 and later | same article | 2026-08-02 |
| `LogicalToDeviceUnits`, `ScaleBitmapLogicalToDevice`, and `DeviceDpi` were added in 4.7 | 4.7 and later | same article | 2026-08-02 |
| Only `Invoke`, `BeginInvoke`, `EndInvoke`, and `CreateGraphics` are thread-safe on a control | all versions | Microsoft Learn, `Control.InvokeRequired` | 2026-08-02 |
| `CreateGraphics` is thread-safe only after the handle exists | all versions | same page | 2026-08-02 |
| From 4.7 the TLS stack uses the operating system default protocols | 4.7 and later | Microsoft Learn, *What's new in .NET Framework* | 2026-08-02 |
| 4.7.2 added `RSA.Create(RSAParameters)` and `DSA.Create(DSAParameters)` | 4.7.2 and later | same article | 2026-08-02 |
| 4.7.2 implemented `HttpClientHandler.CheckCertificateRevocationList` and `SslProtocols`, which threw before | 4.7.2 and later | same article | 2026-08-02 |
| 4.7.2 added `HttpCookie.SameSite` | 4.7.2 and later, ASP.NET | same article | 2026-08-02 |
| 4.7.2 added `SqlAuthenticationMethod.ActiveDirectoryInteractive` | 4.7.2 and later, SqlClient | same article | 2026-08-02 |

Do not treat the reference skeleton's choices as an adopted project's policy. Re-verify a version-sensitive fact through `../mcp/source-routing.md` before relying on it.
