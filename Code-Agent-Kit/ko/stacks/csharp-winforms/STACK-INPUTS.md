# Stack Inputs

## Reference Skeleton에서 확인된 사항

| Input | Key | Value or Path | Evidence | Status |
|---|---|---|---|---|
| 지원되는 Runtime 및 SDK Version | `runtime-sdk-versions` | .NET Framework 4.7.2 (`net472`) | `skeletons/MinimalApp/MinimalApp.csproj`, `skeletons/MinimalApp/App.config` | detected |
| 공식 문서 | `authoritative-sources` | Source Routing을 통한 Microsoft Learn | `mcp/source-routing.md`, `evidence-provenance.md` | confirmed |
| Golden Skeleton File | `golden-skeletons` | `skeletons/MinimalApp/` | `skeletons/README.md` | confirmed |
| Feature 경계와 Action Model | `feature-model` | Form 하나와 그 Service 경계 | `feature-model.md` | confirmed |
| 명명 및 File 관례 | `artifact-contract` | Behaviour는 `MainForm.cs`, Layout은 `MainForm.Designer.cs` | `artifact-contract.md` | confirmed |
| Communication 및 Data Contract | `communication-contract` | Service Interface 하나, UI Thread Marshalling 규칙 | `communication-contract.md`, `skeletons/MinimalApp/Services/IGreetingService.cs` | confirmed |
| Capability 분기 규칙 | `capability-detection` | Project Format, Designer Ownership, DPI, Automation | `capability-detection.md` | confirmed |
| Validation 명령과 실패 신호 | `validation-profile` | MSBuild, VSTest, Designer-tree 비교 | `validation/validation-profile.md` | confirmed |
| 알려진 Pitfall | `known-pitfalls` | Thread Affinity, Designer 재생성, DPI 우선순위 | `references/pitfalls.md` | confirmed |
| 기밀 분류 | `confidentiality` | 조직 내용 없는 합성 공개 Skeleton | this file | confirmed |

## 다른 Project에 이 Profile을 도입할 때 필요한 Input

- **Project Format.** `net472`을 대상으로 하는 SDK-style, 또는 `<TargetFrameworkVersion>v4.7.2</TargetFrameworkVersion>`을 쓰는 Legacy `.csproj`. 이것이 `dotnet build` 사용 가능 여부 자체를 결정합니다.
- **Package 관리.** `PackageReference` 또는 `packages.config`. Restore 명령이 다릅니다.
- **Data Access.** Provider, Connection 처리, Transaction 정책, Connection String이 있는 위치.
- **Authentication과 Authorization.** Windows Integrated, Forms-style, 또는 없음.
- **UI Automation.** Automation Harness가 존재하고 Runtime Evidence에 쓸 수 있는지 여부. 없으면 Runtime Behaviour는 사유를 명시한 채 `PENDING`으로 남습니다.
- **Localization.** Satellite Assembly와 생산해야 하는 Culture.
- **Deployment.** ClickOnce, Installer, 또는 Copy, 그리고 서명 정책.
- **Analyzer 정책.** 어떤 경고가 Error로 처리되는지, 어떤 Analyzer Set이 권위 있는지.
- **기밀성.** Form Layout, Screenshot, Connection String, 업무 용어가 Network를 벗어날 수 있는지.

확인되기 전까지 관련 Capability는 `unknown`으로 남고 의존하는 변경은 차단됩니다.

## 자동으로 Detection된 Evidence

| Item | Key | Detection 방법 | Reference Skeleton에서의 결과 |
|---|---|---|---|
| Project Format |  | `.csproj`의 Root Element와 `Sdk` Attribute | SDK-style |
| Target Framework |  | `TargetFramework` 또는 `TargetFrameworkVersion` | `net472` |
| Windows Forms 사용 |  | `System.Windows.Forms` 참조, `*.Designer.cs` 존재 | present |
| DPI 구성 |  | `App.config`의 `System.Windows.Forms.ApplicationConfigurationSection` | `PerMonitorV2` |
| Manifest 호환성 |  | `app.manifest`의 `supportedOS` Entry | Windows 10 선언됨 |
| Designer-generated File |  | `InitializeComponent`를 담은 `*.Designer.cs` | present |
| Test Project |  | Test Project 참조와 VSTest Adapter | absent |
