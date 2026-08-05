# SPDX-License-Identifier: MPL-2.0
"""Self-test: one passing fixture and three deliberately failing fixtures."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check_mirror_parity.py"


def build(root: Path, count: int | None, rule: str | None) -> None:
    for name in ("en", "ko"):
        mirror = root / name
        (mirror / "docs").mkdir(parents=True)
        (mirror / "tools").mkdir(parents=True)
        (mirror / "docs" / "guide.md").write_text(
            "# Guide\n" if name == "en" else "# 안내\n", encoding="utf-8"
        )
        (mirror / "tools" / "run.py").write_text("print(1)\n", encoding="utf-8")
        manifest: dict[str, object] = {"schema": "fixture/v1"}
        if count is not None:
            manifest["mirrored_file_count"] = count
        if rule is not None:
            manifest["mirrored_file_count_rule"] = rule
        (mirror / "KIT-MANIFEST.json").write_text(
            json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
        )


def run(root: Path) -> int:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True,
        text=True,
    )
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def case(label: str, root: Path, expected: int, failures: list[str]) -> None:
    code = run(root)
    if code != expected:
        print(f"FAIL: {label} expected exit {expected}, got {code}")
        failures.append(label)
    else:
        print(f"PASS: {label} (exit {expected})")


def main() -> int:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)

        clean = base / "clean"
        build(clean, count=3, rule="all-files")
        case("matched mirrors and matched count", clean, 0, failures)

        residue = base / "residue"
        build(residue, count=3, rule="all-files")
        cache = residue / "en" / "tools" / "__pycache__"
        cache.mkdir()
        (cache / "run.cpython-312.pyc").write_bytes(b"\x00")
        case("build residue is excluded and warned", residue, 0, failures)

        orphan = base / "orphan"
        build(orphan, count=3, rule="all-files")
        (orphan / "en" / "docs" / "extra.md").write_text("x\n", encoding="utf-8")
        case("orphan path", orphan, 2, failures)

        drift = base / "drift"
        build(drift, count=3, rule="all-files")
        (drift / "ko" / "tools" / "run.py").write_text(
            "print(2)\n", encoding="utf-8"
        )
        case("shared source differs", drift, 2, failures)

        wrong = base / "wrong"
        build(wrong, count=99, rule="all-files")
        case("count contradicted by measurement", wrong, 2, failures)

        unruled = base / "unruled"
        build(unruled, count=99, rule=None)
        case("count without a recorded rule warns only", unruled, 0, failures)

    print(f"self-test failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
