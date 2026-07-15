# React and ASP.NET Core Feature Model

- Feature unit: a user-visible vertical slice with frontend behavior, API contract, backend implementation, and tests.
- Actions such as create, list, update status, approve, and reject stay in one feature when they share the same domain state.
- A separate feature is required when ownership, deployment, security boundary, or independently versioned contract differs.
- Feature state lives under `docs/features/<feature>.current.md`, history, and active worklog.
