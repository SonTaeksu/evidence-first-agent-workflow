# C# Windows Forms 검증된 Pitfall

| 잘못된 가정 | 검증된 규칙 | Evidence | 실패 단계 |
|---|---|---|---|
| Background Task가 Label을 직접 갱신해도 된다 | Control은 자신을 만든 Thread에 속하며, `Invoke`나 `BeginInvoke`로 Marshal해야 한다 | Microsoft Learn, `Control.InvokeRequired` | runtime |
| `InvokeRequired == false`이면 호출이 안전하다 | Handle이 아직 존재하지 않을 때도 `false`이다; Background Thread에서는 `IsHandleCreated`를 확인해야 한다 | Microsoft Learn, same page | runtime, intermittent |
| `CheckForIllegalCrossThreadCalls = false`로 설정하면 Exception이 고쳐진다 | 그것은 Detection을 제거할 뿐 경합 상태를 없애지 않는다 | Microsoft Learn, *How to handle cross-thread operations with controls* | runtime, later and worse |
| `*.Designer.cs`의 Layout 편집이 유지된다 | Designer가 File을 재생성하며 수기 편집은 사라진다 | `artifact-contract.md` | next designer save |
| Form `.resx`는 Resource Editor에서 편집할 수 있다 | Designer 밖에서 이루어진 변경은 사라질 수 있다 | Microsoft Learn, *What is Windows Forms Designer?* | build or next designer save |
| Manifest에 DPI 설정을 추가하는 것은 `App.config`와 동등하다 | Manifest가 `App.config`를 무시하며, Manifest 경로는 더 이상 권장되지 않는다 | Microsoft Learn, *High DPI support in Windows Forms* | rendered output |
| `DpiAwareness=PerMonitorV2`만으로 High DPI가 활성화된다 | Manifest에 Windows 10 호환성도 선언해야 하고, `EnableVisualStyles`가 먼저 실행되어야 한다 | Microsoft Learn, same article | rendered output |
| `<UseWindowsForms>true</UseWindowsForms>`가 `net472`에서 Windows Forms를 활성화한다 | 그 Property는 .NET Desktop SDK와 `net<n>.0-windows` Target 소속이다; `net472`에서는 Assembly를 직접 참조한다 | Microsoft Learn, *MSBuild reference for .NET Desktop SDK projects* | compile |
| `dotnet build`는 모든 .NET Framework Project에서 동작한다 | Targeting Pack이 설치된 SDK-style Project에서만 동작한다; Legacy `.csproj`는 MSBuild가 필요하다 | `capability-detection.md` | compile |
| Build 성공이 화면이 올바르다는 것을 증명한다 | Compile은 Form이 무엇을 담고 있는지 말해주지 않는다; Designer Control Tree를 Specification과 비교한다 | `ui-evidence-contract.md` | rendered output |
| 선언된 Control은 보이는 Control이다 | 부모의 `Controls` Collection에 추가되지 않은 Control은 보이지 않는다 | `artifact-contract.md` | rendered output |
| TLS Protocol Version은 Code에 고정해야 한다 | .NET Framework 4.7부터 Stack이 운영체제에 위임한다 | Microsoft Learn, *What's new in .NET Framework* | runtime, after an OS change |
| `BinaryFormatter`는 Resource와 Setting에 문제없다 | 안전하지 않으며 Deserialization에 신뢰할 수 없다 | Microsoft Learn, *What is Windows Forms Designer?* | runtime, security |
