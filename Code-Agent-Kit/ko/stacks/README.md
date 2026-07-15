# Stack Profile

Stack Profile에는 Generic Core가 지어낼 수 없는 Fact가 들어갑니다.

| Stack | 상태 | 사용자가 추가로 확인할 입력 |
|---|---|---|
| React + ASP.NET Core Sample | 포함 Sample 기준 ready | 적용 Project의 Auth, Data Access, Shared Client, Version, Deployment, Validation 재확인 |
| Go + HTMX | planned / blocked | Go Version, Router, Template Engine, HTMX Version, Fragment Convention, Auth, DB, Asset Build |
| Rust | planned / blocked | MSRV/Toolchain, Web Framework, Async Runtime, Error Model, DB, Auth, Deployment |
| Elixir | planned / blocked | Elixir/OTP/Phoenix/LiveView Version, Context Boundary, Ecto, Auth, Asset, Deployment |

Stack 생성:

1. `templates/stack-profile/` 복사
2. `STACK-INPUTS.md` 작성
3. Reference, Pitfall, Skeleton, Provenance 추가
4. `STACK-READINESS.json` 완료
5. Readiness Validator 실행

Stack 고유 사내 명칭은 Generic Core가 아니라 관련 비공개 Stack Pack에 둡니다.

## 스택 추가·전환

React + ASP.NET Core만 ready 예시이고 나머지는 placeholder입니다. placeholder를 채우거나 새 스택(예: 데스크톱·레거시 UI)을 추가하려면 [`../docs/getting-started/using-another-stack.md`](../docs/getting-started/using-another-stack.md) 참고.
