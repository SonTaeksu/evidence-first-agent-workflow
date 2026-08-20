# Feature Model — DevExpress WPF (v24.2+)

## What one feature is

`⟨verification required: the owner's definition of a feature boundary in this
codebase⟩`

The kit cannot derive this. A feature boundary that is guessed produces state
documents that describe nothing, and the Project Map stops being usable.

## What a feature may touch

Until the boundary is confirmed, treat the following as the working rule and
record every departure from it:

- one feature owns its own directory or module, and shares only through an
  interface that already exists;
- a change to something two features share is a shared-file change and is
  recorded in the Project Map's reverse index;
- a capability decision belongs to the feature that first needs it, and is
  recorded, not repeated.

Two things in this stack are shared by construction and are shared-file changes
however small they look:

- **the theme.** It is applied once at startup and every themed window inherits
  it, so a theme change is an application-wide change with no local blast radius
  to appeal to.
- **a persisted docking layout.** Panels belong to the layout, not to the feature
  that introduced them. Adding or removing one changes what every stored layout
  means, including layouts saved by earlier builds.

## Naming and file conventions

`⟨verification required: the project's own conventions⟩`
