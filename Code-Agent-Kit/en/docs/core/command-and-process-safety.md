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

## Ports

Free only the ports you bound; confirm the listener is yours (by PID) first.

## Shell and paths

Confirm the OS and shell **before** the first command, and record the answer in the
project map so the next session does not rediscover it. Do not mix cmd / PowerShell /
bash syntax.

### The separator is opposite between the two Windows shells

```powershell
cd app; npm run build          # PowerShell 5.1 — && is a syntax error
```
```bat
cd app && npm run build        REM cmd — ; is not a separator
```

In cmd, `cd` consumes the **rest of the line** as the path, so anything after it on the
same line is swallowed.

### Prefer not to change directory at all

Every tool worth using takes the directory as an argument. Using it removes an entire
class of failure:

```bash
git -C "$ROOT" status
mvn -f "$ROOT/backend/pom.xml" test
npm --prefix "$ROOT/frontend" run build
python "$ROOT/tools/check-state-model/check_state_model.py" --project-docs "$DOCS"
```

### Always quote a path, because it will contain a space

A checkout under `C:\Users\Name\My Projects\app` is the normal case on Windows, not the
exotic one. Unquoted, it splits into two arguments and the command reads a path that does
not exist — usually reporting something misleading rather than "you forgot a quote".

```bash
cd $ROOT            # NO  — breaks on the first space
cd "$ROOT"          # yes
cp $SRC $DEST       # NO
cp "$SRC" "$DEST"   # yes
```

In PowerShell the failure is quieter and worse. `Test-Path`, `Resolve-Path`,
`Get-Content`, `Remove-Item`, `New-Item` and their relatives treat `[`, `]`, `*` and `?`
as **wildcards** on the positional path parameter. A directory called `project [old]`
does not error — it matches nothing, and the script proceeds as though the file were
absent:

```powershell
Test-Path $Image                      # NO  — globs
Test-Path -LiteralPath $Image         # yes
Get-Content -Raw -LiteralPath $File   # yes
```

### A `.ps1` needs a UTF-8 BOM; a `.sh` must not have one

Windows PowerShell 5.1 reads a BOM-less file as the system ANSI code page. Non-ASCII
literals become mojibake, and when one of them is used in a comparison or a regular
expression the **verdict itself fails**, not just the display. A shell script or git hook
with a BOM loses its shebang, because those bytes are no longer first.

Preserve this through copying and deployment — a resource filter, an encoding conversion,
or a line-ending normalisation will strip it silently.

### Long external commands go in a file

When a command needs four absolute paths, two of which contain spaces and live under
different roots, it will be retyped wrong. Put it in a `.bat` or `.sh` wrapper, generate
that wrapper once per machine, add it to `.gitignore`, and fix the log filename so the
check always knows which file to read.

> Enforced by `tools/check-shell-safety`: `.ps1` BOM, absence of a BOM on `.sh` and
> hooks, missing `-LiteralPath`, and unquoted shell variables in path positions. Exit 2
> on a finding. Choosing not to change directory is advice; the rest is checked.

## Evidence

Preserve original build/test logs and real exit codes; an unrun check is `PENDING`, not `PASS`.

> Enforcement note: process cleanup is behavioral (not checkable from a commit), so it is
> **ADVISORY**. The managed runner is how you comply without a bulk kill.
