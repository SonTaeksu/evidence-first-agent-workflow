# SPDX-License-Identifier: MPL-2.0
"""Check basic synchronization between code changes and workflow state files."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402


def git(root: Path, *args: str) -> list[str]:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git command failed")
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def git_root(start: Path) -> Path:
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError("Not inside a Git repository.")
    return Path(result.stdout.strip()).resolve()


def changed_files(root: Path, base: str) -> set[str]:
    git(root, "rev-parse", "--verify", base)
    changed = set(git(root, "diff", "--name-only", base, "--"))
    changed.update(git(root, "ls-files", "--others", "--exclude-standard"))
    return {path.replace("\\", "/") for path in changed}


def project_map_paths(project_map: Path) -> set[str]:
    text = project_map.read_text(encoding="utf-8")
    candidates = set(re.findall(r"`([^`]+)`", text))
    return {
        item.replace("\\", "/")
        for item in candidates
        if "/" in item and not item.startswith(("http://", "https://"))
    }


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--base", default="main")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--current", required=True, type=Path)
    parser.add_argument("--history", required=True, type=Path)
    parser.add_argument("--project-map", required=True, type=Path)
    args = parser.parse_args()

    try:
        root = git_root(Path.cwd())
        changed = changed_files(root, args.base)
    except RuntimeError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    scope = args.scope.strip("/")
    scoped = {p for p in changed if p.startswith(scope + "/")}
    code_changed = any(
        p.startswith(f"{scope}/{part}/")
        for p in scoped
        for part in ("frontend", "backend", "scripts")
    )

    state_paths = {
        f"{scope}/{args.current.as_posix()}",
        f"{scope}/{args.history.as_posix()}",
        f"{scope}/{args.project_map.as_posix()}",
    }
    changed_state = state_paths.intersection(scoped)

    errors: list[str] = []

    if code_changed and not changed_state:
        errors.append(
            "[check-document-sync:state-not-updated] code changed but "
            "current/history/project-map did not"
        )

    sample_root = root / scope
    project_map_file = sample_root / args.project_map
    if not project_map_file.exists():
        errors.append(f"[check-document-sync:missing-project-map] {project_map_file}")
    else:
        for item in sorted(project_map_paths(project_map_file)):
            candidate = sample_root / item
            if not candidate.exists():
                errors.append(f"[check-document-sync:project-map-dangling-path] {item}")

    for state in (args.current, args.history):
        if not (sample_root / state).exists():
            errors.append(f"[check-document-sync:missing-state-file] {state}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 2

    print("Document synchronization checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
