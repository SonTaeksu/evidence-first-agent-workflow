# SPDX-License-Identifier: MPL-2.0
"""Self-test ready and blocked stack-readiness paths."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FILES = [
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


def run(stack: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "check_stack_readiness.py"),
            "--stack",
            str(stack),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        stack = Path(temporary) / "stack"
        for relative in FILES:
            path = stack / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("# test\n", encoding="utf-8")

        manifest = {
            "schema": "evidence-first/stack-readiness/v1",
            "stack_key": "test",
            "declared_state": "ready",
            "required_documents": FILES,
            "inputs": [
                {
                    "key": "runtime",
                    "required": True,
                    "source": "mixed",
                    "status": "detected",
                    "evidence": ["global.json"],
                },
                {
                    "key": "owner-policy",
                    "required": True,
                    "source": "user",
                    "status": "confirmed",
                    "evidence": ["STACK-INPUTS.md"],
                },
            ],
            "capabilities": [
                {
                    "key": "shared-client",
                    "status": "absent",
                    "evidence": ["search: no client"],
                    "selected_path": "approved-default",
                    "blocks": ["API work"],
                }
            ],
        }
        manifest_path = stack / "STACK-READINESS.json"
        manifest_path.write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )

        passing = run(stack)
        assert passing.returncode == 0, passing.stdout + passing.stderr

        manifest["declared_state"] = "blocked"
        manifest["inputs"][1]["status"] = "unknown"
        manifest["inputs"][1]["evidence"] = []
        manifest_path.write_text(
            json.dumps(manifest),
            encoding="utf-8",
        )
        failing = run(stack)
        assert failing.returncode == 2
        assert "Required input unresolved" in failing.stdout + failing.stderr

        print("Stack readiness self-test passed.")
        print("Ready path: exit 0")
        print("Blocked path: exit 2")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
