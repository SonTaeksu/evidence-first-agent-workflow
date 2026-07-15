# React and ASP.NET Core Evidence Provenance

| Claim | Source | Verification |
|---|---|---|
| .NET SDK baseline is 10.0.301 | `/global.json` | parsed file |
| Backend target is net10.0 | sample `.csproj` | parsed project files |
| React is 19.2.7 | frontend `package.json` | parsed package manifest |
| Frontend API entry point is `src/api.ts` | sample source | source inspection |
| Sample has no authentication provider | sample source and configuration | repository search |

Version-sensitive implementation still requires official Microsoft Learn or React documentation through the configured source routing.
