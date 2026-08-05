# C# Windows Forms Capability Detection

| Capability | Detection | Present 경로 | Absent 경로 | Unknown 규칙 |
|---|---|---|---|---|
| project-format | `<Project>`의 `Sdk` Attribute 대 Legacy `ToolsVersion` Project | SDK-style: MSBuild 또는 `dotnet build` | legacy: MSBuild만 | 모든 Build와 Test 명령 차단 |
| package-management | `PackageReference` Item 대 `packages.config` File | Detection된 방식 사용 | — | Package 변경 차단 |
| designer-generated-code | `InitializeComponent`를 담은 `*.Designer.cs` | Designer가 Layout 소유; Behaviour는 Partial Class에 | Code 안의 수기 Layout; 결정 기록 | Layout 편집 차단 |
| dpi-awareness | `App.config`의 `System.Windows.Forms.ApplicationConfigurationSection`과 Manifest의 `supportedOS` | 구성된 Mode 유지 | System-aware 기본값; Manifest DPI 설정 추가 금지 | Scaling과 Layout 작업 차단 |
| ui-automation | Test Project 안의 Automation Harness 참조 | Runtime Evidence에 사용 | Designer-tree Extraction만; Runtime은 사유와 함께 `PENDING` | Runtime 주장 차단 |
| data-access | Provider 참조, Connection String, Generated Data Set | Detection된 Provider 재사용 | Owner 결정 필요 | Data 변경 차단 |
| authentication-provider | Authentication 구성과 Middleware 상당 Code | 기존 Provider와 통합 | 없음 | 보안 변경 차단 |
| localization | Satellite `.resx` File과 Culture Folder | Detection된 Culture 생산 | Invariant Culture만 | Resource 변경 차단 |
| analyzer-policy | `TreatWarningsAsErrors`, Analyzer Package 참조, Rule Set | Detection된 정책 준수 | Owner 결정 필요 | 경고 억제 변경 차단 |

Feature가 사용하는 모든 Capability는 Project Map에 기록하고 Gate Analysis에서 반복해야 합니다. Detection은 File이 보여주는 것을 보고할 뿐, Owner의 의도 확인을 대체하지 않습니다.

## project-format이 첫 번째 분기인 이유

Build 명령은 사소한 부분이 아닙니다. `net472`을 대상으로 하는 SDK-style Project는 Targeting Pack이 설치되어 있으면 `dotnet build`로 Build되지만, Legacy `.csproj`는 그렇지 않습니다. 잘못된 명령을 쓰면 Code 결함처럼 보이는 실패가 발생하고 다음 변경이 엉뚱한 방향으로 향합니다.

## ui-automation이 Runtime 주장을 차단하는 이유

Windows Forms는 Rendered Document를 만들지 않습니다. Automation Harness가 확인되지 않으면 Runtime Behaviour를 관찰할 결정론적 방법이 없으며, 정직한 보고는 `PASS`가 아니라 사유가 기록된 `PENDING`입니다.
