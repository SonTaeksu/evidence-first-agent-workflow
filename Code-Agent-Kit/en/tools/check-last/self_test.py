# SPDX-License-Identifier: MPL-2.0
"""Self-test for the argument-free runner."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check_last.py"
KIT = TOOL.parent.parent.parent
BOM = b"\xef\xbb\xbf"


def copy_shared_library(root: Path) -> None:
    """Copy `tools/_lib` alongside any tool this fixture copies.

    Every tool imports the shared CLI helper. Without it a copied tool dies on
    `from kit_cli import ...` and exits 1 -- a tool error manufactured by the
    fixture, which then looks like a defect in the tool under test.
    """
    target = root / "tools" / "_lib"
    target.mkdir(parents=True, exist_ok=True)
    for source in (KIT / "tools" / "_lib").glob("*.py"):
        shutil.copy(source, target / source.name)


def build(root: Path) -> None:
    """A minimal tree with one real check wired in."""
    copy_shared_library(root)
    (root / "tools" / "check-shell-safety").mkdir(parents=True)
    shutil.copy(
        KIT / "tools/check-shell-safety/check_shell_safety.py",
        root / "tools/check-shell-safety/check_shell_safety.py",
    )
    (root / "scripts").mkdir()
    (root / "scripts" / "ok.ps1").write_bytes(
        BOM + b'Test-Path -LiteralPath $Image\n'
    )


def run(root: Path, *extra: str) -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root), *extra],
        capture_output=True,
        text=True,
    )
    return result.returncode, result.stdout


def check(label: str, condition: bool, failures: list[str]) -> None:
    print(f"{'PASS' if condition else 'FAIL'}: {label}")
    if not condition:
        failures.append(label)


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary) / "repo"
        root.mkdir()
        build(root)

        code, out = run(root)
        check("first run with no baseline is accepted", code == 0, failures)
        check("first run reports it had no baseline", "no baseline yet" in out, failures)

        code, out = run(root)
        check("second run is clean and narrow", code == 0, failures)
        check(
            "second run finds nothing changed",
            "nothing applicable changed" in out or "0 file(s)" in out,
            failures,
        )

        marker = root / ".evidence-first" / "last-check"
        check("baseline marker was created", marker.is_file(), failures)

        # A broken script appears after the baseline.
        time.sleep(1.1)
        bad = root / "scripts" / "bad.ps1"
        bad.write_bytes(b'Test-Path $Image\n')          # no BOM, no -LiteralPath
        os.utime(bad, (time.time(), time.time()))

        code, out = run(root)
        check("a new defect after the baseline is caught", code == 2, failures)

        # Fixing it clears the run.
        time.sleep(1.1)
        bad.write_bytes(BOM + b'Test-Path -LiteralPath $Image\n')
        os.utime(bad, (time.time(), time.time()))
        code, out = run(root)
        check("the fix clears the next run", code == 0, failures)

        code, out = run(root, "--all")
        check("--all still passes on a clean tree", code == 0, failures)

        code, out = run(root, "--mark")
        check("--mark resets and exits 0", code == 0, failures)
        check("--mark says so", "Baseline reset" in out, failures)

        code, out = run(root, "--feature", "does-not-exist")
        check("an unknown feature is a tool error, not a pass", code == 1, failures)

    print(f"self-test failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
