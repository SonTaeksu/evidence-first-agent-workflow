# React 및 ASP.NET Core Stack 입력

## 공개 Sample에서 확인된 내용

| 입력 | 값 또는 경로 | Evidence | 상태 |
|---|---|---|---|
| .NET SDK | 10.0.301, latest-feature Roll-forward | `/global.json` | detected |
| Backend Target | `net10.0` | Sample `.csproj` File | detected |
| React | 19.2.7 | Frontend `package.json` | detected |
| TypeScript | 7.0.2 | Frontend `package.json` | detected |
| Feature Boundary | UI, API, Test를 포함한 Vertical Task-flow Slice | `feature-model.md` | confirmed |
| Communication Contract | Frontend API Module 하나를 통한 JSON REST | `communication-contract.md` | confirmed |
| Validation | Frontend, Backend, E2E, Color, Scope, Docs | `validation/validation-profile.md` | confirmed |
| 보안 등급 | 공개 Synthetic Sample만 사용 | Repository Policy | confirmed |

## 다른 Project에 이 Stack Profile을 적용할 때 필요한 입력

Project Owner가 다음을 확인해야 합니다.

- 실제 지원 .NET 및 Node Version
- Minimal API 또는 Controller Ownership
- EF Core, Dapper, ADO.NET 등 Data Access 경로
- Authentication Provider와 Authorization Policy
- 기존 Shared API Client 또는 Generated OpenAPI Client
- Error Contract와 ProblemDetails Policy
- Design System, Router, State Library
- Production 배포 및 Secret 관리 제약
- 조직별 Validation 명령

확인 전 관련 Capability는 `unknown`이며 의존 변경을 막습니다.
