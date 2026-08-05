# SPDX-License-Identifier: MPL-2.0
"""Validate one installed portable Code Agent Kit language mirror."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

LINK = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
REQUIRED_FILES = {
    # Shared by every tool. A partial copy that omits it leaves each tool dying on
    # `from kit_cli import ...` -- an installation fault reported here, once,
    # rather than as a traceback from whichever tool happened to run first.
    "tools/_lib/kit_cli.py",
    "README.md",
    "AGENTS.md",
    "DESIGN-CONCEPTS.md",
    ".agentignore",
    ".mcp.json",
    ".codex/config.toml",
    ".roo/mcp.json",
    ".roo/rules/10-evidence-first.md",
    ".clinerules/10-evidence-first.md",
    "CLAUDE.md",
    "prompts/GATE.md",
    "prompts/0-sync-and-orient.md",
    "templates/core/worklog.md",
    "templates/core/feature.current.md",
    "templates/core/project-map.md",
    "docs/core/state-and-memory-model.md",
    "docs/getting-started/stack-input-requirements.md",
    "demos/README.md",
    "reference-assets/README.md",
    "tools/check-stack-readiness/check_stack_readiness.py",
    "tools/check-state-model/check_state_model.py",
    "tools/check-kit-selfcheck/check_kit_selfcheck.py",
    "tools/check-mirror-parity/check_mirror_parity.py",
    "tools/check-shell-safety/check_shell_safety.py",
    "tools/check-last/check_last.py",
    "tools/check-script-parity/check_script_parity.py",
    "docs/core/finding-identifiers.md",
    "prompts/7-update-the-kit.md",
    "docs/core/command-and-process-safety.md",
    "docs/core/gate-design-principles.md",
    "scripts/pre-commit-validate.ps1",
    "LICENSES.md",
    "KIT-MANIFEST.json",
}
REQUIRED_DIRS = {
    "docs",
    "prompts",
    "templates",
    "stacks",
    "tools",
    "scripts",
    "demos",
    "reference-assets",
    "agent-configs",
    "LICENSES",
}


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()
    failures: list[str] = []

    for relative in sorted(REQUIRED_FILES):
        path = root / relative
        if not path.is_file():
            failures.append(f"[check-kit-installation:missing-file] required file: {relative}")

    for relative in sorted(REQUIRED_DIRS):
        path = root / relative
        if not path.is_dir():
            failures.append(f"[check-kit-installation:missing-directory] required directory: {relative}")

    for path in root.rglob("*"):
        if path.is_file() and ".ko.md" in path.name:
            failures.append(
                f"[check-kit-installation:language-suffix] {path.relative_to(root)}"
            )

    for path in root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if (
                not target
                or target.startswith(("#", "http://", "https://", "mailto:"))
                or "://" in target
            ):
                continue
            resolved = (path.parent / target).resolve()
            try:
                resolved.relative_to(root)
            except ValueError:
                failures.append(
                    f"{path.relative_to(root)}: [check-kit-installation:link-escapes-root] "
                    f"{raw_target}"
                )
                continue
            if not resolved.exists():
                failures.append(
                    f"{path.relative_to(root)}: [check-kit-installation:missing-link-target] "
                    f"{raw_target}"
                )

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 2

    file_count = sum(1 for path in root.rglob("*") if path.is_file())
    print(f"Kit installation validation passed: {file_count} files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
