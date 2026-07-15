# SPDX-License-Identifier: MPL-2.0
"""Managed service runner — start/stop/status a dev server by tracked PID+port.

Why: agents must NOT bulk-kill by image name (`Get-Process node | Stop-Process`,
`killall node`, `pkill -f npx`) — that also kills the MCP servers the agent itself
relies on (context7 etc. run via npx/node) and the user's other work. This tool starts
a process, records its PID and port, and stops **only that PID's process tree**, then
verifies the port is actually free. No image-name enumeration, ever.

Usage:
  python run_service.py start  --name frontend --port 5173 --cwd path/to/app -- npm run dev
  python run_service.py status [--name frontend]
  python run_service.py stop   --name frontend

State: .agent-state/services.json (in the repo/project root).
Exit codes: 0 ok; 1 usage/IO error; 2 stop could not confirm the port is free.
"""

from __future__ import annotations

import argparse
import json
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

STATE = Path(".agent-state/services.json")
IS_WIN = os.name == "nt"


def load() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {}
    return {}


def save(data: dict) -> None:
    STATE.parent.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def port_listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.4)
        return s.connect_ex(("127.0.0.1", port)) == 0


def kill_tree(pid: int) -> None:
    """Terminate only this PID and its children — never by image name."""
    if IS_WIN:
        subprocess.run(["taskkill", "/PID", str(pid), "/T", "/F"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    else:
        try:
            os.killpg(os.getpgid(pid), signal.SIGTERM)
            time.sleep(1.0)
            os.killpg(os.getpgid(pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            try:
                os.kill(pid, signal.SIGKILL)
            except OSError:
                pass


def do_start(a) -> int:
    data = load()
    if a.name in data:
        _stop_one(data, a.name)
    kwargs: dict = {"cwd": a.cwd or None}
    if IS_WIN:
        kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP  # type: ignore[attr-defined]
    else:
        kwargs["start_new_session"] = True
    proc = subprocess.Popen(a.command, **kwargs)
    data[a.name] = {"pid": proc.pid, "port": a.port, "cmd": a.command,
                    "cwd": a.cwd or "", "started": time.time()}
    save(data)
    print(f"started '{a.name}' pid={proc.pid} port={a.port} :: {' '.join(a.command)}")
    return 0


def _stop_one(data: dict, name: str) -> int:
    entry = data.get(name)
    if not entry:
        print(f"no tracked service '{name}'")
        return 0
    kill_tree(int(entry["pid"]))
    port = int(entry.get("port") or 0)
    ok = True
    if port:
        for _ in range(10):
            if not port_listening(port):
                break
            time.sleep(0.3)
        else:
            ok = False
    data.pop(name, None)
    save(data)
    if port and not ok:
        print(f"stopped pid {entry['pid']} but port {port} still LISTENING — check manually", file=sys.stderr)
        return 2
    print(f"stopped '{name}' (pid {entry['pid']})" + (f"; port {port} free (confirmed)" if port else ""))
    return 0


def do_stop(a) -> int:
    data = load()
    if a.name:
        return _stop_one(data, a.name)
    rc = 0
    for name in list(data.keys()):
        rc = _stop_one(data, name) or rc
    return rc


def do_status(a) -> int:
    data = load()
    names = [a.name] if a.name else list(data.keys())
    if not names:
        print("no tracked services")
        return 0
    for name in names:
        e = data.get(name)
        if not e:
            print(f"{name}: not tracked")
            continue
        port = int(e.get("port") or 0)
        state = ("LISTENING" if port and port_listening(port) else "free/unknown")
        print(f"{name}: pid={e['pid']} port={port or '-'} -> {state}")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="Managed service runner (PID+port tracked).")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("start"); s.add_argument("--name", required=True)
    s.add_argument("--port", type=int, default=0); s.add_argument("--cwd", default="")
    s.add_argument("command", nargs=argparse.REMAINDER)
    s.set_defaults(fn=do_start)
    t = sub.add_parser("stop"); t.add_argument("--name", default=""); t.set_defaults(fn=do_stop)
    q = sub.add_parser("status"); q.add_argument("--name", default=""); q.set_defaults(fn=do_status)
    a = p.parse_args()
    if a.cmd == "start":
        if a.command and a.command[0] == "--":
            a.command = a.command[1:]
        if not a.command:
            print("start requires: ... -- <command>", file=sys.stderr); return 1
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
