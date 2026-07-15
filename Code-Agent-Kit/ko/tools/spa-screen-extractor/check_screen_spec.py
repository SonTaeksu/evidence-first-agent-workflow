# SPDX-License-Identifier: MPL-2.0
"""Compare a reference rendered-screen specification with an implementation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


def normalize(value: str) -> str:
    return re.sub(r"[\s_\-]+", "", value).casefold()


def extract_pages(payload: dict[str, Any]) -> list[dict[str, Any]]:
    pages = payload.get("pages")
    if isinstance(pages, list):
        return pages
    return [payload]


def flatten(payload: dict[str, Any]) -> dict[str, Any]:
    result = {"grids": [], "forms": [], "buttons": [], "visual_blocks": []}
    for page in extract_pages(payload):
        result["grids"].extend(page.get("grids", []))
        result["forms"].extend(page.get("forms", []))
        result["buttons"].extend(page.get("buttons", []))
        result["visual_blocks"].extend(page.get("visual_blocks", []))
    return result


def mapped_id(
    reference_id: str,
    mapping: dict[str, Any],
    section: str,
) -> str:
    section_map = mapping.get(section, {})
    if not isinstance(section_map, dict):
        return reference_id
    return str(section_map.get(reference_id, reference_id))


def select_grid(
    reference: dict[str, Any],
    implementation: list[dict[str, Any]],
    mapping: dict[str, Any],
    index: int,
) -> dict[str, Any] | None:
    expected_id = mapped_id(
        str(reference.get("id", "")),
        mapping,
        "grids",
    )

    for grid in implementation:
        if normalize(str(grid.get("id", ""))) == normalize(expected_id):
            return grid

    if index < len(implementation):
        return implementation[index]
    return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--implementation", required=True, type=Path)
    parser.add_argument("--mapping", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--require-rows", action="store_true")
    parser.add_argument("--strict-controls", action="store_true")
    parser.add_argument("--strict-visual-blocks", action="store_true")
    parser.add_argument("--reject-empty-visual-blocks", action="store_true")
    args = parser.parse_args()

    try:
        reference = flatten(
            json.loads(args.reference.read_text(encoding="utf-8"))
        )
        implementation = flatten(
            json.loads(args.implementation.read_text(encoding="utf-8"))
        )
        mapping = (
            json.loads(args.mapping.read_text(encoding="utf-8"))
            if args.mapping
            else {}
        )

        failures: list[str] = []
        checks: list[dict[str, Any]] = []

        if len(implementation["grids"]) < len(reference["grids"]):
            failures.append(
                "Implementation has fewer grids than the reference "
                f"({len(implementation['grids'])} < {len(reference['grids'])})."
            )

        for index, ref_grid in enumerate(reference["grids"]):
            impl_grid = select_grid(
                ref_grid,
                implementation["grids"],
                mapping,
                index,
            )
            if impl_grid is None:
                failures.append(
                    f"Missing grid: {ref_grid.get('id', index + 1)}"
                )
                continue

            ref_columns = {
                normalize(str(column))
                for column in ref_grid.get("columns", [])
                if str(column).strip()
            }
            impl_columns = {
                normalize(str(column))
                for column in impl_grid.get("columns", [])
                if str(column).strip()
            }
            missing_columns = sorted(ref_columns - impl_columns)

            row_values = impl_grid.get(
                "sample_rows",
                impl_grid.get("rows", []),
            )

            status = "PASS"
            reasons = []
            if missing_columns:
                status = "FAIL"
                reasons.append(
                    "missing columns: " + ", ".join(missing_columns)
                )
            if args.require_rows and not row_values:
                status = "FAIL"
                reasons.append("no sample rows")

            checks.append(
                {
                    "type": "grid",
                    "reference_id": ref_grid.get("id"),
                    "implementation_id": impl_grid.get("id"),
                    "status": status,
                    "reasons": reasons,
                }
            )
            if status == "FAIL":
                failures.append(
                    f"Grid {ref_grid.get('id')}: " + "; ".join(reasons)
                )

        reference_buttons = {
            normalize(str(button))
            for button in reference["buttons"]
            if str(button).strip()
        }
        implementation_buttons = {
            normalize(str(button))
            for button in implementation["buttons"]
            if str(button).strip()
        }
        missing_buttons = sorted(reference_buttons - implementation_buttons)
        if missing_buttons:
            failures.append(
                "Missing buttons or tabs: " + ", ".join(missing_buttons)
            )

        if args.strict_controls:
            reference_controls = {
                normalize(str(control))
                for form in reference["forms"]
                for control in form.get("controls", [])
            }
            implementation_controls = {
                normalize(str(control))
                for form in implementation["forms"]
                for control in form.get("controls", [])
            }
            missing_controls = sorted(
                reference_controls - implementation_controls
            )
            if missing_controls:
                failures.append(
                    "Missing input controls: "
                    + ", ".join(missing_controls)
                )

        if args.strict_visual_blocks or args.reject_empty_visual_blocks:
            implementation_by_id = {
                normalize(str(block.get("id", ""))): block
                for block in implementation["visual_blocks"]
                if str(block.get("id", "")).strip()
            }

            if args.strict_visual_blocks and (
                len(implementation["visual_blocks"])
                < len(reference["visual_blocks"])
            ):
                failures.append(
                    "Implementation has fewer visual blocks than the reference "
                    f"({len(implementation['visual_blocks'])} "
                    f"< {len(reference['visual_blocks'])})."
                )

            for index, reference_block in enumerate(reference["visual_blocks"]):
                reference_id = str(reference_block.get("id", ""))
                expected_id = mapped_id(
                    reference_id,
                    mapping,
                    "visual_blocks",
                )
                implementation_block = implementation_by_id.get(
                    normalize(expected_id)
                )
                if (
                    implementation_block is None
                    and index < len(implementation["visual_blocks"])
                ):
                    implementation_block = implementation["visual_blocks"][index]

                if implementation_block is None:
                    if args.strict_visual_blocks:
                        failures.append(
                            f"Missing visual block: {reference_id or index + 1}"
                        )
                    continue

                reasons = []
                if (
                    args.reject_empty_visual_blocks
                    and not reference_block.get("is_empty", False)
                    and implementation_block.get("is_empty", False)
                ):
                    reasons.append("implemented block is empty")

                reference_type = str(reference_block.get("type", ""))
                implementation_type = str(
                    implementation_block.get("type", "")
                )
                if (
                    args.strict_visual_blocks
                    and reference_type
                    and implementation_type
                    and normalize(reference_type)
                    != normalize(implementation_type)
                ):
                    reasons.append(
                        f"type mismatch: {implementation_type} "
                        f"!= {reference_type}"
                    )

                status = "FAIL" if reasons else "PASS"
                checks.append(
                    {
                        "type": "visual-block",
                        "reference_id": reference_id,
                        "implementation_id": implementation_block.get("id"),
                        "status": status,
                        "reasons": reasons,
                    }
                )
                if reasons:
                    failures.append(
                        f"Visual block {reference_id or index + 1}: "
                        + "; ".join(reasons)
                    )

        report = {
            "schema": "evidence-first/screen-spec-comparison/v1",
            "status": "PASS" if not failures else "FAIL",
            "reference": args.reference.as_posix(),
            "implementation": args.implementation.as_posix(),
            "checks": checks,
            "failures": failures,
        }

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        if failures:
            for failure in failures:
                print(f"FAIL: {failure}", file=sys.stderr)
            return 2

        print("Rendered screen specification comparison passed.")
        return 0
    except (
        OSError,
        ValueError,
        TypeError,
        json.JSONDecodeError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
