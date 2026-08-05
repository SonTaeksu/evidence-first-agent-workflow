# C# Windows Forms Agent Rule

이 File은 Root `AGENTS.md`를 확장합니다.

- 다른 Project에 이 Profile을 도입하기 전에 Stack Readiness Validation을 실행합니다.
- Build 명령을 쓰기 전에 Project Format을 확인합니다. SDK-style `net472`은 MSBuild 또는 `dotnet build`로 Build되고, Legacy `.csproj`는 MSBuild로만 Build됩니다. 둘 다 된다고 가정하지 않습니다.
- Designer가 만들어낼 범위를 넘어서 `*.Designer.cs`의 Layout을 수기 편집하지 않습니다. 재생성되며 수기 편집은 사라집니다. Behaviour는 Partial Class File에 둡니다.
- Form `.resx`를 Designer 밖에서 편집하지 않습니다.
- 만들지 않은 Thread에서 Control을 건드리지 않습니다. `Control.Invoke` 또는 `BeginInvoke`로 Marshal하고, Background Thread에서 `InvokeRequired`가 `false`를 반환할 때 `IsHandleCreated`를 확인합니다.
- Service와 Data Code는 `ConfigureAwait(false)`를 씁니다. UI Thread로 돌아오는 것은 Form Code뿐입니다.
- DPI Awareness는 Manifest가 아니라 `App.config`에서 구성합니다. Manifest는 `App.config`를 무시하며 더 이상 권장 경로가 아닙니다.
- Entry Point의 첫 호출로 `Application.EnableVisualStyles()`를 유지합니다.
- 모든 Server, File, Database 호출을 확인된 Service 진입점을 통해 보냅니다. 두 번째 진입점을 추가하지 않습니다.
- Designer Control Tree에서 Rendered Output Evidence를 만듭니다. Build 성공은 Form이 무엇을 담고 있는지에 대한 Evidence가 아닙니다.
- UI Automation Capability가 확인되지 않으면 Runtime Behaviour를 사유를 명시한 채 `PENDING`으로 보고합니다. 통과했다고 주장하지 않습니다.

## Stack 금지 사항

- `net472` Target에서 `UseWindowsForms` 금지 — 이는 .NET Desktop SDK와 `net<n>.0-windows` Target 소속입니다;
- 새 Serialization 작업에 `BinaryFormatter` 금지, Resource Payload 포함;
- Capability가 `unknown`인 동안 Database, Authentication, Localization, Deployment 변경 금지;
- 하드코딩된 TLS Protocol Version 금지 — .NET Framework 4.7 이후는 운영체제에 위임합니다;
- Build나 실행 중인 Application을 중지해야 할 때 이미지 이름으로 일괄 Process 종료 금지.
