# SPDX-License-Identifier: MPL-2.0
"""Self-test for the managed service runner, on both implementations.

Everything that can be checked without touching the operating system is checked
by `tools/check-script-parity`, whose fixtures deliberately start no process and
bind no port: a harness that competes for ports becomes flaky, and a flaky
harness is one people learn to ignore.

That leaves two things a fixture cannot reach, and they are the two that matter
most, so they are exercised here against a real kernel:

1. **The full start → stop → gone cycle.** No port, so nothing to contend for.
   This is the only place the tool is proven to actually stop what it started.

2. **Exit 2, "the port is still listening".** Left unproven, an exit code gets
   mis-wired — there is a case on record where a check's `2` meaning "no manifest
   here, this is only advice" and its `1` meaning "this is forged" were treated
   alike by the runner, and correct commits were refused outright. So: this test
   holds the port open itself, records a service whose PID is already gone, and
   asserts the tool reports `2` rather than claiming success. The listener is
   bound on an ephemeral port the OS hands out, so it cannot collide.

Both twins run. Without PowerShell the twin is unverified, and an unverified twin
recorded as verified is worse than one recorded as unverified — the same stance
`check-script-parity` takes — so that is a tool error, not a pass.

Exit codes:
  0  every assertion held on every available implementation
  2  an assertion failed
  1  tool error, including no PowerShell available
"""

from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = HERE / "run_service.py"
PS1 = HERE / "run_service.ps1"
STATE = Path(".agent-state") / "services.json"


def implementations() -> list[tuple[str, list[str], str]]:
    """(label, argv prefix, how the command to start is passed).

    The two differ here, by necessity rather than by oversight. `pwsh -File
    script.ps1 start --name x -- python -c ...` does not work: PowerShell's own
    binder consumes the `--`, then matches `-c` against -Command/-Cwd and rejects
    it as ambiguous. Any dev-server command with a flag in it -- `dotnet run
    --project x` -- hits the same wall, so this is not an artefact of the test.

    The twin therefore takes `-CommandArgs a,b,c`, where the binder sees one token
    and the dashes arrive as values. Deliberately exercised with a command that
    *does* contain a flag, because a dash-free command would pass either way and
    prove nothing.
    """
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return []
    return [
        (".py", [sys.executable, str(PY)], "separator"),
        (".ps1", [shell, "-NoProfile", "-NonInteractive", "-File", str(PS1)], "command-args"),
    ]


def run(base: list[str], argv: list[str], cwd: Path) -> tuple[int, str]:
    result = subprocess.run(base + argv, cwd=cwd, text=True,
                            capture_output=True, check=False)
    return result.returncode, (result.stdout or "") + (result.stderr or "")


def check(label: str, condition: bool, detail: str, failures: list[str]) -> None:
    if condition:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label} — {detail}")
        failures.append(label)


def sleeper() -> list[str]:
    """A child that lives long enough to be stopped, on either platform.

    `python -c` rather than `sleep`: it exists wherever this test can run, and it
    is the same command for both implementations, so neither gets an easier job.
    """
    return [sys.executable, "-c", "import time; time.sleep(30)"]


def test_lifecycle(name: str, base: list[str], style: str,
                   failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        if style == "separator":
            argv = ["start", "--name", "svc", "--", *sleeper()]
        else:
            argv = ["start", "--name", "svc", "-CommandArgs", ",".join(sleeper())]
        code, output = run(base, argv, root)
        check(f"{name}: start reports success", code == 0, f"exit {code}: {output}", failures)

        state_path = root / STATE
        if not state_path.is_file():
            check(f"{name}: start records state", False, "no services.json", failures)
            return
        entry = json.loads(state_path.read_text(encoding="utf-8")).get("svc", {})
        pid = int(entry.get("pid", 0))
        check(f"{name}: start records a pid", pid > 0, f"entry {entry}", failures)
        check(f"{name}: start records an ownership token",
              bool(str(entry.get("start_token", ""))),
              "start_token empty — a reused pid would be indistinguishable",
              failures)

        code, output = run(base, ["status"], root)
        check(f"{name}: status reports the tracked service",
              code == 0 and "svc" in output, f"exit {code}: {output}", failures)

        code, output = run(base, ["stop", "--name", "svc"], root)
        check(f"{name}: stop reports success", code == 0, f"exit {code}: {output}", failures)

        # The point of the whole tool: the process is actually gone, and it went
        # away because this PID was signalled, not because an image name was swept.
        gone = False
        for _ in range(20):
            if not pid_alive(pid):
                gone = True
                break
            time.sleep(0.1)
        check(f"{name}: the process it started is gone", gone,
              f"pid {pid} still alive after stop", failures)

        remaining = json.loads((root / STATE).read_text(encoding="utf-8"))
        check(f"{name}: stop removes the record", "svc" not in remaining,
              f"state still {remaining}", failures)


def pid_alive(pid: int) -> bool:
    if os.name == "nt":
        result = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"],
                                text=True, capture_output=True, check=False)
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


def test_port_still_listening(name: str, base: list[str], failures: list[str]) -> None:
    """Exit 2: stop ran, but the port did not come free.

    Constructed rather than provoked. The listener is this test's own socket on an
    OS-assigned ephemeral port, and the recorded PID is one that is already gone,
    so `stop` has nothing to kill and the port stays up no matter what it does.
    That isolates the port assertion from the killing entirely.
    """
    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    port = listener.getsockname()[1]
    listener.listen(16)

    # The listener has to actually accept, and this is not a detail. The tool
    # probes the port up to ten times and stops at the first probe that fails. A
    # bound-but-never-accepting socket fills its backlog after a few probes, the
    # next probe times out, and the tool correctly concludes "free" -- so the test
    # would have reported a bug in the tool that was really a bug in the fixture.
    # It did, on the first run.
    stop = threading.Event()

    def accept_loop() -> None:
        listener.settimeout(0.2)
        while not stop.is_set():
            try:
                connection, _ = listener.accept()
            except (OSError, socket.timeout):
                continue
            connection.close()

    accepter = threading.Thread(target=accept_loop, daemon=True)
    accepter.start()
    try:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".agent-state").mkdir(parents=True)
            (root / STATE).write_text(json.dumps({
                "svc": {"pid": 999999999, "port": port, "cmd": ["x"],
                        "cwd": "", "started": 1.0}
            }) + "\n", encoding="utf-8")
            code, output = run(base, ["stop", "--name", "svc"], root)
            check(f"{name}: a port that stays listening is exit 2, not success",
                  code == 2, f"exit {code}: {output}", failures)
            check(f"{name}: and it says which port by identifier",
                  "run-managed-service:port-still-listening" in output,
                  f"output was: {output}", failures)
    finally:
        stop.set()
        accepter.join(timeout=2)
        listener.close()


def main() -> int:
    failures: list[str] = []
    available = implementations()
    if not available:
        print("FAIL: no pwsh or powershell on PATH — the twin cannot be verified, "
              "and an unverified twin must not be recorded as verified",
              file=sys.stderr)
        return 1

    for name, base, style in available:
        test_lifecycle(name, base, style, failures)
        test_port_still_listening(name, base, failures)

    print(f"self-test failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
