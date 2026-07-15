# React + ASP.NET Core Stack

## Supported baseline

- React: 19.2.x
- Vite: 8.x
- TypeScript: 7.x
- Node.js: 22.12 or later
- .NET SDK: 10.x LTS

The sample intentionally uses an in-memory backend repository to keep the first run independent from an external database. Persistence can be added as a later feature experiment.

## Architecture

```text
frontend/
  React view and API client

backend/
  ASP.NET Core minimal API
  domain model
  request DTOs
  repository abstraction

docs/
  current.md
  history.md
  project-map.md
  designs/
  evidence/
```

## Commands

Frontend:

```bash
npm install
npm run lint
npm run test
npm run build
npm run e2e
```

Backend:

```bash
dotnet restore
dotnet build
dotnet test
dotnet run
```
