# C# Windows Forms Artifact Contract

| Artifact | 요구되는 형태 | Source 또는 Skeleton | Generated Ownership | Validation |
|---|---|---|---|---|
| Form Behaviour | `MainForm.cs` Partial Class, 수기 작성 | `skeletons/MinimalApp/MainForm.cs` | human | compile, unit tests |
| Form Layout | `InitializeComponent`가 있는 `MainForm.Designer.cs` | `skeletons/MinimalApp/MainForm.Designer.cs` | **designer** | designer-tree extraction |
| Form Resources | Designer를 통해서만 편집되는 `*.resx` | — | **designer** | compile |
| Entry Point | `EnableVisualStyles`가 먼저 오는 `Program.cs` | `skeletons/MinimalApp/Program.cs` | human | compile |
| Project File | Detection된 Capability와 일치하는 형식의 실제 `.csproj` | `skeletons/MinimalApp/MinimalApp.csproj` | human | restore, build |
| Runtime 구성 | `supportedRuntime`과 DPI Section이 있는 `App.config` | `skeletons/MinimalApp/App.config` | human | build, startup |
| Application Manifest | Windows 10 호환성을 선언하는 `app.manifest` | `skeletons/MinimalApp/app.manifest` | human | build |
| Service 경계 | UI Type이 없는 Interface와 구현 | `skeletons/MinimalApp/Services/` | human | unit tests |
| Tests | 실제 Test Project Source | — | human | test exit codes |

## 규칙

- Layout과 Behaviour는 별도 File입니다. Designer가 `*.Designer.cs`를 다시 쓰고, 그 안의 수기 작성 내용은 다음 Designer 저장 때 사라집니다.
- 필수 Windows Forms Artifact를 Console Program, Script, 출력만 하는 Mock Window로 대체하지 않습니다. Designer File을 가진 `Form` Subclass로 존재하지 않는 Form은 그 화면의 구현이 아닙니다.
- Build 실패를 우회하려고 두 번째 Project File을 만들지 않습니다. Detection된 형식을 고칩니다.
- Manifest DPI 설정을 추가하지 않습니다. `App.config`를 무시하며 더 이상 권장 경로가 아닙니다.
- Specification을 충족하기 위해 추가한 Control은 실제로 부모의 `Controls` Collection에 추가되어야 합니다. 선언만 되고 부모가 없는 Control은 보이지 않으며, Designer-tree 검사는 이를 absent로 보고합니다.

## 빈 Visual Block

자식이 없는 Container는 빈 공간으로 Rendering됩니다. Designer-tree 검사는 이를 차단하지 않고 경고하는데, Container는 Runtime에 정당하게 채워질 수 있기 때문입니다 — 하지만 Specification이 채워진다고 선언한 Container가 비어 있다면 이는 Rendered-output 실패이며, Required-control 비교가 이를 실패로 잡아냅니다.
