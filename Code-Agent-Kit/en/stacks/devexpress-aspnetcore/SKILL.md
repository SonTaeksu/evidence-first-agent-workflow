---
name: devexpress-aspnetcore
description: Use this skill when implementing or validating work in the DevExpress for ASP.NET Core stack, including DevExpress Reporting hosted on the web.
---

# Stack Skill Router — DevExpress for ASP.NET Core

Routes to the smallest relevant document. The core workflow is not repeated here.

## Always read

- `STACK.md`
- `AGENTS.stack.md`
- `mcp/source-routing.md`
- `validation/validation-profile.md`

## Task routing

| Task | Read |
|---|---|
| New feature | `feature-model.md`, then `capability-detection.md` |
| Adding or changing any DevExpress component | `capability-detection.md` first — server-side control or client-side widget is not a detail |
| Anything about report hosting, the viewer or the designer | `capability-detection.md`, then look it up through `dxdocs` — reporting needs `technologies: ["AspNetCore", "XtraReports"]`, not `AspNetCore` alone |
| Report storage, opening or saving a report | `references/pitfalls.md`, then `communication-contract.md` |
| Package restore or feed failure | `STACK.md` under "Package source", then `validation/validation-profile.md` |
| Plain ASP.NET Core, EF Core or .NET question | `mcp/source-routing.md` — this one goes to `microsoft-learn`, not to `dxdocs` |
| Contract or interface change | `communication-contract.md`, `artifact-contract.md` |
| Anything version-sensitive | `references/verified-facts.md`, then look it up through `dxdocs` |
| Debugging | `references/pitfalls.md` — most failures in this stack are silent |
| Reporting a result | `evidence-provenance.md` |
