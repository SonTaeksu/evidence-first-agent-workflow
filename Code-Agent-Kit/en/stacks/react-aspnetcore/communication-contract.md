# React and ASP.NET Core Communication Contract

- Frontend server calls go through `frontend/src/api.ts`.
- Request and response TypeScript types mirror backend DTO or endpoint payloads.
- JSON REST is used for the public sample.
- Backend validation errors use the established endpoint error shape.
- Contract changes update frontend types, backend payloads, component tests, API tests, and E2E together.
- A generated client may replace the manual adapter only when capability detection confirms ownership and regeneration commands.
