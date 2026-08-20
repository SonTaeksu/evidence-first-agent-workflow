# Stack Profile — WPF (.NET Framework 4.7.2+)

WPF 위에서 동작하는 Desktop UI이며 .NET Framework 4.7.2 이상을 Target합니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

- `App.xaml` / `App.xaml.cs` — Application 진입점, `StartupUri`, Application 범위의 Resource.
- `*.xaml` + `*.xaml.cs` — View와 그 Code-behind. Partial Class는 생성된 `*.g.cs`가 완성합니다.
- `ViewModels/` — MVVM Pattern을 쓰는 경우에 존재합니다. 이 문서가 아니라 Capability 표가 판단합니다.
- `Properties/AssemblyInfo.cs`, `App.config` — Framework Version에 민감합니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다.

- XAML은 BAML로 Compile되어 Resource로 포함됩니다. XAML 오류는 Runtime 오류가 아니라 Build 오류입니다.
- `x:Name`은 `*.g.cs` Partial에 Field를 생성합니다. Rebuild 없이 XAML에서 이름만 바꾸면 낡은 생성 Code가 그대로 남습니다.
- UI Thread는 STA여야 합니다. `Main`에 `[STAThread]`를 붙이거나, 생성된 진입점이 그것을 제공합니다.
- Build에는 WPF MSBuild Target이 필요합니다. 평범한 Library SDK Project는 XAML을 Compile하지 못합니다.
- **Data Binding 실패는 아무것도 던지지 않습니다.** Binding Trace에 기록될 뿐이고, UI에는 값이 그냥 나타나지 않습니다.
