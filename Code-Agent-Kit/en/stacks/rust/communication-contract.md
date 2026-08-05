# Communication Contract — Rust

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
