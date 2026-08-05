# SPDX-License-Identifier: MPL-2.0
"""Self-test: one passing fixture and one deliberately failing fixture."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent / "check_kit_selfcheck.py"
KIT = TOOL.parent.parent.parent
VALIDATOR = "tools/check-stack-readiness/check_stack_readiness.py"

REQUIRED = [
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


def write_seed(seed: Path, complete: bool) -> None:
    """A blank seed: every required document present, every input unknown.

    The unknown inputs make the derived state `blocked`, which is correct and
    must not be reported. Only the missing document must be.
    """
    documents = REQUIRED if complete else REQUIRED[:-1]
    for relative in documents:
        path = seed / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# seed\n", encoding="utf-8")
    manifest = {
        "schema": "evidence-first/stack-readiness/v1",
        "stack_key": "fixture",
        "declared_state": "blocked",
        "required_documents": REQUIRED,
        "inputs": [
            {
                "key": "runtime-sdk-versions",
                "required": True,
                "source": "user",
                "status": "unknown",
                "evidence": [],
                "notes": "",
            }
        ],
        "capabilities": [
            {
                "key": "implementation-path",
                "status": "unknown",
                "evidence": [],
                "selected_path": "",
                "blocks": ["all stack-dependent implementation"],
            }
        ],
    }
    (seed / "STACK-READINESS.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def copy_shared_library(root: Path) -> None:
    """Copy `tools/_lib` alongside any tool this fixture copies.

    Every tool imports the shared CLI helper. Without it a copied tool dies on
    `from kit_cli import ...` and exits 1 -- a tool error manufactured by the
    fixture, which then looks like a defect in the tool under test. Cheap to
    forget, and loud when you do, which is the only reason this is acceptable
    rather than the helper being inlined into all 23 tools.
    """
    target = root / "tools" / "_lib"
    target.mkdir(parents=True, exist_ok=True)
    for source in (KIT / "tools" / "_lib").glob("*.py"):
        shutil.copy(source, target / source.name)

def build_root(root: Path, complete: bool) -> None:
    copy_shared_library(root)
    target = root / VALIDATOR
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy(KIT / VALIDATOR, target)
    seed = root / "templates" / "stack-profile"
    seed.mkdir(parents=True)
    write_seed(seed, complete)
    (root / "stacks").mkdir()


def run(root: Path) -> int:
    result = subprocess.run(
        [
            sys.executable,
            str(TOOL),
            "--root",
            str(root),
            "--seed",
            "templates/stack-profile",
        ],
        capture_output=True,
        text=True,
    )
    print(result.stdout, end="")
    print(result.stderr, end="", file=sys.stderr)
    return result.returncode


def main() -> int:
    failures = 0
    with tempfile.TemporaryDirectory() as temporary:
        good = Path(temporary) / "good"
        good.mkdir()
        build_root(good, complete=True)
        code = run(good)
        if code != 0:
            print(f"FAIL: complete seed expected exit 0, got {code}")
            failures += 1
        else:
            print("PASS: complete seed accepted (exit 0)")

        bad = Path(temporary) / "bad"
        bad.mkdir()
        build_root(bad, complete=False)
        code = run(bad)
        if code != 2:
            print(f"FAIL: incomplete seed expected exit 2, got {code}")
            failures += 1
        else:
            print("PASS: incomplete seed rejected (exit 2)")

    print(f"self-test failures: {failures}")
    return 0 if failures == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
