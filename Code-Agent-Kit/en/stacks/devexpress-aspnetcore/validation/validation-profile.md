# Validation Profile — DevExpress for ASP.NET Core

## Commands

`⟨verification required: this project's exact commands⟩`

The shape they take in this stack:

- Restore: the project's package restore, **against the feed rather than a warm
  cache**. This stack's first failure in CI is an unauthenticated private feed,
  and only a cold restore finds it.
- Build and test: the project's configured commands. Exit code is the verdict.
- Lint, analyzers and types: whichever are configured; absence is reported, not
  assumed to pass.
- Rendering: for anything touching a component or a report, the build passing is
  not the verdict. See below.

## Pass criterion

The **exit code**, in every case. A success message with a non-zero exit is a
failure, and treating the message as the verdict is the specific mistake this
kit was built to prevent.

## What a green build does not cover here

More than usual, which is why this section exists at all. In this stack the
build is satisfied by:

- a missing reporting service registration — nothing resolves it at compile time;
- client-side assets that are not served — the pages compile either way;
- an unimplemented member of the report storage extension point — it throws when
  reached, not when built;
- a report bound to a field that no longer exists — the binding is not checked
  against the schema.

Each of those is a runtime finding. A change touching any of them needs evidence
from a run, not from a build: the page or report actually rendered, with the run
recorded. `artifact-contract.md` says what counts.

`⟨verification required: how this project produces and records such a run⟩`

## Long-running processes

A development server or a service under test is started and stopped through
`tools/run-managed-service/run_service.py` (or its PowerShell twin), which tracks
the process by PID and start time and stops only that process tree.

Never stop a process by image name. `Get-Process dotnet | Stop-Process` and
`pkill -f dotnet` also kill the MCP servers the agent itself depends on, the
build, and the user's unrelated work.

## Recording a result

Command, exit code, the machine's .NET SDK version, **and the resolved DevExpress
package version**. The second is not optional here: the two move independently,
and without it a result cannot be compared to anything later.
