# SPDX-License-Identifier: MPL-2.0
"""Validate that a stack pack contains required evidence and user decisions.

## Evidence is measured, not declared

Every `status` and `declared_state` in a manifest is a sentence somebody typed.
This tool used to check only that those sentences agreed with each other, and that
an `evidence` list was **non-empty** — never that any path in it existed. A stack
with fourteen placeholder documents and entirely invented evidence therefore
reported `READY`, exit 0. Measured, not inferred:

    evidence: ["this/file/does/not/exist.json"]   ->   Stack readiness: READY

So `ready` meant "somebody typed something in the evidence field". Now each
reference is resolved against the tree, and an input whose evidence resolves to
nothing is not evidenced.

That also makes the verdict useful *in an adopting project* rather than only here:
the same profile measures whatever tree it is pointed at, so `ready` is computed
per-project instead of shipped as a claim.

### How a reference is resolved

- Relative to the **stack directory** first, then to the **project root** — both,
  because a profile legitimately cites its own documents *and* files in the
  project it governs.
- A leading `/` means project-root-relative and nothing else. That is the only
  reading of `/global.json` that was ever intended.
- Glob characters are honoured, so `backend/*.csproj` means "at least one".
- The project root is found by walking up for `AGENTS.md`,
  `DESIGN-CONCEPTS.md` or `repository-manifest.json`; `--project-root` overrides
  it for a layout those markers do not describe.

### Evidence is a path, not a description

A reference is a path or a glob. It used to be possible to write a sentence there
— `"search: no client"` was in this tool's own self-test — and a sentence cannot
be checked by anything, which puts it back in the category of things somebody
typed.

Proving a capability *absent* is the case that seems to need prose, and it does
not: the search belongs in `capability-detection.md`, and that document is then the
evidence. The shipped stacks already do this. A recorded search is auditable; a
sentence in a JSON field is not.

### The document and the manifest must agree

`STACK-INPUTS.md` is the table a person fills in; `STACK-READINESS.json` is what
this tool reads. Nothing used to compare them, so filling in the table and
forgetting the manifest left the stack `blocked` with no explanation, and updating
the manifest while leaving the table stale published a document that lied.

They are now compared, joined on a backticked key column that exists for exactly
that purpose. A disagreement is a **warning** — and a warning derives
`provisional`, so a stack declaring `ready` with disagreeing files fails on the
declared-state mismatch. That is intended, not a side effect. A stack whose
document has no key column is simply not compared: being unable to compare is not
the same as disagreeing.

**At least one** reference must resolve, not all of them. A profile may list
several candidate manifests — `frontend/package.json` and `backend/*.csproj` —
and a project with only a backend is not thereby unevidenced. References that do
not resolve are named in a warning, so a list that has rotted is visible without
being fatal. A list where *nothing* resolves is the forgery, and that fails.

Findings are tagged `[check-stack-readiness:<id>]`; see
docs/core/finding-identifiers.md.

Exit codes:
  0  the stack validates as ready (or provisional with --allow-provisional)
  2  blocked, or the declared state contradicts the derived one
  1  tool error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402


# Files whose presence marks the root of the project a stack governs.
ROOT_MARKERS = ("AGENTS.md", "DESIGN-CONCEPTS.md", "repository-manifest.json")

GLOB_CHARACTERS = "*?["

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



INPUTS_DOCUMENT = "STACK-INPUTS.md"
BACKTICKED = re.compile(r"`([^`]+)`")


def document_statuses(stack: Path, keys: set[str]) -> dict[str, set[str]]:
    """Read the statuses the human-facing tables in STACK-INPUTS.md claim.

    A row joins to a manifest entry through a backticked key. That column exists
    only so this comparison is possible: the other columns are prose, and joining
    on prose would break the moment somebody improved a sentence.

    A key with no row returns nothing. Not being able to compare is not the same
    as disagreeing, and reporting it as a disagreement would punish a stack whose
    document simply predates this check.
    """
    document = stack / INPUTS_DOCUMENT
    if not document.is_file():
        return {}
    found: dict[str, set[str]] = {}
    try:
        text = document.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if len(cells) < 2:
            continue
        matched = None
        for cell in cells:
            for token in BACKTICKED.findall(cell):
                if token in keys:
                    matched = token
                    break
            if matched:
                break
        if matched is None:
            continue
        status = cells[-1].strip().strip("`").lower()
        if not status:
            status = "unknown"
        found.setdefault(matched, set()).add(status)
    return found


def _document_has_table(stack: Path) -> bool:
    """True when STACK-INPUTS.md carries at least one filled-in table row.

    The distinction matters. A document that is still a placeholder has nothing to
    compare and never claimed to; saying so would punish a stack nobody has started
    filling in, which is the same mistake the per-key tolerance above avoids. A
    document with rows but no joinable key is the opposite: it looks complete, and
    reports agreement that was never established.
    """
    document = stack / INPUTS_DOCUMENT
    if not document.is_file():
        return False
    try:
        lines = document.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return False
    seen_separator = False
    rows = 0
    for line in lines:
        stripped = line.strip()
        if not stripped.startswith("|"):
            seen_separator = False
            continue
        if set(stripped) <= set("|- :"):
            seen_separator = True
            continue
        if not seen_separator:
            continue
        rows += 1
        # One backticked token anywhere in the row means a `Key` column exists and
        # is being used. The key may simply not be in this manifest, which is the
        # tolerated case: extra rows are allowed and are not this tool's business.
        # No backticked token in any row is the defect — the column is gone.
        if BACKTICKED.findall(stripped):
            return False
    return rows > 0


def compare_document(
    stack: Path,
    manifest_statuses: dict[str, str],
    keys: set[str],
    warnings: list[str],
) -> None:
    """Warn when STACK-INPUTS.md and STACK-READINESS.json disagree.

    A **warning**, and the consequence is deliberate: a warning derives
    `provisional`, so a stack that declares `ready` while its two files disagree
    fails on the declared-state mismatch. That is the intended outcome. Filling in
    the table and forgetting the manifest is the single most likely mistake when
    unblocking a stack, and the old behaviour was to keep saying `blocked` without
    ever saying why. The reverse — manifest updated, table left stale — publishes a
    document that lies about the project.

    The message has to carry the fix, because the person reading it is mid-task and
    will not go looking for an explanation.
    """
    documented = document_statuses(stack, keys)

    # A key with no row is tolerated above, deliberately. *Every* key having no
    # row is a different thing and must not be tolerated: it means the document
    # carries no joinable column at all, so the comparison below iterates over
    # nothing and reports agreement it never established. That is how
    # `ko/stacks/react-aspnetcore` shipped a table with the `Key` column dropped
    # in translation and still measured `READY` with exit 0 — the check passed
    # because its subject was missing, which is the failure this kit exists to
    # catch. Reported at the same weight as drift: a warning, which derives
    # `provisional`, so a stack cannot declare `ready` on an uncomparable table.
    if keys and not documented and _document_has_table(stack):
        warnings.append(
            f"[check-stack-readiness:inputs-document-unjoinable] "
            f"{INPUTS_DOCUMENT} has no row this check can join to "
            f"STACK-READINESS.json. Rows join through a backticked key — add the "
            f"`Key` column back, carrying the manifest keys verbatim "
            f"({', '.join(sorted(keys)[:3])}...). Until then the table and the "
            f"manifest are not being compared at all."
        )

    for key, statuses in sorted(documented.items()):
        expected = manifest_statuses.get(key)
        if expected is None:
            continue
        if expected not in statuses:
            shown = ", ".join(sorted(statuses))
            warnings.append(
                f"[check-stack-readiness:inputs-document-drift] {key}: "
                f"{INPUTS_DOCUMENT} says '{shown}' but STACK-READINESS.json says "
                f"'{expected}'. Both must agree — the document is what a person "
                f"reads and the manifest is what this check reads. Update whichever "
                f"is behind."
            )


def find_project_root(stack: Path) -> Path:
    current = stack.resolve()
    while current.parent != current:
        if any((current / marker).exists() for marker in ROOT_MARKERS):
            return current
        current = current.parent
    return stack.resolve()


def evidence_resolves(stack: Path, root: Path, reference: str) -> bool:
    """Does this one evidence reference name something that exists?"""
    text = str(reference).strip().replace("\\", "/")
    if not text:
        return False
    if text.startswith("/"):
        bases = [root]
        text = text.lstrip("/")
    else:
        bases = [stack, root]
    if not text:
        return False
    for base in bases:
        if any(character in text for character in GLOB_CHARACTERS):
            try:
                if next(base.glob(text), None) is not None:
                    return True
            except (ValueError, OSError, NotImplementedError):
                continue
        elif (base / text).exists():
            return True
    return False


def measure_evidence(
    stack: Path,
    root: Path,
    label: str,
    key: str,
    evidence: list[Any],
    failures: list[str],
    notes: list[str],
) -> None:
    found = [e for e in evidence if evidence_resolves(stack, root, str(e))]
    missing = [str(e) for e in evidence if not evidence_resolves(stack, root, str(e))]
    if not found:
        failures.append(
            f"[check-stack-readiness:evidence-not-found] {label} {key}: "
            f"no cited evidence exists ({', '.join(missing)})"
        )
    elif missing:
        # A note, not a warning. A warning would derive `provisional`, which then
        # contradicts a manifest that declares `ready` -- so citing one candidate
        # manifest that this particular project happens not to have would silently
        # downgrade the whole stack. Visible, and not load-bearing.
        notes.append(
            f"[check-stack-readiness:evidence-partly-missing] {label} {key}: "
            f"{', '.join(missing)}"
        )


def validate(
    stack: Path,
    manifest: dict[str, Any],
    project_root: Path | None = None,
) -> tuple[str, list[str], list[str]]:
    failures: list[str] = []
    warnings: list[str] = []
    # Notes are advisory only and never reach the derived state; see
    # measure_evidence for why that distinction is load-bearing.
    notes: list[str] = []
    root = project_root if project_root is not None else find_project_root(stack)

    required_documents = manifest.get(
        "required_documents",
        REQUIRED_DEFAULT,
    )
    if not isinstance(required_documents, list):
        failures.append("[check-stack-readiness:bad-schema] required_documents must be an array.")
        required_documents = []

    for relative in required_documents:
        path = stack / str(relative)
        if not path.exists() or not path.is_file() or path.stat().st_size == 0:
            failures.append(f"[check-stack-readiness:missing-document] {relative}")

    inputs = manifest.get("inputs", [])
    if not isinstance(inputs, list):
        failures.append("[check-stack-readiness:bad-schema] inputs must be an array.")
        inputs = []

    for item in inputs:
        key = str(item.get("key", "<missing-key>"))
        status = str(item.get("status", "unknown"))
        required = bool(item.get("required", False))
        evidence = item.get("evidence", [])

        if status not in ALLOWED:
            failures.append(f"[check-stack-readiness:invalid-status] input {key}: '{status}'")
            continue

        if required and status not in RESOLVED:
            failures.append(f"[check-stack-readiness:input-unresolved] {key}")

        if status in {"confirmed", "detected"}:
            if not evidence:
                failures.append(
                    f"[check-stack-readiness:input-without-evidence] {key} ({status})"
                )
            else:
                measure_evidence(stack, root, "input", key, evidence,
                                 failures, notes)

        if not required and status == "unknown":
            warnings.append(f"[check-stack-readiness:optional-input-unresolved] {key}")

    capabilities = manifest.get("capabilities", [])
    if not isinstance(capabilities, list):
        failures.append("[check-stack-readiness:bad-schema] capabilities must be an array.")
        capabilities = []

    for item in capabilities:
        key = str(item.get("key", "<missing-key>"))
        status = str(item.get("status", "unknown"))
        evidence = item.get("evidence", [])
        selected_path = str(item.get("selected_path", "")).strip()
        blocks = item.get("blocks", [])

        if status not in {"present", "absent", "unknown", "not-applicable"}:
            failures.append(
                f"[check-stack-readiness:invalid-status] capability {key}: '{status}'"
            )
            continue

        if status in {"present", "absent"}:
            if not evidence:
                failures.append(f"[check-stack-readiness:capability-without-evidence] {key}")
            else:
                measure_evidence(stack, root, "capability", key, evidence,
                                 failures, notes)
            if not selected_path:
                failures.append(
                    f"[check-stack-readiness:capability-without-path] {key}"
                )

        if status == "unknown" and blocks:
            failures.append(
                f"[check-stack-readiness:blocking-capability-unresolved] {key}; blocks={blocks}"
            )
        elif status == "unknown":
            warnings.append(f"[check-stack-readiness:capability-unresolved] {key}")

    # Compared before the state is derived, because a disagreement has to be able
    # to move it. See compare_document for why that is deliberate.
    manifest_statuses: dict[str, str] = {}
    for item in inputs:
        if isinstance(item, dict) and item.get("key"):
            manifest_statuses[str(item["key"])] = str(item.get("status", "unknown"))
    for item in capabilities:
        if isinstance(item, dict) and item.get("key"):
            manifest_statuses[str(item["key"])] = str(item.get("status", "unknown"))
    compare_document(stack, manifest_statuses, set(manifest_statuses), warnings)

    derived = "blocked" if failures else ("provisional" if warnings else "ready")
    declared = str(manifest.get("declared_state", "")).strip()

    if declared and declared != derived:
        failures.append(
            f"[check-stack-readiness:declared-state-mismatch] declared '{declared}' "
            f"but derived '{derived}'"
        )
        derived = "blocked"

    # Merged only now, after `derived` was computed from `warnings` alone. That
    # ordering is the whole mechanism: notes are reported and cannot move the state.
    return derived, failures, warnings + notes


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--stack", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-provisional", action="store_true")
    parser.add_argument(
        "--project-root", type=Path,
        help="root the evidence paths are relative to; inferred when omitted",
    )
    args = parser.parse_args()

    try:
        stack = args.stack.resolve()
        manifest_path = (
            args.manifest.resolve()
            if args.manifest
            else stack / "STACK-READINESS.json"
        )
        manifest = load(manifest_path)
        project_root = args.project_root.resolve() if args.project_root else None
        state, failures, warnings = validate(stack, manifest, project_root)

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
