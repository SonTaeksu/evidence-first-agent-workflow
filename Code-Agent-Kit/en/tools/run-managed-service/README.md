# Managed service runner

Start/stop a dev server (or any long-running process) **by tracked PID + port**, so the
agent never has to bulk-kill by image name. Stopping verifies the port is actually free.

```bash
# start (records PID + port in .agent-state/services.json)
python tools/run-managed-service/run_service.py start --name frontend --port 5173 \
  --cwd frontend -- npm run dev

# is it up?
python tools/run-managed-service/run_service.py status

# stop ONLY what this tool started, and confirm the port is free
python tools/run-managed-service/run_service.py stop --name frontend
```

Why this exists: `Get-Process node | Stop-Process`, `killall node`, `pkill -f npx`,
`taskkill /IM node.exe` also kill the MCP servers the agent depends on (context7 and
others run via npx/node) and the user's other work. Never do that. Use this tool, which
kills only the recorded PID's process tree (`taskkill /PID <pid> /T` on Windows, the
process group on POSIX) and then checks the port to confirm the stop.
