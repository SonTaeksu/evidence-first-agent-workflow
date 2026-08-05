# SPDX-License-Identifier: MPL-2.0
"""Scan a build or generator log using explicit error and success patterns."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402


DEFAULT_ERRORS = [
    r"(?im)^\s*(?:error|fatal)\b",
    r"(?i)\bbuild failed\b",
    r"(?i)\bgeneration failed\b",
    r"(?i)\bcompilation failed\b",
]


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("log", type=Path)
    parser.add_argument("--config", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        text = args.log.read_text(encoding="utf-8", errors="replace")
        config = (
            json.loads(args.config.read_text(encoding="utf-8"))
            if args.config
            else {}
        )
        error_patterns = config.get("error_patterns", DEFAULT_ERRORS)
        ignore_patterns = config.get("ignore_patterns", [])
        required_success = config.get("required_success_patterns", [])

        filtered = text
        for pattern in ignore_patterns:
            filtered = re.sub(pattern, "", filtered)

        errors = []
        for pattern in error_patterns:
            matches = re.findall(pattern, filtered)
            if matches:
                errors.append({"pattern": pattern, "matches": len(matches)})

        missing_success = [
            pattern
            for pattern in required_success
            if not re.search(pattern, filtered)
        ]

        status = "PASS" if not errors and not missing_success else "FAIL"
        report = {
            "schema": "evidence-first/build-log-check/v1",
            "status": status,
            "log": args.log.as_posix(),
            "errors": errors,
            "missing_success_patterns": missing_success,
        }

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        print(f"Build log check: {status}")
        for item in errors:
            print(
                f"[check-build-log:error-pattern-matched] {item['pattern']} "
                f"({item['matches']} matches)",
                file=sys.stderr,
            )
        for pattern in missing_success:
            print(f"[check-build-log:missing-success-pattern] {pattern}", file=sys.stderr)

        return 0 if status == "PASS" else 2
    except (OSError, TypeError, json.JSONDecodeError, re.error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
