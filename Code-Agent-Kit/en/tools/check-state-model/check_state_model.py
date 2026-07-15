# SPDX-License-Identifier: MPL-2.0
"""Validate project routing, feature state, history, and worklog structure."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


PROJECT_MAP_SECTIONS = [
    ("## Features",),
    ("## Architecture State",),
    ("## Environment Capabilities",),
    ("## Shared File Reverse Index",),
]

CURRENT_SECTIONS = [
    ("## Current Behavior",),
    ("## Feature Boundary and Actions", "## Feature Boundary 및 Action"),
    ("## Contracts",),
    ("## Related Files by Role", "## 역할별 Related Files"),
    ("## Shared Dependencies",),
    ("## Environment Capability Decisions",),
    ("## Validation State",),
    ("## Known Issues",),
    ("## Next Candidate Work",),
]

WORKLOG_SECTIONS = [
    ("## 1. Analysis",),
    ("## 2. Task",),
    ("## 3. Todo and Micro-Verify", "## 3. Todo와 Micro-Verify"),
    ("## 4. Checklist",),
    ("## 5. Verification",),
]

FRONT_MATTER_FIELDS = [
    "feature",
    "status",
    "code-verified",
    "last-pr",
    "updated",
    "stack",
]


def front_matter(text: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    return match.group(1) if match else ""


def require_sections(
    label: str,
    text: str,
    sections: list[tuple[str, ...]],
    failures: list[str],
) -> None:
    for alternatives in sections:
        if not any(section in text for section in alternatives):
            failures.append(
                f"{label}: missing section '{alternatives[0]}'"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-docs", required=True, type=Path)
    parser.add_argument(
        "--worklog-template",
        type=Path,
        default=Path("templates/core/worklog.md"),
    )
    args = parser.parse_args()

    try:
        docs = args.project_docs.resolve()
        failures: list[str] = []
        checks: list[str] = []

        project_map = docs / "project-map.md"
        if not project_map.exists():
            failures.append("Missing project-map.md")
        else:
            text = project_map.read_text(encoding="utf-8")
            require_sections(
                "project-map.md",
                text,
                PROJECT_MAP_SECTIONS,
                failures,
            )
            checks.append("project map")

        features = docs / "features"
        current_files = sorted(features.glob("*.current.md"))
        current_files = [
            path for path in current_files
            if not path.name.endswith(".current.ko.md")
        ]
        if not current_files:
            failures.append("No feature current documents found.")

        for current in current_files:
            text = current.read_text(encoding="utf-8")
            fm = front_matter(text)
            if not fm:
                failures.append(f"{current.name}: missing YAML front matter")
            for field in FRONT_MATTER_FIELDS:
                if not re.search(
                    rf"(?m)^{re.escape(field)}\s*:",
                    fm,
                ):
                    failures.append(
                        f"{current.name}: missing front-matter field {field}"
                    )
            require_sections(
                current.name,
                text,
                CURRENT_SECTIONS,
                failures,
            )

            feature_key_match = re.search(r"(?m)^feature\s*:\s*(.+)$", fm)
            if feature_key_match:
                feature_key = feature_key_match.group(1).strip().strip('"')
                history = features / f"{feature_key}.history.md"
                if not history.exists():
                    failures.append(
                        f"{current.name}: missing {history.name}"
                    )
                else:
                    history_text = history.read_text(encoding="utf-8")
                    if not any(
                        marker in history_text[:500]
                        for marker in ("Append-only", "Append-only입니다")
                    ):
                        failures.append(
                            f"{history.name}: append-only rule not declared"
                        )
            checks.append(current.name)

        for area in ("system", "database"):
            current = docs / "architecture" / f"{area}.current.md"
            history = docs / "architecture" / f"{area}.history.md"
            if not current.exists():
                failures.append(f"Missing architecture/{area}.current.md")
            if not history.exists():
                failures.append(f"Missing architecture/{area}.history.md")
            elif not any(
                marker in history.read_text(encoding="utf-8")[:500]
                for marker in ("Append-only", "Append-only입니다")
            ):
                failures.append(
                    f"architecture/{area}.history.md: "
                    "append-only rule not declared"
                )

        worklog_template = args.worklog_template
        if not worklog_template.is_absolute():
            cwd_candidate = Path.cwd() / worklog_template
            if cwd_candidate.exists():
                worklog_template = cwd_candidate
            else:
                repository = docs
                while repository.parent != repository:
                    if (
                        (repository / "DESIGN-CONCEPTS.md").exists()
                        or (repository / "repository-manifest.json").exists()
                    ):
                        break
                    repository = repository.parent
                worklog_template = repository / worklog_template

        text = worklog_template.read_text(encoding="utf-8")
        if "current:" not in front_matter(
            text.replace("```yaml", "---", 1).replace("```", "---", 1)
        ) and "current:" not in text[:500]:
            failures.append("worklog template: missing current path")
        require_sections(
            "worklog template",
            text,
            WORKLOG_SECTIONS,
            failures,
        )

        if failures:
            for failure in failures:
                print(f"FAIL: {failure}", file=sys.stderr)
            return 2

        print(
            "State model validation passed: "
            + ", ".join(checks)
        )
        return 0
    except OSError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
