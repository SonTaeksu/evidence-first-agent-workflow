# DevExpress for ASP.NET Core

DevExpress components on ASP.NET Core MVC and Razor Pages, together with
DevExpress Reporting (XtraReports) hosted on the web. **v24.2 or later only.**

**Blazor is out of scope.** DevExpress ships a separate Blazor component line
with its own registration, rendering and lifecycle rules; nothing in this profile
was written for it, so do not treat any statement here as covering a Blazor
project.

This is a **companion to a plain ASP.NET Core profile, not a replacement**. The
hosting model, routing, dependency injection, configuration and Entity Framework
Core questions are ordinary ASP.NET Core questions and are answered from the
ordinary ASP.NET Core sources. What this profile adds is the part that is not
ordinary: a private package feed, a component library that exists in two
different shapes, and a reporting stack that needs services registered and
client assets served before it renders anything.

Reporting spans desktop and web. **This profile covers web hosting of reports
only** — a WinForms or WPF report host is a different question with different
answers, and should not be answered from here.

**State: `blocked`.** Not broken — waiting. The owner inputs in
`STACK-INPUTS.md` are unanswered, so `check-stack-readiness` derives `blocked`,
and `tools/check-last` deliberately skips a stack in that state so a
placeholder does not produce a false alarm on every run.

What is already here and useful:

- `references/pitfalls.md` — failures in this stack that produce no error message;
- `capability-detection.md` — how to tell what this project actually uses,
  starting with whether it uses server-side controls or client-side widgets;
- `mcp/source-routing.md` — which documentation source is authoritative, which
  must not be consulted, and what was and was not verified about the DevExpress
  MCP server.

To reach `ready`, answer `STACK-INPUTS.md` with evidence that exists. Evidence is
measured, not declared:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
