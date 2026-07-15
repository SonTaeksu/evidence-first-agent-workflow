# SPDX-License-Identifier: MPL-2.0
"""Run a command, record deterministic evidence, and propagate its exit code."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--cwd", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = args.command
    if command and command[0] == "--":
        command = command[1:]

    if not command:
        print("ERROR: command is required after --", file=sys.stderr)
        return 1

    original_command = command.copy()
    resolved_executable = shutil.which(command[0])
    if resolved_executable:
        command[0] = resolved_executable

    started = dt.datetime.now(dt.timezone.utc)
    result = subprocess.run(
        command,
        cwd=args.cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        shell=False,
    )
    finished = dt.datetime.now(dt.timezone.utc)

    output = result.stdout or ""
    output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output)
    status = "PASS" if result.returncode == 0 else "FAIL"

    args.output.parent.mkdir(parents=True, exist_ok=True)
    markdown = f"""# Validation Evidence: {args.name}

- Status: **{status}**
- Started: `{started.isoformat()}`
- Finished: `{finished.isoformat()}`
- Working directory: `{args.cwd.resolve()}`
- Command: `{' '.join(command)}`
- Exit code: `{result.returncode}`

## Output

````text
{output.rstrip()}
````
"""
    args.output.write_text(markdown, encoding="utf-8")

    json_path = args.output.with_suffix(".json")
    json_path.write_text(
        json.dumps(
            {
                "name": args.name,
                "status": status,
                "started": started.isoformat(),
                "finished": finished.isoformat(),
                "cwd": args.cwd.as_posix(),
                "command": original_command,
                "exit_code": result.returncode,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(output, end="")
    print(f"\nEvidence: {args.output}")
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
