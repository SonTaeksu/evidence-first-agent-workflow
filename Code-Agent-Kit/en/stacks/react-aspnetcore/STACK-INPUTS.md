# React and ASP.NET Core Stack Inputs

## Confirmed for the public sample

| Input | Value or Path | Evidence | Status |
|---|---|---|---|
| .NET SDK | 10.0.301 with latest-feature roll-forward | `/global.json` | detected |
| Backend target | `net10.0` | sample `.csproj` files | detected |
| React | 19.2.7 | frontend `package.json` | detected |
| TypeScript | 7.0.2 | frontend `package.json` | detected |
| Feature boundary | vertical task-flow slice across UI, API, and tests | `feature-model.md` | confirmed |
| Communication contract | JSON REST through one frontend API module | `communication-contract.md` | confirmed |
| Validation | frontend, backend, E2E, color, scope, docs | `validation/validation-profile.md` | confirmed |
| Confidentiality | public synthetic sample only | repository policy | confirmed |

## Inputs required when adopting this stack profile in another project

The project owner must confirm:

- actual supported .NET and Node versions;
- Minimal API or Controller ownership;
- EF Core, Dapper, ADO.NET, or another data-access path;
- authentication provider and authorization policy;
- existing shared API client or generated OpenAPI client;
- error contract and ProblemDetails policy;
- design system and routing/state libraries;
- production deployment and secret-management constraints;
- organization-specific validation commands.

Until confirmed, the related capability remains `unknown` and dependent changes are blocked.
