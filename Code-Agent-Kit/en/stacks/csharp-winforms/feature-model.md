# C# Windows Forms Feature Model

- **Feature unit**: one user-visible screen — a form or a modal dialog — together with its service boundary, its designer file, and its tests.
- Actions that share the same screen state stay in one feature: load, filter, edit, validate, save, cancel.
- A separate feature is required when the screen is launched independently, when the service boundary differs, when the deployment artifact differs, or when the security boundary differs.
- A reusable `UserControl` is a feature when it owns behaviour and is consumed by more than one screen. It is a shared dependency, so its change lists the screens it affects.
- Feature state lives under `docs/features/<feature>.current.md`, its history, and the active worklog.

## Shared dependencies to declare

A change to any of these lists the screens affected and the regression checks run:

- a `UserControl` used by more than one form;
- the service interface a form calls;
- a base form or shared designer partial;
- application-wide configuration in `App.config`;
- a shared `.resx` or theme resource.

## Decomposition threshold

The core Gate requires a Todo block list before code when a task crosses a complexity threshold. For this stack, create the block list when any of these applies:

- two or more data-bound grids or lists on one form;
- three or more user actions that change persisted state;
- a new form plus a change to an existing service contract;
- a layout change that touches a container hierarchy rather than a single control.
