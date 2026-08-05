# C# Windows Forms 검증된 Fact

추론으로 알아낼 수 없거나, Project 고유이거나, Version에 민감한 Fact만 여기에 둡니다.

| Fact | Version 또는 범위 | Evidence | 최종 검증 |
|---|---|---|---|
| .NET Framework 4.7.2의 TFM은 `net472`이다 | SDK-style Project | Microsoft Learn, *Overview of porting from .NET Framework to .NET* | 2026-08-02 |
| Legacy Project는 `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`를 쓴다 | legacy `.csproj` | same article | 2026-08-02 |
| `NET472_OR_GREATER`는 4.7.2 이상 Target의 Preprocessor Symbol이다 | SDK-style Project | Microsoft Learn, *Target frameworks in SDK-style projects* | 2026-08-02 |
| Enhanced High DPI 지원은 .NET Framework 4.7부터 Opt-in이다 | 4.7 이상, Windows 10 Creators Update 이상 | Microsoft Learn, *High DPI support in Windows Forms* | 2026-08-02 |
| `DpiAwareness`는 `PerMonitorV2` 또는 `false`를 받으며, 기본값은 `false`이다 | 4.7 이상 | Microsoft Learn, *Windows Forms Add Configuration Element* | 2026-08-02 |
| Windows 10 `supportedOS` 식별자는 `{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}`이다 | application manifest | Microsoft Learn, *High DPI support in Windows Forms* | 2026-08-02 |
| `DpiChanged`, `DpiChangedBeforeParent`, `DpiChangedAfterParent`는 4.7에서 추가되었다 | 4.7 이상 | same article | 2026-08-02 |
| `LogicalToDeviceUnits`, `ScaleBitmapLogicalToDevice`, `DeviceDpi`는 4.7에서 추가되었다 | 4.7 이상 | same article | 2026-08-02 |
| Control에서 `Invoke`, `BeginInvoke`, `EndInvoke`, `CreateGraphics`만 Thread-safe하다 | all versions | Microsoft Learn, `Control.InvokeRequired` | 2026-08-02 |
| `CreateGraphics`는 Handle이 존재한 이후에만 Thread-safe하다 | all versions | same page | 2026-08-02 |
| 4.7부터 TLS Stack은 운영체제 기본 Protocol을 쓴다 | 4.7 이상 | Microsoft Learn, *What's new in .NET Framework* | 2026-08-02 |
| 4.7.2는 `RSA.Create(RSAParameters)`와 `DSA.Create(DSAParameters)`를 추가했다 | 4.7.2 이상 | same article | 2026-08-02 |
| 4.7.2는 이전에는 Throw하던 `HttpClientHandler.CheckCertificateRevocationList`와 `SslProtocols`를 구현했다 | 4.7.2 이상 | same article | 2026-08-02 |
| 4.7.2는 `HttpCookie.SameSite`를 추가했다 | 4.7.2 이상, ASP.NET | same article | 2026-08-02 |
| 4.7.2는 `SqlAuthenticationMethod.ActiveDirectoryInteractive`를 추가했다 | 4.7.2 이상, SqlClient | same article | 2026-08-02 |

Reference Skeleton의 선택을 도입 Project의 정책으로 취급하지 않습니다. Version 민감 Fact는 의존하기 전에 `../mcp/source-routing.md`를 통해 다시 검증합니다.
