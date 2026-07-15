# Command and process safety

## Only touch what you started

Record the PID and a cleanup plan for every process you start — dev server, build
watcher, test runner, container. At completion, terminate **only those PIDs**, and
confirm they are actually gone (e.g. the port is free).

## Never bulk-kill by image name

Forbidden — these also kill the MCP servers the agent depends on (context7 and others run
via `npx`/node), plus the user's other editors, servers, and builds:

```
taskkill /F /IM node.exe        # NO
Get-Process node | Stop-Process # NO
killall node                    # NO
pkill -f npx                    # NO
killall dotnet | killall java   # NO
```

## Use the managed runner (the mechanism, not just the rule)

Do not hand-roll PID tracking. Start and stop long-running processes with the managed
runner, which records the PID+port and stops **only that PID's tree**, then verifies:

```bash
python tools/run-managed-service/run_service.py start --name frontend --port 5173 --cwd frontend -- npm run dev
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name frontend   # confirms the port is free
```

If you must stop a stray port by hand, target the **owner PID of that port only** — never
an image name:

```powershell
# Windows: find the PID that owns the port, stop just that PID tree
$pid = (Get-NetTCPConnection -LocalPort 5173 -State Listen).OwningProcess
taskkill /PID $pid /T /F
```

## Ports and shell

Free only the ports you bound; confirm the listener is yours (by PID) first. Confirm the
OS/shell before running a command; do not mix cmd / PowerShell / bash syntax.

## Evidence

Preserve original build/test logs and real exit codes; an unrun check is `PENDING`, not `PASS`.

> Enforcement note: process cleanup is behavioral (not checkable from a commit), so it is
> **ADVISORY**. The managed runner is how you comply without a bulk kill.
