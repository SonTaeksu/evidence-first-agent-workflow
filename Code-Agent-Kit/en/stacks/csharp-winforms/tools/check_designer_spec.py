# SPDX-License-Identifier: MPL-2.0
"""Compare an extracted designer tree against a declared screen specification.

The specification is written during Gate §1 Analysis from the source asset.
This check answers one question deterministically: does the form actually
contain what the specification said it would.

Verdicts are split by how certain each one is:

  FAIL  a required control is absent, or its type differs from the declaration
  FAIL  the form name differs from the declaration
  WARN  a container control has no children

The empty-container case is a warning, not a failure, because a container may
legitimately be populated at runtime. Blocking it would produce a false
positive on correct code, and one false positive teaches the operator to
bypass the gate.

Exit codes:
  0  the form satisfies the specification
  2  a required control is missing or mistyped
  1  tool error
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check a designer tree against a screen specification."
    )
    parser.add_argument("--tree", required=True, type=Path)
    parser.add_argument("--spec", required=True, type=Path)
    args = parser.parse_args()

    try:
        tree = json.loads(args.tree.read_text(encoding="utf-8"))
        spec = json.loads(args.spec.read_text(encoding="utf-8"))

        controls = {item["name"]: item for item in tree.get("controls", [])}
        failures: list[str] = []
        warnings: list[str] = []

        expected_form = str(spec.get("form", "")).strip()
        if expected_form and expected_form != tree.get("form", ""):
            failures.append(
                f"form is '{tree.get('form', '')}', "
                f"specification declares '{expected_form}'"
            )

        for required in spec.get("required_controls", []):
            name = str(required.get("name", "")).strip()
            if not name:
                failures.append("specification entry has no name")
                continue

            control = controls.get(name)
            if control is None:
                failures.append(f"required control missing: {name}")
                continue

            expected_type = str(required.get("type", "")).strip()
            if expected_type and expected_type not in (
                control["type"],
                control["short_type"],
            ):
                failures.append(
                    f"control {name} is {control['type']}, "
                    f"specification declares {expected_type}"
                )

            expected_parent = str(required.get("parent", "")).strip()
            if expected_parent and expected_parent != control["parent"]:
                failures.append(
                    f"control {name} sits in '{control['parent']}', "
                    f"specification declares '{expected_parent}'"
                )

        for control in tree.get("controls", []):
            if control.get("is_container") and control.get("child_count", 0) == 0:
                warnings.append(
                    f"container {control['name']} "
                    f"({control['short_type']}) has no children"
                )

        print(
            f"Screen specification: {tree.get('form', '?')} "
            f"({len(controls)} control(s) declared in the designer)"
        )
        for warning in warnings:
            print(f"  WARN  {warning}")

        if failures:
            print(f"  result: FAIL ({len(failures)} finding(s))")
            for failure in failures:
                print(f"  FAIL  {failure}", file=sys.stderr)
            return 2

        print(f"  result: PASS ({len(warnings)} warning(s))")
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
