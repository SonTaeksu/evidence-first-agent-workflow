# Stack-Specific Agent Rules — DevExpress WinForms

This file extends root `AGENTS.md` **and** `../csharp-winforms/AGENTS.stack.md`.
It does not repeat either.

Read the plain WinForms rules first. Designer ownership, the UI thread boundary,
DPI configuration, project format and the build-command branch all still apply
here unchanged — a DevExpress control is still a Windows Forms control. This file
adds only what DevExpress changes on top.

- Read `STACK-READINESS.json` before any stack-dependent implementation.
- A blocking capability with status `unknown` prohibits the dependent pattern.
  Not "proceed carefully" — prohibits.
- Route documentation lookups through `mcp/source-routing.md`. `dxdocs` is
  authoritative for DevExpress; `microsoft-learn` is authoritative for Windows
  Forms and .NET and for nothing DevExpress.
- Use `references/verified-facts.md` and `references/pitfalls.md` instead of
  recall. Every entry there names where it was verified.
- Record every selected capability in the Project Map and repeat it in Gate
  Analysis.

## Stack prohibitions

- Do not answer a DevExpress API question from `microsoft-learn`, from a
  general package-documentation server, or from memory. Microsoft Learn does not
  document a third-party control library, so it will answer about the nearest
  Windows Forms type instead — confidently, and about a different control.
- Do not assume a DevExpress type behaves like the `System.Windows.Forms` type
  with a similar name. The similarity is in the name; the members are not the
  same set and a carried-over assumption compiles or fails for reasons that look
  unrelated.
- Do not write a DevExpress version number, member name, enumeration value or
  namespace you did not look up in this session. That is the specific failure this
  kit exists to stop, and a control library with thousands of members is where it
  happens most.
- Do not configure grid behaviour on the `GridControl`. The control holds the
  data; the view holds the behaviour. Code written against the wrong object
  compiles and silently does nothing.
- Do not position a child of a `LayoutControl` with coordinates. Position is
  owned by the layout item, and the assignment is discarded without an error.
- Do not hard-code colours or fonts on a skinned form. The skin decides
  appearance; a control-level override either loses or produces the one control
  that does not match the application.
- Do not hand-edit designer-generated code. DevExpress forms generate more of it,
  not less, and the designer rewrites all of it.
- Do not treat this stack as applicable below v24.2. See `README.md` for why the
  boundary is there.
- Do not report a validation as passed without the command and its exit code.
- Do not fill a row of `STACK-INPUTS.md` on the owner's behalf. An unanswered
  input is a blocked stack, which is a correct state.
