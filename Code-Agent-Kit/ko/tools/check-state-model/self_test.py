# SPDX-License-Identifier: MPL-2.0
"""Self-test state-model pass and fail behavior."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(docs: Path, worklog: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "check_state_model.py"),
            "--project-docs",
            str(docs),
            "--worklog-template",
            str(worklog),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        base = Path(temporary)
        docs = base / "docs"
        features = docs / "features"
        architecture = docs / "architecture"
        features.mkdir(parents=True)
        architecture.mkdir()

        (docs / "project-map.md").write_text(
            "\n".join(
                [
                    "# Map",
                    "## Features",
                    "## Architecture State",
                    "## Environment Capabilities",
                    "## Shared File Reverse Index",
                ]
            ),
            encoding="utf-8",
        )
        (features / "example.current.md").write_text(
            """---
feature: example
status: stable
code-verified: x
last-pr: none
updated: x
stack: test
---
## Current Behavior
## Feature Boundary and Actions
## Contracts
## Related Files by Role
## Shared Dependencies
## Environment Capability Decisions
## Validation State
## Known Issues
## Next Candidate Work
""",
            encoding="utf-8",
        )
        (features / "example.history.md").write_text(
            "# History\n\n> Append-only.\n",
            encoding="utf-8",
        )
        for area in ("system", "database"):
            (architecture / f"{area}.current.md").write_text(
                "# Current\n",
                encoding="utf-8",
            )
            (architecture / f"{area}.history.md").write_text(
                "# History\n\n> Append-only.\n",
                encoding="utf-8",
            )

        worklog = base / "worklog.md"
        worklog.write_text(
            """```yaml
current: docs/features/example.current.md
```
## 1. Analysis
## 2. Task
## 3. Todo and Micro-Verify
## 4. Checklist
## 5. Verification
""",
            encoding="utf-8",
        )

        passing = run(docs, worklog)
        assert passing.returncode == 0, passing.stdout + passing.stderr

        (features / "example.history.md").write_text(
            "# History\n",
            encoding="utf-8",
        )
        failing = run(docs, worklog)
        assert failing.returncode == 2

        print("State-model validator self-test passed.")
        print("Pass path: exit 0")
        print("Failure path: exit 2")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
