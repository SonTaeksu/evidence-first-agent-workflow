# Stack Profile

Stack Profile에는 Generic Core가 지어낼 수 없는 Fact가 들어갑니다.

| Stack | 디렉터리 | 상태 | 사용자가 추가로 확인할 입력 |
|---|---|---|---|
| React + ASP.NET Core Sample | `stacks/react-aspnetcore` | 포함 Sample 기준 ready | 적용 Project의 Auth, Data Access, Shared Client, Version, Deployment, Validation 재확인 |
| C# Windows Forms (.NET Framework 4.7.2+) | `stacks/csharp-winforms` | 포함 Skeleton 기준 ready | 적용 Project의 Project Format, Package Management, Data Access, Auth, UI Automation, Localization, Deployment 재확인 |
| WPF (.NET Framework 4.7.2+) | `stacks/csharp-wpf` | planned / blocked | Framework Version, MVVM 패턴, DI 컨테이너, UI Automation, Localization — Skeleton 있으나 아직 컴파일 미검증 |
| WCF (.NET Framework 4.7.2+) | `stacks/csharp-wcf` | planned / blocked | Framework Version, Binding·Security Mode, Hosting Model, Proxy 생성, 외부 소비자 |
| ASMX Web Service 2.0 (.NET Framework 4+) | `stacks/csharp-asmx` | planned / blocked | Framework Version, SOAP Version, Proxy 생성, 인증, 외부 소비자 존재 여부 |
| Vue.js | `stacks/vue` | planned / blocked | Major Version(2/3 — 경계가 단단함), Build Tool, State Management, Test Runner, TypeScript |
| Next.js | `stacks/nextjs` | planned / blocked | Major Version, Router Mode(App/Pages), Rendering 전략, Data Layer, Auth |
| Node.js | `stacks/nodejs` | planned / blocked | Module System(ESM/CommonJS), Runtime Version, HTTP Framework, Test Runner, TypeScript |
| Go | `stacks/go` | planned / blocked | go directive(1.22에서 loop 변수 스코프 변경), Router, Data Access, Logging |
| Go + HTMX | `stacks/go-htmx` | planned / blocked | Go 요구사항 전부 + HTMX Version, Template Engine, Fragment 규약 |
| Rust | `stacks/rust` | planned / blocked | Edition·MSRV, Async Runtime, Web Framework, Error Model, Data Access |
| Elixir | `stacks/elixir` | planned / blocked | Elixir·OTP·Phoenix·LiveView Version, Ecto, Project 형태, Asset Pipeline |

Stack 생성:

1. `templates/stack-profile/` 복사
2. `STACK-INPUTS.md` 작성
3. Reference, Pitfall, Skeleton, Provenance 추가
4. `STACK-READINESS.json` 완료
5. Readiness Validator 실행

복사 원본 자체가 킷 자신의 Validation을 통과하는지 확인합니다.

```bash
python ../tools/check-kit-selfcheck/check_kit_selfcheck.py --root ..
```

Stack 고유 사내 명칭은 Generic Core가 아니라 관련 비공개 Stack Pack에 둡니다.

## 스택 추가·전환

두 Stack이 채워져 있고 나머지는 placeholder입니다. React + ASP.NET Core는 검사할 Rendered 문서가 있는 Web Stack의 예시이고, C# Windows Forms는 그것이 없는 Desktop Stack에서 Rendered Output Layer를 어떻게 대신 확보하는지 보여줍니다. placeholder를 채우거나 새 스택을 추가하려면 [`../docs/getting-started/using-another-stack.md`](../docs/getting-started/using-another-stack.md) 참고.
