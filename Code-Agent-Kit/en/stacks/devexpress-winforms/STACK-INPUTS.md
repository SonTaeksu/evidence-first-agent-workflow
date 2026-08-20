# Stack Inputs — DevExpress WinForms

Nothing in this file is filled in, and that is the current state rather than an
omission. Each row is a fact about *your* project that the kit cannot derive, and
`STACK-READINESS.json` declares `blocked` until they are answered with evidence.

Evidence is **measured**: `check-stack-readiness` resolves each path against the
tree, so a path that does not exist is not evidence.

**This table and `STACK-READINESS.json` must agree.** They are compared, joined on
the `Key` column, and a disagreement is reported. Because that report is a warning,
and a warning derives `provisional`, a stack that declares `ready` while the two
files disagree will fail. A table with no `Key` column is worse than a
disagreement: it is not compared at all, and that is reported too. Fill in both,
or run the interview prompt (`prompts/8-fill-stack.md`) and let the agent keep
them in step.

The plain Windows Forms inputs are not repeated here. Answer
[`../csharp-winforms/STACK-INPUTS.md`](../csharp-winforms/STACK-INPUTS.md) as
well — project format, package management, data access, authentication,
localization and deployment are still open questions on a DevExpress project.

## Owner confirmation

| Input | Key | Required | Value or Path | Evidence | Status |
|---|---|---:|---|---|---|
| Exact versions in use — not a supported range. The .NET target read from the project's own manifests, and the DevExpress release read from its package or assembly references and from the machine that runs validation. | `runtime-sdk-versions` | yes | | | unknown |
| Which documentation source is authoritative for this stack, and which must not be consulted for it. Recorded in mcp/source-routing.md. | `authoritative-sources` | yes | | | unknown |
| What counts as one feature in this codebase, and what a feature may touch. | `feature-model` | yes | | | unknown |
| The exact build, test and lint commands, and what their failure looks like. A command nobody has run is not a validation profile. | `validation-profile` | yes | | | unknown |
| How the DevExpress licence reaches the machine that builds, whether licenses.licx is under source control, and whether the assemblies may be redistributed with the application. | `licensing` | yes | | | unknown |
| Whether this stack's material may appear in a public repository — including form layouts, skin names and screenshots. | `confidentiality` | yes | | | unknown |

## Capability decisions

Each capability below has to resolve to `present`, `absent` or `not-applicable`
with evidence. Until then the Unknown Rule in `capability-detection.md` applies,
and it blocks the dependent work rather than guessing.

| Capability | Decision | Evidence | Status |
|---|---|---|---|
| `devexpress-version` | | | unknown |
| `grid-views` | | | unknown |
| `command-surface` | | | unknown |
| `layout-control` | | | unknown |
| `skins-and-appearance` | | | unknown |
| `license-file` | | | unknown |
| `designer-generated-code` | | | unknown |
| `ui-automation` | | | unknown |

## Automatically detected evidence

| Item | Detection Method | Result | Evidence |
|---|---|---|---|
| Project and package manifests | read from the repository | | |
| DevExpress references and their version | read from the project file and the lock or package files | | |
| Installed DevExpress assemblies | read on the validating machine | | |
| Designer files and the DevExpress types they construct | read from the repository | | |
| `licenses.licx` and whether it is tracked | read from the repository | | |
| Existing tests and build scripts | read from the repository | | |

## Blocking unknowns

- `⟨verification required: every row above⟩`
