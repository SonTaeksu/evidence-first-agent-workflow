# Stack Profiles

A stack profile contains the facts the generic core cannot invent.

| Stack | Directory | Status | Owner inputs still required |
|---|---|---|---|
| React + ASP.NET Core sample | `stacks/react-aspnetcore` | ready for the included sample | adopted projects must reconfirm auth, data access, shared clients, versions, deployment, and validation |
| C# Windows Forms (.NET Framework 4.7.2+) | `stacks/csharp-winforms` | ready for the included skeleton | adopted projects must reconfirm project format, package management, data access, auth, UI automation, localization, and deployment |
| DevExpress WinForms (v24.2+) | `stacks/devexpress-winforms` | planned / blocked | DevExpress version, grid views, command surface, layout control, skins, licensing — a companion to `stacks/csharp-winforms`, which still applies in full |
| WPF (.NET Framework 4.7.2+) | `stacks/csharp-wpf` | planned / blocked | framework version, MVVM pattern, DI container, UI automation, localization — skeleton present but not yet compiled |
| WCF (.NET Framework 4.7.2+) | `stacks/csharp-wcf` | planned / blocked | framework version, binding and security mode, hosting model, proxy generation, external consumers |
| ASMX Web Service 2.0 (.NET Framework 4+) | `stacks/csharp-asmx` | planned / blocked | framework version, SOAP version, proxy generation, authentication, whether external consumers exist |
| DevExpress for ASP.NET Core (v24.2+) | `stacks/devexpress-aspnetcore` | planned / blocked | .NET and DevExpress versions, the private feed and its credential, server-side controls or DevExtreme widgets, reporting host and report storage, client asset delivery — Blazor is out of scope |
| DevExpress WPF (v24.2+) | `stacks/devexpress-wpf` | planned / blocked | .NET and DevExpress versions, the licensed feed, MVVM framework (DevExpress or third-party), binding dialect, theme and its deployed assemblies, GridControl view types, docking — a companion to `stacks/csharp-wpf`, not a replacement |
| Vue.js | `stacks/vue` | planned / blocked | major version (2 or 3 — a hard boundary), build tool, state management, test runner, TypeScript |
| Next.js | `stacks/nextjs` | planned / blocked | major version, router mode (App or Pages), rendering strategy, data layer, auth |
| Node.js | `stacks/nodejs` | planned / blocked | module system (ESM or CommonJS), runtime version, HTTP framework, test runner, TypeScript |
| Go | `stacks/go` | planned / blocked | go directive (1.22 changed loop-variable scope), router, data access, logging |
| Go + HTMX | `stacks/go-htmx` | planned / blocked | everything Go requires, plus HTMX version, template engine, and the fragment convention |
| Rust | `stacks/rust` | planned / blocked | edition and MSRV, async runtime, web framework, error model, data access |
| Elixir | `stacks/elixir` | planned / blocked | Elixir, OTP, Phoenix and LiveView versions, Ecto, project shape, asset pipeline |

To create a stack:

1. copy `templates/stack-profile/`;
2. fill `STACK-INPUTS.md`;
3. add references, pitfalls, skeletons, and provenance;
4. complete `STACK-READINESS.json`;
5. run the readiness validator.

Confirm the copy source itself passes the kit's own validation:

```bash
python ../tools/check-kit-selfcheck/check_kit_selfcheck.py --root ..
```

Stack-specific internal names belong in the relevant private stack pack, not the generic core.

## Add or switch stacks

Two stacks are filled in; the rest are placeholders. React + ASP.NET Core shows a web stack with a rendered document to inspect; C# Windows Forms shows a desktop stack that has none, and how the rendered-output layer is served without one. To fill a placeholder or add a new stack, see [`../docs/getting-started/using-another-stack.md`](../docs/getting-started/using-another-stack.md).
