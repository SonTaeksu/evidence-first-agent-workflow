# C# Windows Forms Artifact Contract

| Artifact | Required form | Source or skeleton | Generated ownership | Validation |
|---|---|---|---|---|
| Form behaviour | `MainForm.cs` partial class, hand-written | `skeletons/MinimalApp/MainForm.cs` | human | compile, unit tests |
| Form layout | `MainForm.Designer.cs` with `InitializeComponent` | `skeletons/MinimalApp/MainForm.Designer.cs` | **designer** | designer-tree extraction |
| Form resources | `*.resx` edited through the designer only | — | **designer** | compile |
| Entry point | `Program.cs` with `EnableVisualStyles` first | `skeletons/MinimalApp/Program.cs` | human | compile |
| Project file | real `.csproj`, format matching the detected capability | `skeletons/MinimalApp/MinimalApp.csproj` | human | restore, build |
| Runtime configuration | `App.config` with `supportedRuntime` and the DPI section | `skeletons/MinimalApp/App.config` | human | build, startup |
| Application manifest | `app.manifest` declaring Windows 10 compatibility | `skeletons/MinimalApp/app.manifest` | human | build |
| Service boundary | interface plus implementation, no UI types | `skeletons/MinimalApp/Services/` | human | unit tests |
| Tests | real test project source | — | human | test exit codes |

## Rules

- Layout and behaviour are separate files. The designer rewrites `*.Designer.cs`; anything hand-written there is lost on the next designer save.
- Do not replace a required Windows Forms artifact with a console program, a script, or a mock window that only prints. A form that does not exist as a `Form` subclass with a designer file is not an implementation of the screen.
- Do not create a second project file to work around a build failure. Fix the detected format.
- Do not add a manifest DPI setting. It overrides `App.config` and is no longer the recommended route.
- A control added to satisfy a specification must actually be added to a parent's `Controls` collection. A declared-but-unparented control is invisible and the designer-tree check reports it as absent.

## Empty visual blocks

A container with no children renders as blank space. The designer-tree check warns on it rather than blocking, because a container may legitimately be filled at runtime — but an empty container that the specification declared as populated is a rendered-output failure, and the required-control comparison catches that case as a failure.
