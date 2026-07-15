# React 및 ASP.NET Core Validation Profile

| Layer | 명령 |
|---|---|
| Stack Readiness | `python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/react-aspnetcore` |
| Frontend Artifact | `npm run lint`, `npm run test`, `npm run build` |
| Backend Artifact/Runtime | `dotnet restore`, `dotnet build`, `dotnet test` |
| Rendered Output | SPA Screen 추출 및 완전성 비교 |
| Runtime Behavior | `npm run e2e` |
| Color/Accessibility | `npm run color:static`, `npm run e2e:color` |
| Scope/State | Git Scope 및 Document Sync Tool |

실행할 수 없는 Layer는 이유와 함께 PENDING으로 남깁니다.
