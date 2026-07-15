# SPDX-License-Identifier: MPL-2.0
"""Validate that a stack pack contains required evidence and user decisions."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


RESOLVED = {"confirmed", "detected", "not-applicable"}
ALLOWED = RESOLVED | {"unknown"}
REQUIRED_DEFAULT = [
    "STACK.md",
    "STACK-INPUTS.md",
    "AGENTS.stack.md",
    "SKILL.md",
    "capability-detection.md",
    "feature-model.md",
    "artifact-contract.md",
    "communication-contract.md",
    "evidence-provenance.md",
    "references/_index.md",
    "references/pitfalls.md",
    "references/verified-facts.md",
    "skeletons/README.md",
    "validation/validation-profile.md",
]


def load(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(
    stack: Path,
    manifest: dict[str, Any],
) -> tuple[str, list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []

    required_documents = manifest.get(
        "required_documents",
        REQUIRED_DEFAULT,
    )
    if not isinstance(required_documents, list):
        failures.append("required_documents must be an array.")
        required_documents = []

    for relative in required_documents:
        path = stack / str(relative)
        if not path.exists() or not path.is_file() or path.stat().st_size == 0:
            failures.append(f"Missing or empty required document: {relative}")

    inputs = manifest.get("inputs", [])
    if not isinstance(inputs, list):
        failures.append("inputs must be an array.")
        inputs = []

    for item in inputs:
        key = str(item.get("key", "<missing-key>"))
        status = str(item.get("status", "unknown"))
        required = bool(item.get("required", False))
        evidence = item.get("evidence", [])

        if status not in ALLOWED:
            failures.append(f"Input {key}: invalid status '{status}'.")
            continue

        if required and status not in RESOLVED:
            failures.append(f"Required input unresolved: {key}")

        if status in {"confirmed", "detected"} and not evidence:
            failures.append(
                f"Resolved input has no evidence: {key} ({status})"
            )

        if not required and status == "unknown":
            warnings.append(f"Optional input unresolved: {key}")

    capabilities = manifest.get("capabilities", [])
    if not isinstance(capabilities, list):
        failures.append("capabilities must be an array.")
        capabilities = []

    for item in capabilities:
        key = str(item.get("key", "<missing-key>"))
        status = str(item.get("status", "unknown"))
        evidence = item.get("evidence", [])
        selected_path = str(item.get("selected_path", "")).strip()
        blocks = item.get("blocks", [])

        if status not in {"present", "absent", "unknown", "not-applicable"}:
            failures.append(
                f"Capability {key}: invalid status '{status}'."
            )
            continue

        if status in {"present", "absent"}:
            if not evidence:
                failures.append(f"Capability {key} has no evidence.")
            if not selected_path:
                failures.append(
                    f"Capability {key} has no selected_path."
                )

        if status == "unknown" and blocks:
            failures.append(
                f"Blocking capability unresolved: {key}; blocks={blocks}"
            )
        elif status == "unknown":
            warnings.append(f"Non-blocking capability unresolved: {key}")

    derived = "blocked" if failures else ("provisional" if warnings else "ready")
    declared = str(manifest.get("declared_state", "")).strip()

    if declared and declared != derived:
        failures.append(
            f"declared_state '{declared}' does not match derived state "
            f"'{derived}'."
        )
        derived = "blocked"

    return derived, failures, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stack", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-provisional", action="store_true")
    args = parser.parse_args()

    try:
        stack = args.stack.resolve()
        manifest_path = (
            args.manifest.resolve()
            if args.manifest
            else stack / "STACK-READINESS.json"
        )
        manifest = load(manifest_path)
        state, failures, warnings = validate(stack, manifest)

        report = {
            "schema": "evidence-first/stack-readiness-report/v1",
            "stack": stack.as_posix(),
            "manifest": manifest_path.as_posix(),
            "state": state,
            "failures": failures,
            "warnings": warnings,
        }

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        print(f"Stack readiness: {state.upper()}")
        for warning in warnings:
            print(f"WARN: {warning}")
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)

        if failures:
            return 2
        if state == "provisional" and not args.allow_provisional:
            return 2
        return 0
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
