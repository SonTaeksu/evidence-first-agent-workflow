# Stack Profile — DevExpress WPF (v24.2+)

DevExpress WPF controls inside a WPF application, v24.2 or later.

**Companion to [`../csharp-wpf`](../csharp-wpf).** Plain WPF and MVVM rules are
not repeated here and are not superseded here. `csharp-wpf` governs XAML
compilation, dependency properties, routed events, resource lookup, the
Dispatcher and binding failure. This document covers only the places where
DevExpress changes the answer. If a question is answerable without naming a
DevExpress type, it belongs to the other profile.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation — the .NET target, and
the DevExpress version resolved by the build, not the version someone installed⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

Structurally this is a WPF application, so `../csharp-wpf/STACK.md` describes the
layout. The additions worth knowing about:

- `App.xaml` / `App.xaml.cs` — where the DevExpress theme is applied, and
  therefore where the ordering constraint below lives.
- `*.xaml` views hosting DevExpress controls — a `GridControl` declares its
  `View` as a child element, so the behaviour of the screen is in that element
  and not on the control.
- The project or package file — DevExpress assemblies are versioned as a set and
  restored from a licensed feed, which makes this file both version-sensitive and
  a build prerequisite rather than a detail.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

A DevExpress build has one extra failure mode worth naming in that answer: the
restore. See `validation/validation-profile.md`.

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project. Where
an exact type or member name would be needed to act on one, it is marked rather
than recalled.

### `GridControl` delegates to its `View`

`GridControl` holds data and selection; it does not decide how rows are drawn or
edited. A view does — `TableView` and `CardView` are the two named here — and the
view is declared inside the grid. The consequence is practical rather than
theoretical: most of what a developer wants to configure is on the view, so a
setting looked for on the grid is usually simply absent, and an answer written
for one view type does not transfer to another even though both are "the grid".
Always establish the view type before applying any grid answer.
`⟨verification required: the view types this project uses and the members it
configures on them — from the project's XAML and from dxdocs⟩`

### `DXWindow` / `ThemedWindow` and theme loading order

A DevExpress theme applies to a window only if that window participates in
DevExpress theming; `DXWindow` and `ThemedWindow` are the window types that do.
A plain `Window` in the same application is not themed by the same mechanism, so
a mixed application looks inconsistent without anything failing.

Theme selection is order-dependent: the theme has to be established before the
first themed window is created, because a window resolves its appearance when it
is constructed. Setting it later is not an error and produces no message — the
already-created windows simply keep what they had.
`⟨verification required: the exact API this project uses to select the theme, and
the point in startup at which it runs — from App.xaml.cs and from dxdocs⟩`

### Theme assemblies are a deployment input

DevExpress themes ship in assemblies alongside `DevExpress.Xpf.Core` that
compiled code does not reference by name, because the theme is selected by value
at runtime. Nothing in the build therefore requires them to be present. An
application that omits them builds, links, starts and runs — with a fallback
appearance and no diagnostic. This is why "it looked right on my machine" is not
evidence for this stack: the developer machine has the full installation.
`⟨verification required: which theme assemblies this project's chosen themes
require, and evidence that they are present in the build output — from the
published output, not from the project file⟩`

### `DXBinding` / `DXCommand` are not `Binding`

DevExpress provides its own markup extensions that take an expression rather than
a property path. They are a different dialect, not shorthand: what is a valid
expression in one is not necessarily a valid path in the other, and the two
report failure in different places. Mixing dialects inside one view is legal and
is a maintenance trap, because the reader has to know which rules apply line by
line.
`⟨verification required: where a failed DevExpress binding expression is reported
in this project's configuration — established by deliberately breaking one and
observing, not by recall⟩`

### The DevExpress MVVM framework versus a third-party one

DevExpress ships an MVVM framework — `ViewModelBase` for a conventional
inheritance-based view model, and a POCO approach that produces an enhanced type
from a plain class at runtime. The POCO route has a consequence that surprises
people: the object in use is not an instance of the class as written, so
reflection, serialisation, equality by concrete type and pattern matching on the
declared class can all behave differently from what the source suggests.

A project that also references a third-party MVVM library then has two command
types, two notification base classes and two conventions, and code moves between
them by copy-paste. Which one governs is an owner decision, not a preference.
`⟨verification required: which MVVM framework this project uses, and whether both
are present — from the package references and from the view model base types⟩`

### `DevExpress.Xpf.Docking`

Docking replaces the window's layout with a managed one: panels, groups and
document hosts are owned by the docking layout rather than by the XAML tree the
way plain WPF panels are. The layout is serialisable, and applications commonly
save it per user and restore it at startup. That combination is the trap — a
layout change made in XAML is overwritten by a restored layout from an earlier
build, so the change appears not to have been made, and a panel removed from the
XAML can be resurrected by an old saved layout. There is no error in either case.
`⟨verification required: whether this project persists and restores a docking
layout, where it is stored, and what happens to a stored layout when the panel
set changes⟩`

### Version answers do not carry

DevExpress releases on its own cadence, independent of .NET. A control's members
and defaults are properties of the DevExpress version resolved by the build, not
of the .NET target. An answer found for another version frequently still
compiles, which is what makes it dangerous. The version in the project's own
restore output is the authority.
