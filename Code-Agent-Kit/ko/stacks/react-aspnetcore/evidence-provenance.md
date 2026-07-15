# React 및 ASP.NET Core Evidence Provenance

| Claim | Source | Verification |
|---|---|---|
| .NET SDK 기준 10.0.301 | `/global.json` | File Parse |
| Backend Target net10.0 | Sample `.csproj` | Project File Parse |
| React 19.2.7 | Frontend `package.json` | Package Manifest Parse |
| Frontend API Entry Point `src/api.ts` | Sample Source | Source 검사 |
| Sample에 Authentication Provider 없음 | Sample Source 및 Config | Repository Search |

Version 민감 구현은 설정된 Source Routing을 통해 Microsoft Learn 또는 React 공식 문서를 추가 확인합니다.
