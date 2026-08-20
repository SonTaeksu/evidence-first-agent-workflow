# Feature Model — DevExpress for ASP.NET Core

## What one feature is

`⟨verification required: the owner's definition of a feature boundary in this
codebase⟩`

The kit cannot derive this. A feature boundary that is guessed produces state
documents that describe nothing, and the Project Map stops being usable.

This stack has one boundary question the owner has to answer explicitly, because
guessing it wrong is expensive: **is a report definition part of a feature, or an
artefact with its own lifecycle?** A report that is edited by a business user
through the Report Designer at runtime is not source code and does not move with
a feature branch. A report that is compiled into the assembly is. Projects do
both, sometimes in the same repository.

`⟨verification required: which of the two this project does, and where the
boundary between them falls⟩`

## What a feature may touch

Until the boundary is confirmed, treat the following as the working rule and
record every departure from it:

- one feature owns its own directory or module, and shares only through an
  interface that already exists;
- a change to something two features share is a shared-file change and is
  recorded in the Project Map's reverse index;
- **application startup is shared**. Reporting registration, static-file
  configuration and asset delivery all live there, so a feature that adds a
  reporting host or a new component is touching shared ground and says so;
- **report storage is shared**. Changing how reports are addressed or stored
  affects every report, not the one being worked on;
- a capability decision belongs to the feature that first needs it, and is
  recorded, not repeated.

## Naming and file conventions

`⟨verification required: the project's own conventions, including how report
definitions are named and addressed by the storage implementation⟩`
