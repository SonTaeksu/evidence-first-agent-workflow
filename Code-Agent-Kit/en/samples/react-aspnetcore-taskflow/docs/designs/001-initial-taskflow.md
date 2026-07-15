# Design: Initial TaskFlow Sample

## Request

Create a public React + ASP.NET Core sample that demonstrates the workflow without retaining organization- or product-specific details.

## Current Evidence

- The workflow core and bilingual design review already exist.
- Public Microsoft Learn MCP is available for Microsoft technologies.
- Context7 can provide React and related library documentation.
- A mainstream stack reduces technology novelty as a confounding variable.

## Assumptions

- The first sample should run without an external database.
- Persistence is a later experiment.
- English is the default public language.
- The sample should remain small enough for paired control/treatment tasks.

## Out of Scope

- authentication and authorization;
- persistent database;
- multi-user concurrency;
- production deployment hardening;
- full visual design system.

## Impact

- Adds the first executable stack sample.
- Adds stack-specific validation and MCP routing.
- Establishes the extension contract for future Rust, Go + HTMX, and Elixir profiles.

## Expected Files

- `AGENTS.md`
- `README.md`
- `docker-compose.yml`
- `frontend/package.json`
- `frontend/src/App.tsx`
- `frontend/src/api.ts`
- `frontend/src/components/TaskForm.tsx`
- `frontend/src/components/TaskList.tsx`
- `frontend/e2e/taskflow.spec.ts`
- `backend/TaskFlow.Api/Program.cs`
- `backend/TaskFlow.Api/Domain/TaskItem.cs`
- `backend/TaskFlow.Api/Repositories/InMemoryTaskRepository.cs`
- `backend/TaskFlow.Api.Tests/TaskApiTests.cs`
- `docs/current.md`
- `docs/history.md`
- `docs/project-map.md`
- `scripts/validate.ps1`
- `scripts/validate.sh`

## Tasks

1. Create backend API and domain rules.
2. Create React frontend.
3. Add frontend, backend, and E2E tests.
4. Add deterministic validation scripts.
5. Add sample workflow state.
6. Add Docker execution.

## Todos

- [x] Define status workflow.
- [x] Implement API.
- [x] Implement frontend.
- [x] Add test sources.
- [x] Add state documents.
- [ ] Run local or CI validation.
- [ ] Record validation evidence.

## Validation Checklist

- [ ] `dotnet build` PASS
- [ ] `dotnet test` PASS
- [x] `npm run lint` PASS
- [x] `npm run test` PASS
- [x] `npm run build` PASS
- [ ] `npm run e2e` PASS
- [ ] Docker build PASS
- [ ] Final Diff contains no unrelated changes
