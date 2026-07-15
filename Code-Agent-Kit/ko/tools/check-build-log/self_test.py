# SPDX-License-Identifier: MPL-2.0
"""Self-test build-log pass and fail behavior."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(log: Path, config: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "check_build_log.py"),
            str(log),
            "--config",
            str(config),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        log = folder / "build.log"
        config = folder / "config.json"
        config.write_text(
            json.dumps(
                {
                    "error_patterns": [r"(?im)^\[Error\]"],
                    "required_success_patterns": [r"BUILD SUCCESS"],
                }
            ),
            encoding="utf-8",
        )

        log.write_text("compile\nBUILD SUCCESS\n", encoding="utf-8")
        assert run(log, config).returncode == 0

        log.write_text("[Error] invalid artifact\n", encoding="utf-8")
        assert run(log, config).returncode == 2

        print("Build-log checker self-test passed.")
        print("Pass path: exit 0")
        print("Failure path: exit 2")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
