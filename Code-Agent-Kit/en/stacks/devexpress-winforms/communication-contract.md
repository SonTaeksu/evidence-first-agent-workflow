# Communication Contract — DevExpress WinForms

## Interfaces this stack exposes or consumes

`⟨verification required: the contracts this project owns, and which of them have
consumers outside this repository⟩`

Whether an external consumer exists decides whether a change may be made in place
or must be additive. Nobody can infer that from the code.

## The UI thread boundary is inherited, not restated

[`../csharp-winforms/communication-contract.md`](../csharp-winforms/communication-contract.md)
holds the rule and the reasoning: controls belong to the thread that created them,
background work marshals through `Invoke` or `BeginInvoke`, and `InvokeRequired`
returning `false` is not by itself permission. A DevExpress control is a Windows
Forms control, so none of that changes and none of it is repeated here.

## What DevExpress adds

- **Data reaches the screen through the control; behaviour is configured on the
  view.** Binding a data source and configuring how it is displayed are two
  operations against two objects. A boundary that hands a form a data source has
  not thereby configured anything about how it appears.
- **The service returns data, never a control, a view or a form.** Formatting for
  display happens on the form side. A service that returns a configured grid view
  has moved the UI into the service layer, and the next screen that needs the same
  data inherits the first screen's presentation.
- **A shared appearance or skin decision is a contract.** It is consumed by every
  screen, so changing it is a change to all of them and the change lists them.
- **Error contract**: the service raises a typed exception or returns a result
  value; the form decides what the user sees. A swallowed exception that leaves a
  grid empty is indistinguishable from an empty result, which is the version of
  this defect that survives longest.

## Rules that hold regardless

- A change to a contract is a change to every consumer of it. Regenerating one
  side and not the other produces a runtime failure, not a build failure.
- A generated client is regenerated, never edited. Adaptation belongs in a
  hand-written wrapper, because the next regeneration silently discards edits.
- An error that a caller is expected to branch on must be part of the contract.
  An undeclared error arrives as something generic and cannot be handled.
