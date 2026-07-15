#!/usr/bin/env python3
"""Install one portable language mirror into a target repository."""
from __future__ import annotations
import argparse, filecmp, json, shutil, subprocess, sys
from pathlib import Path

EXCLUDE_ALWAYS = {"install-kit.py", "install-kit.ps1", "install-kit.sh"}
CORE_EXCLUDE_PREFIXES = (
    "samples/",
    "stacks/go-htmx/",
    "stacks/rust/",
    "stacks/elixir/",
)

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument("--mode", choices=["full", "core"], default="full")
    parser.add_argument("--stack", default="_template")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()

    source = Path(__file__).resolve().parent
    target = args.target.resolve()
    target.mkdir(parents=True, exist_ok=True)
    copied = skipped = conflicts = 0

    for path in sorted(source.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(source).as_posix()
        if rel in EXCLUDE_ALWAYS:
            continue
        if args.mode == "core":
            if rel.startswith("samples/"):
                continue
            if rel.startswith("stacks/") and not (
                rel.startswith("stacks/_template/")
                or rel.startswith(f"stacks/{args.stack}/")
                or rel in {"stacks/README.md"}
            ):
                continue
        dest = target / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            try:
                same = filecmp.cmp(path, dest, shallow=False)
            except OSError:
                same = False
            if same:
                skipped += 1
                continue
            if not args.overwrite:
                print(f"CONFLICT: {rel}")
                conflicts += 1
                continue
        shutil.copy2(path, dest)
        copied += 1

    print(f"Copied: {copied}; unchanged: {skipped}; conflicts: {conflicts}")
    if conflicts:
        print("Re-run with --overwrite after reviewing conflicts.")
        return 2

    if not args.no_validate:
        validator = target / "tools/check-kit-installation/check_kit_installation.py"
        result = subprocess.run(
            [sys.executable, str(validator), "--root", str(target)],
            text=True,
            check=False,
        )
        if result.returncode != 0:
            return result.returncode
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
