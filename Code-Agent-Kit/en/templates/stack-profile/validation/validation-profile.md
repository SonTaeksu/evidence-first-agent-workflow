# Validation Profile

## Verification commands (mandatory)

Every stack pack MUST fill this in. Each row is a **copy-pasteable** command with an
explicit exit-code / marker pass criterion. Completion (`prompts/GATE.md` §5) is not
reached until these pass — a self-report is not a substitute. Do not trust a summary
line alone; inspect the real error markers or artifacts (a "0 failures" summary can
still hide errors). Keep paths as `{PLACEHOLDERS}` — never commit absolute vendor/SDK
paths (see the sanitization gate).

| Gate | Command (copy-paste) | Pass criterion |
|---|---|---|
| Static / lint | `` | exit 0 |
| Build / compile | `` | exit 0 **and** no error marker in the log |
| Unit / integration | `` | exit 0, all target tests pass |
| Artifact completeness | `` | no empty/placeholder block |

## Long-running processes

Start and stop dev servers, watchers, and any long-running process with the **managed
runner** — never bulk-kill by image name (`Get-Process node | Stop-Process`,
`killall node`, `pkill -f npx`); that also kills the agent's own MCP servers. See
`docs/core/command-and-process-safety.md`. Fill in this stack's run command and port:

```bash
python tools/run-managed-service/run_service.py start --name {svc} --port {PORT} --cwd {dir} -- {this stack's run command}
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name {svc}
```

## Format / lint

-

## Build

-

## Tests

-

## Artifact checks

-
