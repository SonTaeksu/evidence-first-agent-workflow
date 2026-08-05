# SPDX-License-Identifier: MPL-2.0
"""Catch the script defects that only appear on a real developer's machine.

Every finding here is something that passes review, passes on the author's
machine, and breaks on someone else's:

1. A `.ps1` with no UTF-8 BOM. Windows PowerShell 5.1 reads a BOM-less file as
   the system ANSI code page, so non-ASCII literals become mojibake. When a
   non-ASCII string is used in a comparison or a regular expression, the
   *verdict itself* fails, not just the display.

2. A `.sh` or a git hook that has a BOM. The shebang stops being the first
   bytes of the file and the interpreter is not selected.

3. A PowerShell path cmdlet called without `-LiteralPath`. `Test-Path`,
   `Resolve-Path`, `Get-Content`, `Remove-Item` and friends treat `[`, `]`,
   `*` and `?` as wildcards on the positional parameter. A directory named
   `project [old]` silently resolves to nothing.

   `New-Item` is the exception and is **not** in that list: it has no
   `-LiteralPath` parameter at all. It used to be, and the finding was therefore
   unsatisfiable — obeying it produced `A parameter cannot be found that matches
   parameter name 'LiteralPath'`, which is how four twins were broken at once and
   two more shipped broken on their `--output` path. A rule that cannot be
   obeyed is worse than no rule: it teaches the operator that this tool is wrong.
   `New-Item` with a variable path now warns and names the fix that exists.

   The cmdlet/parameter table is **verified against the live PowerShell** by
   `self_test.py`, so a claim about a parameter that does not exist cannot lie
   dormant again.

4. An unquoted shell variable in a path position. `cd $ROOT` breaks the moment
   the checkout lives under a directory with a space in its name, which on
   Windows is the normal case, not the exotic one.

Exit codes:
  0  clean
  2  one or more findings
  1  tool error
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

BOM = b"\xef\xbb\xbf"

SKIP_DIRS = {
    ".git", "node_modules", "bin", "obj", "dist", "coverage",
    "__pycache__", ".venv", "target", "_archive",
}

# PowerShell cmdlets whose positional path parameter globs, and which offer
# `-LiteralPath` as the fix. Every entry is asserted to really have that
# parameter by self_test.py, against the PowerShell actually installed.
PS_LITERALPATH_CMDLETS = (
    "Test-Path", "Resolve-Path", "Get-Content", "Set-Content", "Add-Content",
    "Remove-Item", "Get-Item", "Get-ChildItem", "Copy-Item", "Move-Item",
    "Out-File", "Rename-Item",
)

# Cmdlets that glob but have **no** `-LiteralPath` to offer. Asserted by
# self_test.py to really lack it, so this list cannot silently become wrong in
# the other direction either. The fix is a .NET call, and the message says so.
PS_NO_LITERALPATH = {
    "New-Item": "[System.IO.Directory]::CreateDirectory / [System.IO.File]::WriteAllText",
}

def _call_pattern(names) -> re.Pattern:
    return re.compile(
        r"\b(" + "|".join(names) + r")\b((?:\s+-\w+(?:\s+[^\s|;)]+)?)*)\s+(\$\w+)"
    )

PS_CALL = _call_pattern(PS_LITERALPATH_CMDLETS)
PS_CALL_NO_LITERAL = _call_pattern(PS_NO_LITERALPATH)

# Shell hook / script files without an extension that are still shell.
EXTENSIONLESS_SHELL = {"pre-commit", "pre-push", "commit-msg", "post-merge"}

# `cd $VAR`, `cp $VAR ...` and similar with no quotes around the variable.
SH_UNQUOTED = re.compile(
    r"(?<![\"'])\b(cd|cp|mv|rm|mkdir|source|\.)\s+(-\w+\s+)*(\$\{?\w+\}?)(?![\"'\w])"
)

# Comment lines are not code.
SH_COMMENT = re.compile(r"^\s*#")
PS_COMMENT = re.compile(r"^\s*#")


def iter_files(root: Path):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def check_ps1_bom(path: Path, rel: str) -> list[str]:
    raw = path.read_bytes()
    if raw.startswith(BOM):
        return []
    body = raw.decode("utf-8", errors="replace")
    non_ascii = sum(1 for ch in body if ord(ch) > 127)
    detail = (
        f"{non_ascii} non-ASCII character(s) will be misread as ANSI"
        if non_ascii
        else "no non-ASCII text yet, but the next edit that adds some will break"
    )
    return [f"{rel}:1: [check-shell-safety:ps1-bom] missing UTF-8 BOM — {detail}"]


def check_no_bom(path: Path, rel: str) -> list[str]:
    if path.read_bytes().startswith(BOM):
        return [f"{rel}:1: [check-shell-safety:sh-bom] has a UTF-8 BOM — the shebang is no longer first"]
    return []


def check_ps_literalpath(path: Path, rel: str) -> tuple[list[str], list[str]]:
    """Returns (blocking findings, warnings)."""
    findings: list[str] = []
    warnings: list[str] = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), 1
    ):
        if PS_COMMENT.match(line):
            continue
        for match in PS_CALL.finditer(line):
            cmdlet, switches, variable = match.groups()
            if "-LiteralPath" in (switches or ""):
                continue
            findings.append(
                f"{rel}:{number}: [check-shell-safety:ps-literalpath] {cmdlet} {variable} without "
                f"-LiteralPath — a path containing [ ] * ? resolves to nothing"
            )
        for match in PS_CALL_NO_LITERAL.finditer(line):
            cmdlet, _switches, variable = match.groups()
            # A warning, not a block. The hazard is real but narrower, and there
            # is no switch to add — the fix is a different call, which is a
            # judgement about the surrounding code rather than a mechanical edit.
            warnings.append(
                f"{rel}:{number}: [check-shell-safety:new-item-path] {cmdlet} {variable} globs "
                f"[ ] * ? and has no -LiteralPath — use {PS_NO_LITERALPATH[cmdlet]}"
            )
    return findings, warnings


def check_sh_quoting(path: Path, rel: str) -> list[str]:
    findings = []
    for number, line in enumerate(
        path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
    ):
        if SH_COMMENT.match(line):
            continue
        for match in SH_UNQUOTED.finditer(line):
            command, _switch, variable = match.groups()
            findings.append(
                f"{rel}:{number}: [check-shell-safety:sh-quoting] {command} {variable} unquoted — "
                f'a path with a space splits into two arguments; use "{variable}"'
            )
    return findings


def main() -> int:
    parser = ArgumentParser(
        description="Check script encoding and path-quoting safety."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    args = parser.parse_args()

    try:
        root = args.root.resolve()
        findings: list[str] = []
        warnings: list[str] = []
        counts = {"ps1": 0, "sh": 0}

        for path in iter_files(root):
            rel = path.relative_to(root).as_posix()
            suffix = path.suffix.lower()

            if suffix == ".ps1":
                counts["ps1"] += 1
                findings += check_ps1_bom(path, rel)
                blocking, advisory = check_ps_literalpath(path, rel)
                findings += blocking
                warnings += advisory
            elif suffix == ".sh" or path.name in EXTENSIONLESS_SHELL:
                counts["sh"] += 1
                findings += check_no_bom(path, rel)
                findings += check_sh_quoting(path, rel)

        print(
            f"Shell safety: {counts['ps1']} PowerShell, {counts['sh']} shell "
            f"file(s) under {root}"
        )
        for warning in warnings:
            print(f"  WARN  {warning}")
        if findings:
            print(f"  result: BLOCKED ({len(findings)} finding(s))")
            for finding in findings:
                print(f"  FAIL  {finding}", file=sys.stderr)
            return 2
        print(f"  result: CLEAN ({len(warnings)} warning(s))")
        return 0
    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
