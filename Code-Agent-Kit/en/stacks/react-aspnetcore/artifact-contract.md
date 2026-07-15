# React and ASP.NET Core Artifact Contract

| Artifact | Required Form | Source or Skeleton | Validation |
|---|---|---|---|
| React UI | `.tsx`, typed props/state, project CSS | existing sample components | TypeScript, Vitest, Playwright |
| Frontend contract | TypeScript types and one API module | existing `src/types.ts`, `src/api.ts` | build and E2E |
| ASP.NET Core API | real `.cs` and `.csproj` files | existing Minimal API sample | restore, build, tests |
| Tests | Vitest, xUnit, Playwright source | existing test projects | test exit codes |

Do not replace required React or .NET artifacts with a standalone HTML-only implementation.
