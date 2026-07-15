# React and ASP.NET Core Capability Detection

| Capability | Sample Evidence | Status | Selected Path | Unknown Rule |
|---|---|---|---|---|
| frontend-shared-api-client | `frontend/src/api.ts` | present | reuse module | do not create a second client |
| generated-openapi-client | no generated client in sample | absent | typed manual adapter | do not invent generated ownership |
| backend-style | Minimal API endpoints in `Program.cs` | present | preserve Minimal API | block style conversion |
| data-access | in-memory repository | present | preserve sample repository | require owner decision before database introduction |
| authentication-provider | no auth in public sample | not-applicable | no auth changes | block auth assumptions |
| design-system | local CSS only | absent | preserve local components | require owner confirmation before adding a library |
| sdk-version | `global.json`, `package.json`, `.csproj` | present | use detected versions | block version-sensitive API when files disagree |

Every adopted project must regenerate these decisions from its own evidence.
