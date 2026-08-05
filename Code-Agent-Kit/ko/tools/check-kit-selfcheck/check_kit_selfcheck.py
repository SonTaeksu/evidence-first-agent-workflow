# SPDX-License-Identifier: MPL-2.0
"""Run the kit's own seed material through the kit's own validation.

A template or scaffold the kit tells the user to copy must pass the kit's own
checks unmodified. When it does not, the only exit is to bypass the gate.

Two assertions, both chosen so a correct kit produces zero findings:

1. Seed templates. Copy each instructed seed exactly as the kit instructs and
   run the readiness validator. A blank seed is *supposed* to report `blocked`,
   because its inputs are deliberately unknown, so unresolved inputs and
   capabilities are ignored. Only structural failures count: a required
   document that is missing or empty, an array of the wrong type, and a
   declared state that contradicts the derived state.

2. Shipped stacks. Any stack whose manifest declares `ready` must validate as
   ready. A stack that declares a state it cannot reach is a kit defect.

3. The stack table. `stacks/README.md` lists every stack and its status by hand.
   Only the derived columns are compared against the manifests — which
   directories exist, and what each `declared_state` says. Prose is left alone.
   Without this, flipping a `declared_state` leaves the table quietly wrong, and
   the table is what a reader trusts.

## Why this invokes the validator instead of importing it

It used to import the validator as a Python module and classify the returned
failure strings by **prose prefix**. When the validator's messages gained
`[check-stack-readiness:<id>]` identifiers, every one of those prefixes stopped
matching, and assertion 1 became completely inert: deleting a required document
from a seed, or replacing `required_documents` with a string, both reported
CLEAN and exit 0 for three releases. The validator itself caught both.

Two things were wrong, and only one of them was the prose.

Prose is for the person reading; the identifier is the machine contract. A
machine consumer that matches prose dies silently the next time somebody
improves a sentence, and nothing is watching. So classification is by identifier
(see `docs/core/finding-identifiers.md`).

And importing the module was a choice, not a necessity, which bought a
dependency on the validator's internal signature while leaving the CLI layer --
the one every agent, hook and CI job actually runs -- unexercised by anything.
Both implementations now go through the same subprocess and parse the same
identifiers, so this check re-verifies the identifier contract every time it
runs, and the `.ps1` twin has the same shape rather than mirroring a Python
function it cannot call.

Exit codes:
  0  the kit passes its own checks
  2  a seed or a shipped stack is blocked by the kit's own validation
  1  tool error
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

# Seeds the kit instructs the reader to copy. Both entries are documented copy
# sources: `stacks/README.md` and `docs/getting-started/using-another-stack.md`
# name `templates/stack-profile/`, and `docs/core/stack-extension.md` treats
# `stacks/_template/` as the reference layout.
DEFAULT_SEEDS = (
    "templates/stack-profile",
    "stacks/_template",
)

# Findings that indicate a kit defect rather than a deliberate unknown. These
# are identifiers, not sentences, precisely so that rewording the validator's
# messages cannot switch this check off.
STRUCTURAL_IDENTIFIERS = (
    "check-stack-readiness:missing-document",
    "check-stack-readiness:bad-schema",
    "check-stack-readiness:declared-state-mismatch",
)

VALIDATOR = "tools/check-stack-readiness/check_stack_readiness.py"

IDENTIFIER = re.compile(r"\[([a-z0-9][a-z0-9/_-]*:[a-z0-9-]+)\]")
STATE_LINE = re.compile(r"(?mi)^Stack readiness:\s*(\w+)\s*$")


def run_validator(root: Path, stack: Path) -> tuple[str, list[str]]:
    """Invoke the readiness validator and read its verdict off its output."""
    script = root / VALIDATOR
    if not script.is_file():
        raise OSError(
            f"[check-kit-selfcheck:validator-missing] readiness validator not "
            f"found: {VALIDATOR}"
        )
    result = subprocess.run(
        [sys.executable, str(script), "--stack", str(stack)],
        text=True, capture_output=True, check=False,
    )
    text = (result.stdout or "") + (result.stderr or "")
    # The validator failing to run is not the same event as the validator
    # reaching a verdict, and must not be reported as a clean seed.
    if result.returncode == 1:
        raise OSError(
            f"[check-kit-selfcheck:validator-failed] readiness validator could "
            f"not run on {stack}: {text.strip()}"
        )
    match = STATE_LINE.search(text)
    state = match.group(1).lower() if match else ""
    return state, sorted(set(IDENTIFIER.findall(text)))


def read_manifest(stack: Path) -> dict[str, Any]:
    return json.loads(
        (stack / "STACK-READINESS.json").read_text(encoding="utf-8")
    )


def check_seed(root: Path, relative: str) -> tuple[bool, list[str]]:
    source = root / relative
    if not source.is_dir():
        return True, [f"skipped (absent): {relative}"]
    if not (source / "STACK-READINESS.json").is_file():
        return True, [f"skipped (not a stack seed): {relative}"]

    with tempfile.TemporaryDirectory() as temporary:
        copy = Path(temporary) / "seed-stack"
        shutil.copytree(source, copy)
        _state, identifiers = run_validator(root, copy)

    structural = [i for i in identifiers if i in STRUCTURAL_IDENTIFIERS]
    if structural:
        return False, [
            f"[check-kit-selfcheck:seed-structurally-invalid] {relative}: [{i}]"
            for i in structural
        ]
    return True, [f"{relative}: no structural failure"]


def check_shipped_stacks(root: Path) -> tuple[bool, list[str]]:
    stacks = root / "stacks"
    if not stacks.is_dir():
        return True, ["skipped (absent): stacks/"]

    notes: list[str] = []
    ok = True
    for manifest_path in sorted(stacks.glob("*/STACK-READINESS.json")):
        stack = manifest_path.parent
        relative = stack.relative_to(root).as_posix()
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if str(manifest.get("declared_state", "")).strip() != "ready":
            continue
        state, identifiers = run_validator(root, stack)
        if identifiers or state != "ready":
            ok = False
            for identifier in identifiers:
                notes.append(
                    f"[check-kit-selfcheck:declared-ready-not-ready] "
                    f"{relative}: [{identifier}]"
                )
            if not identifiers:
                notes.append(
                    f"[check-kit-selfcheck:declared-ready-not-ready] "
                    f"{relative}: derived state is {state}, not ready"
                )
        else:
            notes.append(f"{relative}: ready")
    if not notes:
        notes.append("no stack declares ready")
    return ok, notes



STACK_TABLE = "stacks/README.md"
TABLE_ROW = re.compile(r"^\|(?P<cells>.+)\|\s*$")
TABLE_DIRECTORY = re.compile(r"`(stacks/[A-Za-z0-9._-]+)`")


def check_stack_table(root: Path) -> tuple[bool, list[str]]:
    """The hand-written table in stacks/README.md against the manifests.

    Only the *derived* columns are compared: which stack directories exist, and
    the `declared_state` each manifest holds. The label and the "owner inputs"
    column are prose written by a person and are left alone.

    Generating the table from the manifests instead was considered. A generator is
    the better shape in principle, but it introduces its own wiring problem — who
    runs it, and when — and an ungenerated table is exactly as stale as an
    unchecked one. This check is already on the CI path, so the comparison takes
    effect immediately. If the table is later generated, this stays: generation
    can fall out of date too, and the comparison is what notices.

    The directory is matched from a backticked `stacks/<name>` cell rather than
    from the prose label, so renaming a label cannot break the check and cannot
    silently disable it either.
    """
    table = root / STACK_TABLE
    if not table.is_file():
        return True, [f"skipped (absent): {STACK_TABLE}"]

    rows: dict[str, str] = {}
    for line in table.read_text(encoding="utf-8").splitlines():
        match = TABLE_ROW.match(line.strip())
        if not match:
            continue
        cells = [cell.strip() for cell in match.group("cells").split("|")]
        directory = next(
            (TABLE_DIRECTORY.search(cell).group(1) for cell in cells
             if TABLE_DIRECTORY.search(cell)), None)
        if directory is None:
            continue
        # The status cell is whichever cell mentions a state word; naming it by
        # position would break the moment a column is added.
        status = " ".join(cells)
        rows[directory] = status

    stacks = root / "stacks"
    manifests = {}
    if stacks.is_dir():
        for manifest_path in sorted(stacks.glob("*/STACK-READINESS.json")):
            relative = f"stacks/{manifest_path.parent.name}"
            if manifest_path.parent.name.startswith("_"):
                continue  # a copy source, not a stack anyone selects
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifests[relative] = str(manifest.get("declared_state", "")).strip()

    notes: list[str] = []
    ok = True
    for relative, declared in manifests.items():
        if relative not in rows:
            ok = False
            notes.append(
                f"[check-kit-selfcheck:stack-table-row-missing] {STACK_TABLE} has "
                f"no row for {relative} (declares '{declared}')")
            continue
        if declared and declared not in rows[relative]:
            ok = False
            notes.append(
                f"[check-kit-selfcheck:stack-table-state-stale] {STACK_TABLE} row "
                f"for {relative} does not mention its declared state "
                f"'{declared}'")
        else:
            notes.append(f"{relative}: table agrees with the manifest")
    for relative in rows:
        if relative not in manifests:
            ok = False
            notes.append(
                f"[check-kit-selfcheck:stack-table-row-orphan] {STACK_TABLE} has "
                f"a row for {relative}, which has no readiness manifest")
    if not notes:
        notes.append(f"{STACK_TABLE}: no stack rows to compare")
    return ok, notes


def main() -> int:
    parser = ArgumentParser(
        description="Run the kit's own seed material through its own checks."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--seed",
        action="append",
        default=[],
        help="Seed directory relative to root; repeatable.",
    )
    args = parser.parse_args()

    try:
        root = args.root.resolve()
        seeds = args.seed or list(DEFAULT_SEEDS)

        failures: list[str] = []
        print(f"Kit self-check: {root}")

        for relative in seeds:
            ok, notes = check_seed(root, relative)
            for note in notes:
                print(f"  {'OK  ' if ok else 'FAIL'}  {note}")
            if not ok:
                failures.extend(notes)

        ok, notes = check_shipped_stacks(root)
        for note in notes:
            print(f"  {'OK  ' if ok else 'FAIL'}  {note}")
        if not ok:
            failures.extend(notes)

        ok, notes = check_stack_table(root)
        for note in notes:
            print(f"  {'OK  ' if ok else 'FAIL'}  {note}")
        if not ok:
            failures.extend(notes)

        if failures:
            print(f"  result: BLOCKED ({len(failures)} finding(s))")
            for failure in failures:
                print(f"  FAIL  {failure}", file=sys.stderr)
            return 2
        print("  result: CLEAN")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
