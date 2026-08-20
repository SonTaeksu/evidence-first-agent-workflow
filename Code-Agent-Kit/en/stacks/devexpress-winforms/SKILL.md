---
name: devexpress-winforms
description: Use this skill when implementing or validating work on DevExpress WinForms controls, v24.2 or later. It is a companion to the csharp-winforms skill, not a replacement for it.
---

# Stack Skill Router — DevExpress WinForms

Routes to the smallest relevant document. The core workflow is not repeated here,
and neither is the plain Windows Forms profile.

## Always read

- `../csharp-winforms/STACK.md` and `../csharp-winforms/AGENTS.stack.md` — the
  base rules this stack sits on top of
- `STACK.md`
- `AGENTS.stack.md`
- `mcp/source-routing.md`
- `validation/validation-profile.md`

## Task routing

| Task | Read |
|---|---|
| New feature | `feature-model.md`, then `capability-detection.md` |
| Grid work | `references/pitfalls.md`, then look the members up through `dxdocs` |
| Ribbon, bars or any command surface | `capability-detection.md`, then `dxdocs` |
| Layout change | `references/pitfalls.md`, `artifact-contract.md` |
| Skins, themes or appearance | `references/pitfalls.md`, then `dxdocs` |
| Threading or background work | `../csharp-winforms/communication-contract.md` |
| Contract or interface change | `communication-contract.md`, `artifact-contract.md` |
| Anything version-sensitive | `references/verified-facts.md`, then look it up through `dxdocs24_2` |
| Licensing or a build that fails only on the agent | `capability-detection.md`, `validation/validation-profile.md` |
| Debugging | `references/pitfalls.md` — most failures in this stack are silent |
| Reporting a result | `evidence-provenance.md` |
