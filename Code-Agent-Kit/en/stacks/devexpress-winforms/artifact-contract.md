# Artifact Contract — DevExpress WinForms

What this stack produces, and what counts as evidence that it was produced. The
plain Windows Forms artifact rules in
[`../csharp-winforms/artifact-contract.md`](../csharp-winforms/artifact-contract.md)
apply unchanged; this document records what DevExpress adds to them.

## Build output

`⟨verification required: the artefact this project's build produces, where it is
written, and which DevExpress assemblies are deployed alongside it⟩`

A DevExpress application ships the component assemblies with it. Which ones, and
whether the licence permits it, is an owner fact — see the `licensing` input.

## Ownership

- **Layout is generated.** The designer owns `*.Designer.cs` and rewrites it. A
  DevExpress form generates more of that file than a plain form, not less, so the
  temptation to hand-edit is larger and the loss is the same.
- **Behaviour is hand-written**, in the form's partial class.
- **`licenses.licx` is a build input, not source code.** It is generated and
  maintained by the tooling. Editing it by hand to make a build pass is a change
  to a licensing artefact, and it belongs in the owner's decision rather than in a
  fix.
- **Skin and appearance configuration is application-wide.** Whether it lives in
  the entry point, a shared base form or a startup module is a project fact
  `⟨verification required: where this project applies it⟩` — but wherever it is,
  a change there affects every screen, and the change lists them.

## What is evidence

- A build or test **exit code**, with the command that produced it. A log line
  saying success while the exit code is non-zero is not evidence — it is the
  failure mode this kit exists to catch.
- A file that exists at a stated path. `check-stack-readiness` resolves evidence
  paths, so a cited path that does not exist is treated as absent.
- For screen contents, the designer control tree rather than the running window.
  Windows Forms has no rendered document, and adding DevExpress does not create
  one. See `validation/validation-profile.md` for the one caveat that applies to
  DevExpress designer files.

## What is not evidence

- A self-report with no command.
- A build that succeeded on a developer machine, offered as proof that the build
  agent will succeed. The licence is the difference, and it is invisible in the
  source.
- A control that is declared but never added to a parent's control collection. It
  exists in the code and not on the screen.
- A screenshot with nothing to compare it against.
