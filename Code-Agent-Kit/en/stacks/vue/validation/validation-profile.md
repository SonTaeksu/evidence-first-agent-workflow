# Validation Profile — Vue.js

## Commands

`⟨verification required: this project's exact commands⟩`

The shape they take in this stack:

- Install: the project's lock-file-respecting install. A resolution that changes the lock file is a change, and must be reported.
- Build and test: the configured package scripts. Exit code is the verdict.
- Lint and types: whichever are configured; absence is reported, not assumed to pass.

## Pass criterion

The **exit code**, in every case. A success message with a non-zero exit is a
failure, and treating the message as the verdict is the specific mistake this
kit was built to prevent.

## Long-running processes

A development server or a service under test is started and stopped through
`tools/run-managed-service/run_service.py` (or its PowerShell twin), which tracks
the process by PID and start time and stops only that process tree.

Never stop a process by image name. `Get-Process node | Stop-Process` and
`pkill -f node` also kill the MCP servers the agent itself depends on, and the
user's unrelated work.

## Recording a result

Command, exit code, and the machine's toolchain version. Without the version the
result cannot be compared to anything later.
