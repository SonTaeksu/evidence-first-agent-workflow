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

Ownership: a PID alone does not identify a process. The OS-reported start time
is recorded alongside it, and `stop` compares both before signalling anything. A
reused PID therefore gets a refusal instead of a kill, which is the same rule as
"never bulk-kill by image name" applied to a stale record.

State: .agent-state/services.json (in the repo/project root).
Exit codes: 0 ok; 1 usage/IO error; 2 stop could not confirm the port is free.

Findings are tagged `[run-managed-service:<id>]`; see
docs/core/finding-identifiers.md. The identifiers matter more here than the
wording, because the one thing this tool must never do -- widen a failed lookup
into an image-name sweep -- is only observable from the outside as "it said the
name was not tracked and stopped". `tools/check-script-parity` pins that.

No call site branches on this tool's exit code; every documented invocation is a
command in a stack's validation profile, read by whoever ran it. Recorded because
it means exit 2 is currently advisory in practice.
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

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

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



def process_start_token(pid: int) -> str:
    """An OS-reported identity for a running process, or "" if it is gone.

    This is what makes "is this still *our* process" answerable. Liveness alone is
    not enough: PIDs are reused, so a stale record plus an unlucky reuse means
    this tool signals something it never started -- the exact collateral damage it
    exists to prevent, just smaller and harder to notice than a bulk kill.

    The token is the kernel's own start time, never a timestamp this tool took.
    A timestamp taken here would drift from the kernel's by an unpredictable
    amount and force a tolerance window, and a tolerance window is a hole.

    Sources, in the order they are portable:
      Linux/BSD  /proc/<pid>/stat field 22 -- start time in clock ticks since boot
      Windows    PowerShell's Get-Process StartTime; always present on Windows
    """
    if not IS_WIN:
        try:
            with open(f"/proc/{pid}/stat", "r", encoding="utf-8") as handle:
                content = handle.read()
        except OSError:
            return ""
        # The comm field can contain spaces and parentheses, so split after the
        # last ')' rather than on whitespace from the start.
        tail = content[content.rfind(")") + 1:].split()
        if len(tail) < 20:
            return ""
        return tail[19]  # field 22 overall, 0-based index 19 after comm

    result = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command",
         f"try {{ (Get-Process -Id {pid} -ErrorAction Stop).StartTime.Ticks }} catch {{ '' }}"],
        text=True, capture_output=True, check=False,
    )
    return (result.stdout or "").strip()


def owns(entry: dict, pid: int) -> tuple[bool, str]:
    """Returns (this is our process, why not).

    A record written before ownership tokens existed has no token to compare.
    Refusing on that basis would strand anyone upgrading mid-session, so it is
    accepted with the reason stated -- an explicit, visible gap rather than a
    silent one.
    """
    recorded = str(entry.get("start_token", "") or "")
    if not recorded:
        return True, "record predates ownership tokens; identity unverified"
    current = process_start_token(pid)
    if not current:
        return False, "process is gone"
    if current != recorded:
        return False, f"start token {current} does not match the recorded {recorded}"
    return True, ""


def pid_alive(pid: int) -> bool:
    """Is this PID still there? Asked by PID, never by image name.

    A recorded PID whose process is gone must not be signalled: the number may
    have been reused by something unrelated, and this tool exists precisely so
    that a stale record cannot turn into collateral damage.

    Liveness is necessary but not sufficient; `owns()` answers identity.
    """
    if IS_WIN:
        result = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            text=True, capture_output=True, check=False,
        )
        return str(pid) in (result.stdout or "")
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


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
    # Ask the OS for the child's start time immediately, rather than storing the
    # local clock: the comparison at stop time is then exact, with no tolerance
    # window to be wrong about.
    data[a.name] = {"pid": proc.pid, "port": a.port, "cmd": a.command,
                    "cwd": a.cwd or "", "started": time.time(),
                    "start_token": process_start_token(proc.pid)}
    save(data)
    print(f"started '{a.name}' pid={proc.pid} port={a.port} :: {' '.join(a.command)}")
    return 0


def _stop_one(data: dict, name: str) -> int:
    entry = data.get(name)
    if not entry:
        # The refusal is the feature. There is no fallback that widens this into
        # an image-name sweep, and there must never be one.
        print(
            f"[run-managed-service:untracked-service] no tracked service "
            f"'{name}'; not widening the search"
        )
        return 0
    pid = int(entry["pid"])
    if not pid_alive(pid):
        print(
            f"[run-managed-service:pid-not-alive] tracked pid {pid} for '{name}' "
            f"is gone; nothing signalled"
        )
    else:
        mine, reason = owns(entry, pid)
        if not mine:
            # Refuse, and keep the record. Dropping it would make the next run
            # report "not tracked" and look clean, hiding the fact that something
            # was never stopped. Exit 2 for the same reason the port check uses
            # it: this tool could not confirm it did its job.
            print(
                f"[run-managed-service:pid-owner-mismatch] pid {pid} recorded for "
                f"'{name}' is not the process this tool started ({reason}); "
                f"refusing to signal it. Stop it yourself, or remove the entry "
                f"from .agent-state/services.json.",
                file=sys.stderr,
            )
            return 2
        if reason:
            print(f"[run-managed-service:ownership-unverified] {name}: {reason}")
        kill_tree(pid)
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
        print(f"[run-managed-service:port-still-listening] stopped pid {entry['pid']} but port {port} still LISTENING — check manually", file=sys.stderr)
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
            print(f"[run-managed-service:untracked-service] {name}: not tracked")
            continue
        port = int(e.get("port") or 0)
        state = ("LISTENING" if port and port_listening(port) else "free/unknown")
        print(f"{name}: pid={e['pid']} port={port or '-'} -> {state}")
    return 0


def main() -> int:
    p = ArgumentParser(description="Managed service runner (PID+port tracked).")
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
            print("[run-managed-service:command-missing] start requires: ... -- <command>", file=sys.stderr); return 1
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
