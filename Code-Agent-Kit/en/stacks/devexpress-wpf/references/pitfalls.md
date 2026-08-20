# Pitfalls — DevExpress WPF (v24.2+)

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

The plain-WPF list in `../../csharp-wpf/references/pitfalls.md` still applies —
silent binding failure, inherited `DataContext`, off-thread collection updates,
resource lookup order. This file adds only what DevExpress contributes.

## Configuring the grid instead of its view

`GridControl` holds data; a view — `TableView`, `CardView` — decides presentation
and editing. An answer found for one view type is often accepted by the other, or
by the grid, without doing what the reader expected. The symptom is a setting
that appears to have been applied and has no effect.

## The theme assembly that was never deployed

Theme assemblies are resolved at runtime by name, so no compiled reference points
at them and the build cannot notice their absence. The application starts, runs,
and looks wrong. This is invisible on a developer machine, which has the full
installation on disk.

## Theme applied after the first window exists

A window resolves its appearance when it is constructed. Setting the theme after
that point is not an error and produces no message; the windows already created
simply keep what they had. The result is an application that is themed except for
the one window that matters most — the first one.

## A plain `Window` in a themed application

Only windows that participate in DevExpress theming are themed by it. A plain
`Window` added later is not, and nothing complains. The application looks
half-finished rather than broken, which is why it ships.

## Mixed binding dialects in one view

DevExpress binding and command markup extensions take an expression; plain
`Binding` takes a property path. Both are valid in the same file. A reader — human
or agent — who applies one dialect's rules to the other's line gets a construct
that parses and does something else.
`⟨verification required: where a failed DevExpress binding expression is reported
in this project — established by breaking one deliberately and observing⟩`

## POCO view models are not the class you wrote

The DevExpress POCO approach produces an enhanced type from a plain class at
runtime. Reflection, serialisation, equality by concrete type and pattern
matching on the declared class can therefore all behave differently from what the
source file suggests, with no error at any point.

## Two MVVM frameworks in one solution

A project that references both the DevExpress MVVM framework and a third-party
one has two command types and two notification bases. Code copied between view
models compiles and then does not notify, or does not enable, for reasons that
are visible nowhere in the diff.

## A restored docking layout overwrites the XAML

Where a docking layout is saved per user and restored at startup, a layout change
made in XAML is silently replaced by an older stored layout, and a panel deleted
from the XAML can reappear. The developer's conclusion — "my change did not take"
— names the wrong cause, and the usual next step is to make the change again.

## A DevExpress answer from the wrong version

DevExpress versions its controls independently of .NET. A member from another
version frequently still exists, so the code compiles and the difference shows up
as behaviour. This is the single reason `mcp/source-routing.md` insists on
pinning the documentation server rather than querying the latest.
