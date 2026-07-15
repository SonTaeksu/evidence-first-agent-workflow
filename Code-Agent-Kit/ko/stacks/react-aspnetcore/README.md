# React + ASP.NET Core Verified Stack Profile

이 Profile은 **포함된 공개 Sample 기준으로 Ready**입니다. 다른 Project는 자체 Version, Capability, Contract, Owner Policy를 다시 확인해야 합니다.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

## 핵심 File

- [Stack 입력](STACK-INPUTS.md)
- `STACK-READINESS.json`
- [Capability Detection](capability-detection.md)
- [Feature Model](feature-model.md)
- [Artifact Contract](artifact-contract.md)
- [Communication Contract](communication-contract.md)
- [Evidence Provenance](evidence-provenance.md)
- [Reference Index](references/_index.md)
- [검증 Pitfall](references/pitfalls.md)
- [검증 Fact](references/verified-facts.md)
- [Skeleton Source](skeletons/README.md)
- [Validation Profile](validation/validation-profile.md)
- [MCP Source Routing](mcp/source-routing.md)

## 포함 Sample Fact

- React 19.2.7
- TypeScript 7.0.2
- Vite 8.1.4
- ASP.NET Core `net10.0`
- .NET SDK 기준 10.0.301
- Minimal API
- In-memory Repository
- Frontend API Module 하나를 통한 JSON REST

이 내용은 Sample Fact이며 적용 Project의 자동 Policy가 아닙니다.

## 다른 Project에서 필요한 Owner Decision

- 지원 .NET 및 Node Version
- API Style
- Data Access
- Authentication 및 Authorization
- Shared 또는 Generated Client
- Design System 및 State/Router Library
- Deployment 및 Secret 관리 Rule
- 조직 전용 Validation
