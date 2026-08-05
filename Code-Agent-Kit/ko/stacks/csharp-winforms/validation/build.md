# Build Validation

## 필수

Build 경로는 `project-format` Capability에 달려 있습니다. 무엇이든 실행하기 전에 확인합니다.

```bash
# SDK-style, TargetFramework net472
msbuild {PROJECT}.csproj /t:Restore,Build /p:Configuration=Release
# or, with the .NET SDK and the 4.7.2 targeting pack installed
dotnet build {PROJECT}.csproj -c Release

# Legacy .csproj, TargetFrameworkVersion v4.7.2
msbuild {PROJECT}.csproj /t:Build /p:Configuration=Release
```

Restore는 Package 관리 방식에 따라 다릅니다:

| Package 관리 | Restore |
|---|---|
| `PackageReference` | `msbuild /t:Restore` 또는 `dotnet restore` |
| `packages.config` | `nuget restore {SOLUTION}.sln` |

## Evidence

- 정확한 명령과 그 Exit Code;
- Log 끝부분의 Error와 Warning 개수;
- Log가 보고하는 Target Framework와 Project File의 비교;
- Warnings-as-errors Project의 경우, 통과시키기 위해 어떤 Warning도 억제하지 않았다는 확인.

## Build 통과가 증명하지 않는 것

Form이 무엇을 담고 있는지, 열리는지, Scaling되는지를 증명하지 않습니다. Rendered-output Layer는 따로 기록합니다 — [`ui.md`](ui.md)를 참조하십시오.

Warning을 억제하거나, Target Framework를 낮추거나, `TreatWarningsAsErrors`를 제거해서 통과시킨 Build는 Scope 변경이지 수정이 아닙니다. 그렇게 보고합니다.
