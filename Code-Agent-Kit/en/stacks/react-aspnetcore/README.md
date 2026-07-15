# React + ASP.NET Core Verified Stack Profile

This profile is **ready for the included public sample**. Another project must reconfirm its own versions, capabilities, contracts, and owner policies.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

## Core files

- [Stack inputs](STACK-INPUTS.md)
- `STACK-READINESS.json`
- [Capability detection](capability-detection.md)
- [Feature model](feature-model.md)
- [Artifact contract](artifact-contract.md)
- [Communication contract](communication-contract.md)
- [Evidence provenance](evidence-provenance.md)
- [Reference index](references/_index.md)
- [Verified pitfalls](references/pitfalls.md)
- [Verified facts](references/verified-facts.md)
- [Skeleton sources](skeletons/README.md)
- [Validation profile](validation/validation-profile.md)
- [MCP source routing](mcp/source-routing.md)

## Included sample facts

- React 19.2.7
- TypeScript 7.0.2
- Vite 8.1.4
- ASP.NET Core `net10.0`
- .NET SDK baseline 10.0.301
- Minimal API
- In-memory repository
- JSON REST through one frontend API module

These are sample facts, not automatic policy for an adopted project.

## Owner decisions required in another project

- supported .NET and Node versions;
- API style;
- data access;
- authentication and authorization;
- shared or generated clients;
- design system and state/router libraries;
- deployment and secret-management rules;
- organization-specific validation.
