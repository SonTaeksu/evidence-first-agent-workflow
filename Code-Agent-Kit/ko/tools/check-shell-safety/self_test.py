# SPDX-License-Identifier: MPL-2.0
"""Self-test: passing fixtures and one deliberately failing fixture per rule.

More cases assert that something is accepted than that something is rejected.
A false positive here would make every script in the repository look broken,
and the operator would stop running the check — which costs more than the
defect it was meant to catch.
"""

from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check_shell_safety.py"
BOM = b"\xef\xbb\xbf"


def _load_tool():
    spec = importlib.util.spec_from_file_location("_shell_safety", TOOL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def verify_rule_table(failures: list[str]) -> None:
    """Check the rule table against the PowerShell that is actually installed.

    This is the root repair for a defect that lay dormant for three releases:
    `New-Item` was listed as fixable with `-LiteralPath`, and `New-Item` has no
    such parameter. The finding was therefore impossible to obey. Six shipped
    files "obeyed" it and threw `A parameter cannot be found that matches
    parameter name 'LiteralPath'` at runtime, including
    `scripts/pre-commit-validate.ps1`, an entry point.

    Reviewing the table cannot catch that — nobody remembers which of thirteen
    cmdlets has which parameter. Asking PowerShell can, and does it every run.

    Both directions are asserted. A cmdlet in the fixable list that lacks the
    parameter is the original defect; a cmdlet in the *unfixable* list that has
    gained one would mean the kit is warning where it could be blocking.

    Without PowerShell the table cannot be verified, and an unverified table must
    not be recorded as verified -- the same stance tools/check-script-parity
    takes. That is a tool error, not a pass.
    """
    module = _load_tool()
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        print("FAIL: rule table unverified — no pwsh or powershell on PATH")
        failures.append("rule table unverified (no PowerShell)")
        return

    fixable = list(module.PS_LITERALPATH_CMDLETS)
    unfixable = sorted(module.PS_NO_LITERALPATH)
    script = (
        "$fixable = @(" + ",".join(f"'{name}'" for name in fixable) + ");"
        "$unfixable = @(" + ",".join(f"'{name}'" for name in unfixable) + ");"
        "foreach ($n in $fixable) {"
        "  $c = Get-Command $n -ErrorAction SilentlyContinue;"
        "  if (-not $c) { \"MISSING-CMDLET $n\"; continue }"
        "  if (-not $c.Parameters.ContainsKey('LiteralPath')) { \"NO-LITERALPATH $n\" } };"
        "foreach ($n in $unfixable) {"
        "  $c = Get-Command $n -ErrorAction SilentlyContinue;"
        "  if (-not $c) { \"MISSING-CMDLET $n\"; continue }"
        "  if ($c.Parameters.ContainsKey('LiteralPath')) { \"HAS-LITERALPATH $n\" } };"
        "'DONE'"
    )
    result = subprocess.run(
        [shell, "-NoProfile", "-NonInteractive", "-Command", script],
        capture_output=True, text=True, check=False,
    )
    output = (result.stdout or "") + (result.stderr or "")
    problems = [line.strip() for line in output.splitlines()
                if line.strip() and line.strip() != "DONE"]
    if result.returncode != 0 or "DONE" not in output:
        print(f"FAIL: rule table could not be queried — {output.strip()[:200]}")
        failures.append("rule table query failed")
        return
    if problems:
        for problem in problems:
            print(f"FAIL: rule table disagrees with PowerShell — {problem}")
        failures.extend(problems)
        return
    print(f"PASS: rule table verified against {shell} "
          f"({len(fixable)} fixable, {len(unfixable)} unfixable)")


def run(root: Path) -> int:
    result = subprocess.run(
        [sys.executable, str(TOOL), "--root", str(root)],
        capture_output=True,
        text=True,
    )
    return result.returncode


def case(label: str, files: dict[str, bytes], expected: int, failures: list[str]) -> None:
    with tempfile.TemporaryDirectory() as temporary:
        root = Path(temporary)
        for name, content in files.items():
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
        code = run(root)
    if code == expected:
        print(f"PASS: {label}")
    else:
        print(f"FAIL: {label} — expected exit {expected}, got {code}")
        failures.append(label)


def main() -> int:
    failures: list[str] = []

    # --- the rule table itself --------------------------------------------
    verify_rule_table(failures)

    # --- accepted ---------------------------------------------------------
    case(
        "ps1 with BOM and -LiteralPath is accepted",
        {"a.ps1": BOM + b'if (Test-Path -LiteralPath $Image) { exit 0 }\n'},
        0, failures,
    )
    case(
        "sh with quoted variables is accepted",
        {"a.sh": b'#!/usr/bin/env bash\ncd "$ROOT"\ncp "$SRC" "$DEST"\n'},
        0, failures,
    )
    case(
        "extensionless git hook without BOM is accepted",
        {"pre-commit": b'#!/usr/bin/env sh\npython3 "$GATE" --staged\n'},
        0, failures,
    )
    case(
        "commented-out unquoted usage is not a finding",
        {"a.sh": b'#!/usr/bin/env bash\n# cd $ROOT is wrong, do not do this\n'},
        0, failures,
    )
    case(
        "-LiteralPath after another switch is still recognised",
        {"a.ps1": BOM + b'Get-Content -Raw -Encoding UTF8 -LiteralPath $File\n'},
        0, failures,
    )
    case(
        "a literal quoted path is not mistaken for a variable",
        {"a.ps1": BOM + b'Test-Path "C:/some path/file.txt"\n'},
        0, failures,
    )
    case(
        "a repository with no scripts at all is clean",
        {"README.md": b"# nothing to check\n"},
        0, failures,
    )

    # --- rejected ---------------------------------------------------------
    case(
        "ps1 without BOM is rejected",
        {"a.ps1": b'Write-Host "\xed\x95\x9c\xea\xb8\x80"\n'},
        2, failures,
    )
    case(
        "sh with a BOM is rejected",
        {"a.sh": BOM + b'#!/usr/bin/env bash\necho hi\n'},
        2, failures,
    )
    case(
        "ps1 path cmdlet without -LiteralPath is rejected",
        {"a.ps1": BOM + b'if (Test-Path $Image) { exit 0 }\n'},
        2, failures,
    )
    case(
        "sh unquoted variable in a path position is rejected",
        {"a.sh": b'#!/usr/bin/env bash\ncd $ROOT\n'},
        2, failures,
    )

    # --- warned, not rejected ---------------------------------------------
    case(
        "New-Item with a variable path warns and does not block",
        {"a.ps1": BOM + b'New-Item -ItemType Directory -Force -Path $Output\n'},
        0, failures,
    )
    case(
        "the .NET replacement for New-Item is not flagged at all",
        {"a.ps1": BOM + b'[void][System.IO.Directory]::CreateDirectory($Output)\n'},
        0, failures,
    )

    print(f"self-test failures: {len(failures)}")
    return 0 if not failures else 2


if __name__ == "__main__":
    raise SystemExit(main())
