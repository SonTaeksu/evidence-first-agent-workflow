# SPDX-License-Identifier: MPL-2.0
"""Compare language mirrors against each other and against their own claims.

Three checks, ordered by how certain the verdict is:

1. Path parity. Every mirror holds the same set of relative paths. A path
   present in one mirror and absent from another is an orphan, and an orphan
   means a link or a documented command is broken in one language.

2. Shared source identity. Files that are not prose are shared verbatim across
   mirrors. Only the documentation is translated, so a difference in a script
   means the mirrors will produce different verdicts on the same input.

3. Counted claims. A manifest that states a file count is checked against a
   measurement. A count whose counting rule is not recorded cannot be checked;
   that is reported as a warning, not a failure, because the claim may be
   correct under a rule the document never wrote down.

Findings are tagged `[check-mirror-parity:<id>]`; see
docs/core/finding-identifiers.md.

Exit codes:
  0  mirrors agree and every checkable claim matches
  2  orphan path, differing shared source, or a claim contradicted by measurement
  1  tool error
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

DEFAULT_MIRRORS = ("en", "ko")

# Not prose. Translated mirrors share these verbatim.
IDENTICAL_SUFFIXES = (".py", ".sh", ".ps1", ".js", ".cs")

MANIFEST = "KIT-MANIFEST.json"
COUNT_KEY = "mirrored_file_count"
RULE_KEY = "mirrored_file_count_rule"

# Build residue. Never part of a mirror, and produced by running any Python
# tool in place, so it is excluded from measurement and reported as a warning
# rather than a failure.
RESIDUE_DIRS = ("__pycache__", ".evidence-first")
RESIDUE_SUFFIXES = (".pyc", ".pyo")

# Locally generated evidence. `.gitignore` already declares these paths as
# generated, and the kit's own scripts write them -- `scripts/pre-commit-validate`
# produces exactly this. Without the exclusion, running the validation the kit
# tells you to run makes the kit's own mirror check report orphan paths, so the
# operator learns that this gate cries wolf. Same shape as a rule that cannot be
# obeyed: the tool must not fail a state its own instructions produce.
RESIDUE_PATH_FRAGMENTS = ("docs/evidence/generated/",)

# Counting rules this tool knows how to measure. A manifest naming a rule that
# is absent here is reported as unverifiable rather than wrong.
RULES = {
    "all-files": lambda paths: len(paths),
}


def is_residue(relative: str) -> bool:
    parts = Path(relative).parts
    if any(part in RESIDUE_DIRS for part in parts):
        return True
    if any(fragment in relative for fragment in RESIDUE_PATH_FRAGMENTS):
        return True
    return Path(relative).suffix.lower() in RESIDUE_SUFFIXES


def relative_paths(root: Path) -> set[str]:
    return {
        relative
        for relative in (
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        )
        if not is_residue(relative)
    }


def residue_paths(root: Path) -> list[str]:
    return sorted(
        relative
        for relative in (
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        )
        if is_residue(relative)
    )


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_paths(roots: dict[str, Path]) -> list[str]:
    names = list(roots)
    sets = {name: relative_paths(roots[name]) for name in names}
    union: set[str] = set()
    for paths in sets.values():
        union |= paths

    failures: list[str] = []
    for relative in sorted(union):
        missing = [name for name in names if relative not in sets[name]]
        if missing and len(missing) < len(names):
            present = [name for name in names if relative in sets[name]]
            failures.append(
                f"[check-mirror-parity:orphan-path] {relative} "
                f"(in {'/'.join(present)}; "
                f"missing from {'/'.join(missing)})"
            )
    return failures


def check_shared_source(
    roots: dict[str, Path], suffixes: tuple[str, ...]
) -> tuple[list[str], int]:
    names = list(roots)
    base = names[0]
    shared = sorted(
        relative
        for relative in relative_paths(roots[base])
        if Path(relative).suffix.lower() in suffixes
    )

    failures: list[str] = []
    compared = 0
    for relative in shared:
        reference = roots[base] / relative
        expected = digest(reference)
        for name in names[1:]:
            other = roots[name] / relative
            if not other.is_file():
                continue  # already reported by the path check
            compared += 1
            if digest(other) != expected:
                failures.append(
                    f"[check-mirror-parity:shared-source-differs] between "
                    f"{base} and {name}: {relative}"
                )
    return failures, compared


def check_claims(roots: dict[str, Path]) -> tuple[list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    for name, root in roots.items():
        manifest_path = root / MANIFEST
        if not manifest_path.is_file():
            continue
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if COUNT_KEY not in manifest:
            continue

        claimed = manifest[COUNT_KEY]
        rule = str(manifest.get(RULE_KEY, "")).strip()
        measured_paths = relative_paths(root)

        if not rule:
            warnings.append(
                f"[check-mirror-parity:count-rule-absent] {name}/{MANIFEST}: "
                f"{COUNT_KEY}={claimed} has no {RULE_KEY}; "
                f"cannot verify (all files measured: {len(measured_paths)})"
            )
            continue
        if rule not in RULES:
            warnings.append(
                f"[check-mirror-parity:count-rule-unknown] {name}/{MANIFEST}: "
                f"unknown {RULE_KEY} '{rule}'; cannot verify"
            )
            continue

        measured = RULES[rule](measured_paths)
        if measured != claimed:
            failures.append(
                f"[check-mirror-parity:count-contradicted] {name}/{MANIFEST}: "
                f"{COUNT_KEY} claims {claimed}, "
                f"rule '{rule}' measures {measured}"
            )
    return failures, warnings


def main() -> int:
    parser = ArgumentParser(
        description="Check language-mirror parity and counted claims."
    )
    parser.add_argument("--root", type=Path, default=Path("."))
    parser.add_argument(
        "--mirror",
        action="append",
        default=[],
        help="Mirror directory name relative to root; repeatable.",
    )
    parser.add_argument(
        "--identical-suffix",
        action="append",
        default=[],
        help="Extra suffix that must be byte-identical across mirrors.",
    )
    args = parser.parse_args()

    try:
        root = args.root.resolve()
        names = args.mirror or list(DEFAULT_MIRRORS)
        roots = {name: root / name for name in names}

        missing = [name for name, path in roots.items() if not path.is_dir()]
        if missing:
            raise OSError(
            "[check-mirror-parity:mirror-missing] mirror directory not found: "
            + ", ".join(missing)
        )
        if len(roots) < 2:
            raise ValueError(
            "[check-mirror-parity:too-few-mirrors] at least two mirrors are "
            "required"
        )

        suffixes = tuple(
            list(IDENTICAL_SUFFIXES)
            + [
                suffix if suffix.startswith(".") else "." + suffix
                for suffix in args.identical_suffix
            ]
        )

        print(f"Mirror parity: {', '.join(names)} under {root}")

        path_failures = check_paths(roots)
        print(f"  paths: {len(relative_paths(roots[names[0]]))} in {names[0]}")

        source_failures, compared = check_shared_source(roots, suffixes)
        print(f"  shared source compared: {compared}")

        claim_failures, warnings = check_claims(roots)

        for name in names:
            residue = residue_paths(roots[name])
            if residue:
                warnings.append(
                    f"[check-mirror-parity:build-residue] {name}: "
                    f"{len(residue)} build residue file(s) present, "
                    f"e.g. {residue[0]}"
                )

        failures = path_failures + source_failures + claim_failures
        for warning in warnings:
            print(f"  WARN  {warning}")
        if failures:
            print(f"  result: BLOCKED ({len(failures)} finding(s))")
            for failure in failures:
                print(f"  FAIL  {failure}", file=sys.stderr)
            return 2
        print(f"  result: CLEAN ({len(warnings)} warning(s))")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
