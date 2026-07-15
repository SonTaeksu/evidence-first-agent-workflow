# React 및 ASP.NET Core Artifact Contract

| Artifact | 필수 형태 | Source 또는 Skeleton | Validation |
|---|---|---|---|
| React UI | `.tsx`, Typed Props/State, Project CSS | 기존 Sample Component | TypeScript, Vitest, Playwright |
| Frontend Contract | TypeScript Type와 API Module 하나 | 기존 `src/types.ts`, `src/api.ts` | Build 및 E2E |
| ASP.NET Core API | 실제 `.cs`, `.csproj` File | 기존 Minimal API Sample | Restore, Build, Test |
| Test | Vitest, xUnit, Playwright Source | 기존 Test Project | Test Exit Code |

필수 React 또는 .NET Artifact를 독립 HTML 한 장으로 대체하지 않습니다.
