# Feature Model — DevExpress WinForms

## What one feature is

`⟨verification required: the owner's definition of a feature boundary in this
codebase⟩`

The kit cannot derive this. A feature boundary that is guessed produces state
documents that describe nothing, and the Project Map stops being usable.

## What a feature may touch

Until the boundary is confirmed, treat the following as the working rule and
record every departure from it:

- one feature owns its own screen — a form or a modal dialog — together with its
  service boundary, its designer file and its tests;
- actions that share the same screen state stay in one feature: load, filter,
  edit, validate, save, cancel;
- a change to something two features share is a shared-file change and is recorded
  in the Project Map's reverse index;
- a capability decision belongs to the feature that first needs it, and is
  recorded, not repeated.

## Shared dependencies to declare

A change to any of these lists the screens affected and the regression checks run.
The first three are what makes this stack different from plain Windows Forms:
DevExpress moves several decisions from the screen to the application.

- the application-wide skin or appearance configuration — it reaches every screen;
- a shared appearance or utility type from `DevExpress.Utils`, used by more than
  one control;
- a shared command surface: a ribbon or bar layout that more than one form
  inherits or reuses;
- a reusable user control that owns behaviour and is consumed by more than one
  screen;
- the service interface a form calls;
- a base form or shared designer partial.

## Naming and file conventions

`⟨verification required: the project's own conventions⟩`

## Decomposition threshold

The core Gate requires a Todo block list before code when a task crosses a
complexity threshold. For this stack, create the block list when any of these
applies:

- two or more data-bound grids or lists on one screen, or one grid with more than
  one view;
- three or more user actions that change persisted state;
- a new screen plus a change to an existing service contract;
- a layout change that touches a container hierarchy rather than a single control;
- any change to the shared appearance configuration or the shared command surface.
