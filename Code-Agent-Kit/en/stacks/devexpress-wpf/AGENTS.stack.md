# Stack-Specific Agent Rules — DevExpress WPF (v24.2+)

This file extends root `AGENTS.md`. It does not repeat it. It also extends
`../csharp-wpf/AGENTS.stack.md`, which stays in force: this stack adds DevExpress
rules on top of the WPF ones rather than replacing them.

- Read `STACK-READINESS.json` before any stack-dependent implementation.
- A blocking capability with status `unknown` prohibits the dependent pattern.
  Not "proceed carefully" — prohibits.
- Route documentation lookups through `mcp/source-routing.md`. `dxdocs` is
  authoritative for DevExpress; `microsoft-learn` and `wpf-docs` are
  authoritative for plain WPF, XAML and .NET. Neither side answers for the other.
- Use `references/verified-facts.md` and `references/pitfalls.md` instead of
  recall. Every entry there names where it was verified.
- Record every selected capability in the Project Map and repeat it in Gate
  Analysis.

## Stack prohibitions

- Do not answer a DevExpress API question from `microsoft-learn`, from `wpf-docs`
  or from memory. Microsoft does not document these controls, and a DevExpress
  answer recalled rather than looked up is version-shaped: it usually compiles,
  which is why it survives review.
- Do not apply an answer written for one `GridControl` view type to another. The
  view type has to be established first.
- Do not carry an answer across DevExpress versions. On a v24.2 project, pin the
  documentation server to v24.2 rather than querying the latest endpoint.
- Do not treat this profile as covering plain WPF. For binding traces, the
  Dispatcher, resource lookup or XAML compilation, read `../csharp-wpf`.
- Do not report a validation as passed without the command and its exit code, and
  do not report a themed UI as correct from a developer machine — the theme
  assemblies are present there whether or not they are deployed.
- Do not fill a row of `STACK-INPUTS.md` on the owner's behalf. An unanswered
  input is a blocked stack, which is a correct state.
