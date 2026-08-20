# Stack Inputs — DevExpress WPF (v24.2+)

Nothing in this file is filled in, and that is the current state rather than an
omission. Each row is a fact about *your* project that the kit cannot derive, and
`STACK-READINESS.json` declares `blocked` until they are answered with evidence.

Evidence is **measured**: `check-stack-readiness` resolves each path against the
tree, so a path that does not exist is not evidence.

**This table and `STACK-READINESS.json` must agree.** They are compared, joined on
the `Key` column, and a disagreement is reported. Because that report is a warning,
and a warning derives `provisional`, a stack that declares `ready` while the two
files disagree will fail. Fill in both, or run the interview prompt
(`prompts/8-fill-stack.md`) and let the agent keep them in step.

The plain-WPF inputs are not repeated here. `../csharp-wpf/STACK-INPUTS.md` is a
prerequisite for this stack, not an alternative to it — answer both.

## Owner confirmation

| Input | Key | Required | Value or Path | Evidence | Status |
|---|---|---:|---|---|---|
| Exact versions in use — not a supported range. The .NET target and the DevExpress version the build actually resolves, read from this project's manifests and from the toolchain on the machine that runs validation. | `runtime-sdk-versions` | yes | | | unknown |
| Which documentation source is authoritative for this stack, and which must not be consulted for it. Recorded in mcp/source-routing.md. | `authoritative-sources` | yes | | | unknown |
| Which DevExpress feed the build restores from, how it is authenticated on the build machine, and whether the licence covers this project's use. A build that cannot restore DevExpress packages is not a build, and this is not derivable from the repository. | `devexpress-license-and-feed` | yes | | | unknown |
| What counts as one feature in this codebase, and what a feature may touch. | `feature-model` | yes | | | unknown |
| The exact build, test and lint commands, and what their failure looks like. A command nobody has run is not a validation profile. | `validation-profile` | yes | | | unknown |
| Whether this stack's material may appear in a public repository. DevExpress material is licensed, which makes this a narrower question here than in an open-source stack. | `confidentiality` | yes | | | unknown |

## Capability decisions

Each capability below has to resolve to `present`, `absent` or `not-applicable`
with evidence. Until then the Unknown Rule in `capability-detection.md` applies,
and it blocks the dependent work rather than guessing.

| Capability | Decision | Evidence | Status |
|---|---|---|---|
| `devexpress-version` | | | unknown |
| `mvvm-source` | | | unknown |
| `binding-dialect` | | | unknown |
| `theme-deployment` | | | unknown |
| `grid-view` | | | unknown |
| `docking` | | | unknown |

## Automatically detected evidence

| Item | Detection Method | Result | Evidence |
|---|---|---|---|
| Package or project manifests | read from the repository | | |
| Resolved DevExpress version | read from the build's restore output | | |
| Theme assemblies in the published output | read from the build output, not the project file | | |
| Toolchain version | run on the validating machine | | |
| Existing tests and build scripts | read from the repository | | |

## Blocking unknowns

- `⟨verification required: every row above⟩`
