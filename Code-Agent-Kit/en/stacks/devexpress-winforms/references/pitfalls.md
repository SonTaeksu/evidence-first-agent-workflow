# Pitfalls — DevExpress WinForms

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

The plain Windows Forms pitfalls in
[`../../csharp-winforms/references/pitfalls.md`](../../csharp-winforms/references/pitfalls.md)
still apply. These are the ones DevExpress adds.

## Configuring the control instead of the view

`GridControl` holds the data; the view holds column layout, editing and
behaviour. A behaviour setting applied to the control compiles and has no effect,
so the symptom is "the change did nothing" rather than an error — and the usual
next step is to make the same wrong change harder.

## Assuming a grid has exactly one view

With master-detail or multiple levels, "the view" is ambiguous. A change applied
to the wrong view is applied successfully, to a surface the user is not looking
at.

## Positioning a child of a `LayoutControl` with coordinates

Position belongs to the layout item. Setting a child's coordinates is discarded
without an error, and the control appears where the layout put it — which reads
as the designer ignoring the edit.

## Adding a command to the form instead of the command component

A `RibbonControl` or a `BarManager` owns its items in its own collections. An item
created and left outside them exists in the code and never appears on screen.
Nothing fails; the command is simply not there.

## Hard-coding appearance under a skin

The skin decides colours and fonts. A control-level override either loses to the
skin or wins and produces the one control that does not match the application —
and which of the two happens is not obvious from reading the code.

## Applying application-wide appearance settings too late

Settings of this kind apply to controls created after them, so a call made after
a form has been constructed produces a partly themed application rather than an
exception. `⟨verification required: which settings this applies to in this
release, the exact members, and the call order the documentation requires⟩`

## Reasoning from the Windows Forms type with a similar name

A DevExpress control is not the `System.Windows.Forms` control it resembles.
`GridControl` is not `DataGridView`, and the members do not carry over. The good
case is a compile error; the bad case is a member that exists on both and means
something different.

## Consulting the unpinned endpoint on a pinned project

`dxdocs` answers from the latest release. On a v24.2 project it will describe
members added afterwards as though they were available. No error is produced at
lookup time — the cost arrives at compile time, or later.

## Treating a browser `405` as an outage

`https://api.devexpress.com/mcp/docs` speaks Streamable HTTP only. A browser GET
returns `405 Method Not Allowed`, and the documentation says that is the expected
response. It is what a working server returns to the wrong verb, so it is not a
health check and not a fault.

## Assuming the build agent has what the developer machine has

DevExpress is licensed. A build that passes locally and fails on an agent is a
licensing or feed configuration finding, not a code defect, and reading it as a
code defect sends the next change in the wrong direction.

## Hand-editing `licenses.licx` to make a build pass

It is a generated build input. Editing it changes a licensing artefact rather than
fixing the reason the licence is not present, and the original failure returns on
the next machine.
