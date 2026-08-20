# Communication Contract — DevExpress for ASP.NET Core

## Interfaces this stack exposes or consumes

`⟨verification required: the contracts this project owns, and which of them have
consumers outside this repository⟩`

Whether an external consumer exists decides whether a change may be made in
place or must be additive. Nobody can infer that from the code.

Three contracts in this stack are easy to miss because they do not look like
APIs:

- **The report storage addressing scheme.** `ReportStorageWebExtension` is a
  contract between the designer and wherever reports live. The identifiers it
  hands out end up embedded in links, saved documents and user bookmarks, so
  changing how a report is addressed is a breaking change with no compiler in
  front of it. `⟨verification required: this project's scheme, and who else
  depends on it⟩`
- **The endpoints the viewer and designer are served through.** They are called
  by client-side code the project does not write. Moving or renaming one changes
  a contract with the browser. `⟨verification required: this project's routes⟩`
- **The data a report binds to.** A report definition names fields. Renaming a
  column or changing a result shape breaks the report at render time, not at
  build time, and the report is usually not in the same review as the schema
  change.

## Rules that hold regardless

- A change to a contract is a change to every consumer of it. Regenerating one
  side and not the other produces a runtime failure, not a build failure.
- A generated client is regenerated, never edited. Adaptation belongs in a
  hand-written wrapper, because the next regeneration silently discards edits.
- An error that a caller is expected to branch on must be part of the contract.
  An undeclared error arrives as something generic and cannot be handled.
- A contract that only a browser consumes is still a contract. Nothing in the
  build checks it, which makes writing it down more important rather than less.
