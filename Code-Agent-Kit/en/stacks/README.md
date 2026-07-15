# Stack Profiles

A stack profile contains the facts the generic core cannot invent.

| Stack | Status | Owner inputs still required |
|---|---|---|
| React + ASP.NET Core sample | ready for the included sample | adopted projects must reconfirm auth, data access, shared clients, versions, deployment, and validation |
| Go + HTMX | planned / blocked | Go version, router, template engine, HTMX version, fragment conventions, auth, DB, asset build |
| Rust | planned / blocked | MSRV/toolchain, web framework, async runtime, error model, DB, auth, deployment |
| Elixir | planned / blocked | Elixir/OTP/Phoenix/LiveView versions, Context boundaries, Ecto, auth, assets, deployment |

To create a stack:

1. copy `templates/stack-profile/`;
2. fill `STACK-INPUTS.md`;
3. add references, pitfalls, skeletons, and provenance;
4. complete `STACK-READINESS.json`;
5. run the readiness validator.

Stack-specific internal names belong in the relevant private stack pack, not the generic core.

## Add or switch stacks

React + ASP.NET Core is the one ready example; the others are placeholders. To fill a placeholder or add a new stack (e.g. a desktop or legacy UI), see [`../docs/getting-started/using-another-stack.md`](../docs/getting-started/using-another-stack.md).
