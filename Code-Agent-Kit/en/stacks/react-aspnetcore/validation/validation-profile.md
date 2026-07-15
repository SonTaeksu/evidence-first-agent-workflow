# React and ASP.NET Core Validation Profile

| Layer | Commands |
|---|---|
| Stack readiness | `python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/react-aspnetcore` |
| Frontend artifact | `npm run lint`, `npm run test`, `npm run build` |
| Backend artifact/runtime | `dotnet restore`, `dotnet build`, `dotnet test` |
| Rendered output | SPA screen extraction and completeness comparison |
| Runtime behavior | `npm run e2e` |
| Color/accessibility | `npm run color:static`, `npm run e2e:color` |
| Scope/state | Git scope and document-sync tools |

A layer that cannot run remains PENDING with reason.
