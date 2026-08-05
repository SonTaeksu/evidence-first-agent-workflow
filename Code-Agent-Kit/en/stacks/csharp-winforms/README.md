# C# Windows Forms Verified Stack Profile

Baseline: C# on .NET Framework 4.7.2 or later (`net472`+), Windows Forms desktop.

This profile is **ready for the included reference skeleton** under `skeletons/MinimalApp/`. An adopted project must reconfirm its own project format, data access, authentication, deployment, and UI evidence route.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/csharp-winforms
```

## Why this stack needs its own evidence route

Windows Forms has no DOM. The kit's rendered-output layer normally reads a rendered document; here there is nothing to read without launching the application. The designer file is the deterministic substitute: it is generated, it is the single declaration of what a form contains, and it can be parsed without compiling.

```text
source asset
→ screen specification (Gate §1)
→ designer file
→ extracted control tree
→ deterministic comparison
```

`tools/extract_designer_tree.py` and `tools/check_designer_spec.py` implement that comparison. See [`references/ui-evidence-contract.md`](references/ui-evidence-contract.md).

## Core files

| File | Purpose |
|---|---|
| `STACK.md` | baseline, layout, commands |
| `STACK-INPUTS.md` | what the reference confirms and what an adopted project must supply |
| `capability-detection.md` | project format, designer ownership, DPI, automation, data, auth |
| `artifact-contract.md` | which files are hand-written and which are generated |
| `communication-contract.md` | UI thread boundary and the single service entry point |
| `references/pitfalls.md` | verified failure modes |
| `references/verified-facts.md` | version-sensitive facts with sources |
| `validation/validation-profile.md` | build, test, and UI gates |

## Reference skeleton facts

- SDK-style project targeting `net472`, `OutputType` `WinExe`
- per-monitor v2 DPI awareness configured in `App.config`, Windows 10 compatibility declared in `app.manifest`
- layout in `MainForm.Designer.cs`, behaviour in `MainForm.cs`
- one service interface as the form's only route outside itself
- no database, no authentication provider, no localization beyond the invariant culture

These are skeleton facts, not policy for an adopted project.

## Owner decisions required in another project

- project format: SDK-style `net472` or legacy `.csproj`, and package management
- data access and connection handling
- authentication and authorization
- UI automation harness, if any
- localization and satellite assemblies
- deployment: ClickOnce, MSI, or copy
- confidentiality classification of forms, connection strings, and screenshots

Until confirmed, the related capability remains `unknown` and dependent changes are blocked.
