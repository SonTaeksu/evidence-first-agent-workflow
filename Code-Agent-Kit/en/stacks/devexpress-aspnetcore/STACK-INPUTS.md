# Stack Inputs — DevExpress for ASP.NET Core

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

This stack has one input the other stacks do not: the DevExpress packages come
from a **private feed that needs credentials**. That is why
`devexpress-package-source` is a required owner input rather than something
detection can settle. A machine with a warm package cache restores happily and
proves nothing about the feed.

## Owner confirmation

| Input | Key | Required | Value or Path | Evidence | Status |
|---|---|---:|---|---|---|
| The exact .NET target framework and SDK, and the exact DevExpress package version — not a supported range. Read from the project file, the restore output, and the toolchain on the machine that runs validation. | `runtime-sdk-versions` | yes | | | unknown |
| Which DevExpress feed this project restores from, where the credential comes from, and whether the build agent has it. A restore that succeeded on a developer machine is not evidence that the feed is configured. | `devexpress-package-source` | yes | | | unknown |
| Which documentation source is authoritative for DevExpress and which for plain ASP.NET Core, and which must not be consulted for either. Recorded in mcp/source-routing.md. | `authoritative-sources` | yes | | | unknown |
| What counts as one feature in this codebase, and what a feature may touch — including whether a report definition belongs to a feature or has its own lifecycle. | `feature-model` | yes | | | unknown |
| The exact build, test and lint commands, and what their failure looks like. A command nobody has run is not a validation profile. | `validation-profile` | yes | | | unknown |
| Whether this stack's material may appear in a public repository. Report definitions carry connection details; licence keys are the other usual leak. | `confidentiality` | yes | | | unknown |

## Capability decisions

Each capability below has to resolve to `present`, `absent` or `not-applicable`
with evidence. Until then the Unknown Rule in `capability-detection.md` applies,
and it blocks the dependent work rather than guessing.

| Capability | Decision | Evidence | Status |
|---|---|---|---|
| `devexpress-version` | | | unknown |
| `ui-component-layer` | | | unknown |
| `page-model` | | | unknown |
| `reporting-host` | | | unknown |
| `report-storage` | | | unknown |
| `client-resource-delivery` | | | unknown |

## Automatically detected evidence

| Item | Detection Method | Result | Evidence |
|---|---|---|---|
| Project files and their package references | read from the repository | | |
| The feed configuration NuGet actually reads | read from the repository and the build agent | | |
| Application startup and service registration | read from the repository | | |
| Views, layouts and the assets they reference | read from the repository | | |
| Report definitions and where they are stored | read from the repository | | |
| Toolchain version | run on the validating machine | | |
| Existing tests and build scripts | read from the repository | | |

## Blocking unknowns

- `⟨verification required: every row above⟩`
