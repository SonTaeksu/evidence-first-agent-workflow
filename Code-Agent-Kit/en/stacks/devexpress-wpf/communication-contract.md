# Communication Contract — DevExpress WPF (v24.2+)

## Interfaces this stack exposes or consumes

`⟨verification required: the contracts this project owns, and which of them have
consumers outside this repository⟩`

Whether an external consumer exists decides whether a change may be made in
place or must be additive. Nobody can infer that from the code.

## Rules that hold regardless

- A change to a contract is a change to every consumer of it. Regenerating one
  side and not the other produces a runtime failure, not a build failure.
- A generated client is regenerated, never edited. Adaptation belongs in a
  hand-written wrapper, because the next regeneration silently discards edits.
- An error that a caller is expected to branch on must be part of the contract.
  An undeclared error arrives as something generic and cannot be handled.

## The contract this stack has that plain WPF does not

A **persisted docking layout is a serialised contract with the installed base**,
and it is the one people forget is a contract at all. It is written by one build
and read by a later one, so the set of panels is a versioned schema: removing a
panel, renaming its identity, or changing what identifies it in the layout are
all breaking changes to every layout already saved on a user's machine. The
failure is silent in both directions — a restored layout can hide a new panel, or
resurrect one that no longer exists.

`⟨verification required: whether this project persists a docking layout, what
identifies a panel in it, and what the application does with a layout it cannot
fully apply⟩`
