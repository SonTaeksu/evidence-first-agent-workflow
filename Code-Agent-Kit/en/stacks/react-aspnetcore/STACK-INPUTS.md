# React and ASP.NET Core Stack Inputs

## Confirmed for the public sample

The `Key` column joins each row to `STACK-READINESS.json`. The two files are
compared and a disagreement is reported — and because that report is a warning, and
a warning derives `provisional`, a stack declaring `ready` with disagreeing files
fails. Change both, together.

| Input | Key | Value or Path | Evidence | Status |
|---|---|---|---|---|
| .NET SDK | `runtime-sdk-versions` | 10.0.301 with latest-feature roll-forward | `/global.json` | detected |
| Backend target | `runtime-sdk-versions` | `net10.0` | sample `.csproj` files | detected |
| React | `runtime-sdk-versions` | 19.2.7 | frontend `package.json` | detected |
| TypeScript | `runtime-sdk-versions` | 7.0.2 | frontend `package.json` | detected |
| Feature boundary | `feature-model` | vertical task-flow slice across UI, API, and tests | `feature-model.md` | confirmed |
| Communication contract | `communication-contract` | JSON REST through one frontend API module | `communication-contract.md` | confirmed |
| Validation | `validation-profile` | frontend, backend, E2E, color, scope, docs | `validation/validation-profile.md` | confirmed |
| Confidentiality | `confidentiality` | public synthetic sample only | repository policy | confirmed |
| Authoritative documentation | `authoritative-sources` | Microsoft Learn and the official repositories, through source routing | `mcp/source-routing.md`, `evidence-provenance.md` | confirmed |

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
