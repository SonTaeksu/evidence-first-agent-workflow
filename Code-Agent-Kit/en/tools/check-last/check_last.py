# SPDX-License-Identifier: MPL-2.0
"""Run the checks that apply to what changed. No arguments required.

Why this exists, and why it takes no arguments:

Across twelve observed sessions the checks were run essentially zero times.
Not because anyone objected to them — because running one meant first deciding
*which files to pass*, and that decision was itself a step, and that step got
skipped. Removing the decision is the entire point. Every argument this tool
requires is a place it stops being run.

Scope, in order of preference:

  (default)          files modified since the last run of this tool
  --feature <name>   the files listed in that feature's current document
  --all              the whole tree

The marker is a file mtime, not a git commit. Real sessions commit rarely, so a
commit-based baseline drifts to "everything" and the tool becomes slow enough to
avoid. The marker is updated *before* the output is printed, so an interrupted
run still leaves a correct baseline.

Exit codes:
  0  every applicable check passed
  2  at least one check failed
  1  tool error

This is a router, so its own finding is only ever "something it routed to said
no". The routed check's identifiers are propagated with it, which is what makes
the combined output traceable to an actual rule rather than to the router.
Findings are tagged `[check-last:<id>]`; see docs/core/finding-identifiers.md.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

MARKER = Path(".evidence-first") / "last-check"

SKIP_DIRS = {
    ".git", "node_modules", "bin", "obj", "dist", "coverage",
    "__pycache__", ".venv", "target", "_archive", ".evidence-first",
}

SHELL_SUFFIXES = {".ps1", ".sh"}
EXTENSIONLESS_SHELL = {"pre-commit", "pre-push", "commit-msg", "post-merge"}

FEATURE_PATH = re.compile(r"`([^`]+\.[A-Za-z0-9]+)`")


def changed_since(root: Path, since: float) -> list[Path]:
    found = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        try:
            if path.stat().st_mtime > since:
                found.append(path)
        except OSError:
            continue
    return sorted(found)


def all_files(root: Path) -> list[Path]:
    return changed_since(root, 0.0)


def feature_files(root: Path, feature: str) -> list[Path]:
    """Read the paths a feature's current document names in backticks."""
    candidates = list((root / "docs").rglob(f"{feature}.current.md"))
    if not candidates:
        raise ValueError(
            f"[check-last:feature-document-missing] no current document found "
            f"for feature '{feature}'"
        )
    found = []
    for document in candidates:
        for match in FEATURE_PATH.finditer(document.read_text(encoding="utf-8")):
            candidate = root / match.group(1)
            if candidate.is_file():
                found.append(candidate)
    return sorted(set(found))


def is_shell(path: Path) -> bool:
    return path.suffix.lower() in SHELL_SUFFIXES or path.name in EXTENSIONLESS_SHELL


def declared_state(stack: Path) -> str:
    try:
        manifest = json.loads(
            (stack / "STACK-READINESS.json").read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return ""
    return str(manifest.get("declared_state", "")).strip()


def touched_stacks(root: Path, files: list[Path]) -> list[Path]:
    stacks = set()
    for path in files:
        try:
            parts = path.relative_to(root).parts
        except ValueError:
            continue
        if len(parts) >= 2 and parts[0] == "stacks" and parts[1] != "_template":
            stack = root / "stacks" / parts[1]
            if (stack / "STACK-READINESS.json").is_file():
                stacks.add(stack)
    return sorted(stacks)


def run(label: str, command: list[str]) -> tuple[str, int]:
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
    return label, result.returncode


def plan(root: Path, files: list[Path], everything: bool) -> list[tuple[str, list[str]]]:
    """Route the changed set to the checks that can judge it."""
    tools = root / "tools"
    jobs: list[tuple[str, list[str]]] = []

    def tool(relative: str) -> Path:
        return tools / relative

    if everything or any(is_shell(path) for path in files):
        script = tool("check-shell-safety/check_shell_safety.py")
        if script.is_file():
            jobs.append(("shell safety", [sys.executable, str(script), "--root", str(root)]))

    state_touched = everything or any(
        "docs" in path.relative_to(root).parts[:1] for path in files
    )
    script = tool("check-state-model/check_state_model.py")
    # Only when this tree is a *project* using the kit. A kit mirror also has a
    # `docs/` directory, but it holds kit documentation, not project state —
    # judging it as project state is a false positive on a correct tree.
    if state_touched and script.is_file() and (root / "docs" / "project-map.md").is_file():
        jobs.append(
            ("state model", [sys.executable, str(script), "--project-docs", str(root / "docs")])
        )

    script = tool("check-stack-readiness/check_stack_readiness.py")
    if script.is_file():
        stacks = (
            sorted(p.parent for p in (root / "stacks").glob("*/STACK-READINESS.json"))
            if everything and (root / "stacks").is_dir()
            else touched_stacks(root, files)
        )
        for stack in stacks:
            # A stack that declares `blocked` is *supposed* to validate as
            # blocked — its owner inputs are deliberately unresolved. Counting
            # that as a failure would flag every placeholder in the tree, and
            # one false alarm is enough for the operator to stop running this.
            if declared_state(stack) == "blocked":
                continue
            jobs.append(
                (
                    f"stack readiness: {stack.name}",
                    [sys.executable, str(script), "--stack", str(stack), "--allow-provisional"],
                )
            )

    return jobs


def main() -> int:
    parser = ArgumentParser(
        description="Run the checks that apply to what changed. No arguments needed."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument("--all", action="store_true", help="check the whole tree")
    parser.add_argument("--feature", help="check the files this feature's current document names")
    parser.add_argument("--mark", action="store_true", help="reset the baseline and do nothing else")
    args = parser.parse_args()

    try:
        root = args.root.resolve()
        marker = root / MARKER
        marker.parent.mkdir(parents=True, exist_ok=True)

        if args.mark:
            marker.write_text(f"{time.time()}\n", encoding="utf-8")
            print(f"Baseline reset: {MARKER.as_posix()}")
            return 0

        if args.all:
            files, scope = all_files(root), "whole tree"
        elif args.feature:
            files, scope = feature_files(root, args.feature), f"feature '{args.feature}'"
        elif marker.is_file():
            since = marker.stat().st_mtime
            files, scope = changed_since(root, since), "changed since the last run"
        else:
            files, scope = all_files(root), "whole tree (no baseline yet)"

        # Update the baseline before printing: an interrupted run must still
        # leave a correct marker, or the next run silently re-checks the world.
        marker.write_text(f"{time.time()}\n", encoding="utf-8")

        jobs = plan(root, files, everything=bool(args.all))
        print(f"check-last: {len(files)} file(s), scope = {scope}")

        if not jobs:
            print("  nothing applicable changed")
            print("  result: CLEAN")
            return 0

        failures = []
        for label, command in jobs:
            name, code = run(label, command)
            if code == 0:
                print(f"  OK    {name}")
            else:
                print(f"  FAIL  [check-last:routed-check-failed] {name}")
                failures.append(name)

        if failures:
            print(f"  result: BLOCKED ({len(failures)} check(s) failed)")
            return 2
        print("  result: CLEAN")
        return 0
    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
