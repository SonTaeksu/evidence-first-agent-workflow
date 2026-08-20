# Stack Profile — DevExpress WinForms

DevExpress controls on a Windows Forms desktop application, v24.2 or later.

## Relationship to `csharp-winforms`

This profile is a **companion** to [`../csharp-winforms`](../csharp-winforms/),
not a replacement. The plain Windows Forms rules are unchanged: the designer owns
`*.Designer.cs`, `.resx` is edited through the designer, controls belong to their
creating thread, and the project format decides whether `dotnet build` is
available at all. Nothing below repeals any of that. Everything below is what
DevExpress adds.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation — the .NET target, and the
DevExpress version from the package or assembly references rather than from a
supported range⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## DevExpress version

`⟨verification required: the DevExpress release this project actually references,
and whether the same release is installed on the machine that builds⟩`

This is the first branch, not a detail. It decides which documentation endpoint
answers — `dxdocs24_2` for a v24.2 project, `dxdocs` only when the project really
is on the latest release. See `mcp/source-routing.md`.

## Directory structure

The plain WinForms layout, unchanged: behaviour in the form's partial class,
layout in the designer file, resources in `.resx`.

`⟨verification required: this project's own conventions — where forms live,
whether a shared base form or a shared appearance module exists, and where the
application-wide startup configuration is performed⟩`

## Build commands

`⟨verification required: the project's own build command and its pass criterion,
plus how the DevExpress assemblies are made available to the build machine⟩`

The DevExpress assemblies are a licensed dependency rather than part of the .NET
SDK, so a build that works on a developer's machine and fails on an agent is a
normal outcome here, and it is a configuration finding rather than a code defect.

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project. Every
one of them is stated without a member name on purpose: the names are exactly what
must be looked up rather than recalled.

- **The control and the view are different objects.** A `GridControl` is the bound
  container — it holds the data source. A `GridView` is a view over it, and the
  view is where column layout, editing, sorting, grouping and behaviour live.
  Applying a behaviour setting to the control compiles and does nothing, which is
  the single most common way work in this stack is lost.
- **A grid may have more than one view.** `⟨verification required: whether this
  project uses master-detail or multiple view levels, and which view a given
  change is meant to affect⟩` "The view" is a question in that case, not a
  default.
- **The command surface is owned by a component, not by the form.** A
  `RibbonControl` or a `BarManager` owns its items in its own collections.
  Adding a command means adding it where that component keeps them; a command
  added anywhere else exists and is invisible.
- **Ribbon and `BarManager` are alternatives, not layers.** Which one a form uses
  is a project decision. `⟨verification required: which command surface this
  project uses, and whether the two are mixed anywhere⟩`
- **`LayoutControl` owns position.** Children are placed through layout items, so
  coordinates set on a child are discarded. There is no error; the control simply
  appears where the layout decided.
- **Appearance is decided by the skin, not by the control.** On `XtraForm` and the
  skinned controls, a hard-coded colour or font is an override of the theme, and
  it either has no effect or produces the one control that does not match the
  rest of the application.
- **Application-wide appearance settings are startup settings.** `WindowsFormsSettings`
  is where several of them live, and settings of this kind take effect only for
  controls created after they are applied. `⟨verification required: which settings
  this project applies, the exact members, and the call order the documentation
  requires⟩`
- **`DevExpress.Utils` is shared across controls.** Appearance and utility types
  from it are used by many controls at once, so a change there is a
  cross-control change and its blast radius is every screen that uses the type.
  `⟨verification required: which of these types this project actually uses⟩`
- **Designer-generated code is larger here, not smaller.** A DevExpress form
  generates substantially more `InitializeComponent` content than a plain form,
  and the designer still rewrites all of it. Hand edits are still lost.
- **Licensing is a build-time and run-time fact.** DevExpress is a commercial
  library; Windows Forms records component licences in `licenses.licx`, which is a
  build input rather than source code. `⟨verification required: whether this
  project has a licences file, whether it is under source control, and what the
  build agent needs in order to compile⟩`
