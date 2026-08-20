# Stack-Specific Agent Rules — DevExpress for ASP.NET Core

This file extends root `AGENTS.md`. It does not repeat it.

- Read `STACK-READINESS.json` before any stack-dependent implementation.
- A blocking capability with status `unknown` prohibits the dependent pattern.
  Not "proceed carefully" — prohibits. `ui-component-layer` is the one that
  matters most here: until it is resolved, adding a component means guessing
  between two different products.
- Route documentation lookups through `mcp/source-routing.md`. `dxdocs` is
  authoritative for DevExpress; `microsoft-learn` is authoritative for ASP.NET
  Core, EF Core and .NET, and for nothing DevExpress.
- Use `references/verified-facts.md` and `references/pitfalls.md` instead of
  recall. Every entry there names where it was verified.
- Record every selected capability in the Project Map and repeat it in Gate
  Analysis.

## Stack prohibitions

- **Do not answer a DevExpress API question from `microsoft-learn`, and do not
  answer one from memory.** Component names, property names, tag helper names and
  service-registration calls are all version-sensitive and all look plausible
  when invented. Look them up through `dxdocs`.
- Do not mix an answer about server-side controls into a project using
  DevExtreme's client-side widgets, or the reverse. They are different products;
  an answer carried across is confidently wrong.
- Do not carry a WinForms or WPF reporting answer into this web host, or the
  reverse.
- Do not assume the Report Designer or the Document Viewer works because the
  package is referenced. Registration and client assets are separate facts, and
  each is checked separately.
- Do not report a build as passing on the strength of a cached restore. The
  private feed is only exercised by a restore that actually reaches it.
- Do not write a version number, a package identifier or a licence key into any
  document here that was not read from this project.
- Do not report a validation as passed without the command and its exit code.
- Do not fill a row of `STACK-INPUTS.md` on the owner's behalf. An unanswered
  input is a blocked stack, which is a correct state.
