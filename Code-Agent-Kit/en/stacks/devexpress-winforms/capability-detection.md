# Capability Detection — DevExpress WinForms

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

The plain Windows Forms capabilities are detected as
[`../csharp-winforms/capability-detection.md`](../csharp-winforms/capability-detection.md)
describes: project format, package management, DPI, data access, authentication,
localization, analyzer policy. Those still decide the build command. The table
below is what DevExpress adds.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | the DevExpress package or assembly references in the project file, resolved through the lock or package files — not a range — cross-checked against what is installed on the machine that builds | answer within that release, and route lookups to the matching pinned endpoint | this is not a DevExpress project; use `../csharp-winforms` alone | block any version-sensitive DevExpress API use, and block choosing between the `dxdocs` and `dxdocs24_2` endpoints |
| grid-views | grid types constructed in the designer files, and which view type each grid's generated code creates | change behaviour on the view the designer created, not on the control | no grid; grid rules do not apply | block grid column, editing and behaviour changes |
| command-surface | ribbon versus bar-manager components in the designer files and the entry point | add commands where that component keeps them | the form uses the plain Windows Forms menu surface | block adding, moving or removing a command |
| layout-control | layout-control instances in the designer files | position through layout items | plain container layout; coordinates apply | block layout and positioning changes |
| skins-and-appearance | application-wide appearance calls in the entry point, and the skin assemblies the project references | keep the configured skin; do not override at control level | default appearance; record the decision | block appearance, colour and theme changes |
| license-file | `licenses.licx` in the project, whether it is tracked in source control, and whether the build agent has a licence | build the way the project already builds | find out how the agent compiles before claiming a reproducible build | block claiming the build reproduces on another machine |
| designer-generated-code | `*.Designer.cs` containing `InitializeComponent` | designer owns layout; behaviour goes in the partial class | hand-built layout in code; record the decision | block hand-editing generated layout |
| ui-automation | an automation harness reference in a test project | use it for runtime evidence | no runtime evidence route; runtime stays `PENDING` with a reason | block runtime behaviour claims |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.

## Why devexpress-version is the first branch

It decides which documentation server answers, and therefore which version every
subsequent answer describes. A member introduced after the project's release will
be documented as available by the unpinned endpoint, and the resulting code
compiles against nothing. Below v24.2 the endpoint cannot be pinned at all, which
is why this profile draws its boundary there.

## Why the control-versus-view split is a detection question

"Does this project use a grid" is not the useful question; "which view object
does this grid's designer code create" is. The behaviour settings live on the
view, so a change made without knowing the view type is a change made to the
wrong object — and that failure is silent, which is why it is a blocking
capability rather than a note.

## Why license-file blocks a reproducibility claim

The DevExpress assemblies are licensed, not part of the SDK. A build that succeeds
on a developer machine says nothing about the build agent, and a licensing failure
surfaces as a build error or a run-time dialog rather than as anything that looks
like a licensing problem. Until the route is confirmed, "the build passes" is a
claim about one machine.
