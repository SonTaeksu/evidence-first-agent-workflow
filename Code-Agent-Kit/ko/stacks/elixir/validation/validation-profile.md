# Validation Profile — Elixir

## Commands

`⟨verification required: this project's exact commands⟩`

The shape they take in this stack:

- Compile: `mix compile --warnings-as-errors`. A warning in Elixir is usually a real defect.
- Test: `mix test`. Record the exit code.
- Record `elixir --version` and the OTP release from the validating machine.

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
