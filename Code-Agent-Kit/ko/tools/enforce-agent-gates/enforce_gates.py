# SPDX-License-Identifier: MPL-2.0
"""Turn the advisory Markdown rules (AGENTS.md, prompts/GATE.md, docs/core/*)
into a deterministic, blocking gate at the git commit and CI layers.

Modes:
  --staged            check files staged for the current commit  (pre-commit hook)
  --base <ref>        check the diff against a base ref           (CI / PR)

Exit codes:
  0  all enforced gates pass (or nothing relevant changed)
  2  a hard gate failed  -> commit/PR is blocked
  1  tool error -- this check could not reach a verdict at all

The 1/2 split is a machine contract, not a formality: a runner that cannot tell
"this gate found something" from "this gate could not run" blocks correct
commits. Being outside a git repository is the second kind. `check-document-sync`
already exits 1 on exactly that condition, and the same condition returning two
different values inside one repository is itself the defect.

Reference: docs/core/enforcement-matrix.md maps each rule to its mechanism.
Findings are tagged `[enforce-agent-gates:<id>]`; see
docs/core/finding-identifiers.md.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

SOURCE_SUFFIXES = {
    ".cs", ".csproj", ".fs", ".vb",
    ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte",
    ".java", ".kt", ".go", ".rs", ".py",
    ".ex", ".exs", ".php", ".rb",
    ".xjs", ".xfdl", ".xml",
}

WORKFLOW_ROOTS = {
    "docs", "prompts", "templates", "stacks", "tools", "scripts",
    "demos", "reference-assets", "agent-configs", "samples", "LICENSES",
    ".codex", ".roo", ".clinerules", ".agent-state", ".agent-evidence",
    ".github",
}
IGNORED_PARTS = {
    ".git", ".vs", "bin", "obj", "node_modules",
    "dist", "coverage", "__pycache__", ".venv",
}

MANDATORY_GATE_SECTIONS = ("## 1. Analysis", "## 2. Task", "## 3.", "## 4.", "## 5.")

SECRET_PATTERNS = [
    (re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{3,}['\"]"), "hardcoded password"),
    (re.compile(r"(?i)(secret|api[_-]?key|access[_-]?key|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}['\"]"), "hardcoded secret/key/token"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
]
SECRET_ALLOW = re.compile(r"(\.example($|\.)|\.sample($|\.)|/tests?/|\.test\.|\.spec\.|_test\.|README|\.md$)")


def git(*args):
    return subprocess.run(["git", *args], text=True, capture_output=True, check=False).stdout


def changed_files(base):
    if base:
        out = git("diff", "--name-only", "--diff-filter=ACMR", base, "--")
    else:
        out = git("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    files = []
    for line in out.splitlines():
        rel = line.strip().replace("\\", "/").lstrip("./")
        if rel:
            files.append(rel)
    return files


def staged_blob(path, base):
    ref = (base + ":" + path) if base else (":" + path)
    result = subprocess.run(["git", "show", ref], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        p = Path(path)
        return p.read_text(encoding="utf-8", errors="replace") if p.exists() else ""
    return result.stdout


def is_project_source(rel):
    path = Path(rel)
    if any(part in IGNORED_PARTS for part in path.parts):
        return False
    if path.parts and path.parts[0] in WORKFLOW_ROOTS:
        return False
    return path.suffix.lower() in SOURCE_SUFFIXES


def gate_secret_scan(changed, base):
    failures = []
    for rel in changed:
        if SECRET_ALLOW.search(rel):
            continue
        if Path(rel).suffix.lower() not in SOURCE_SUFFIXES \
           and not rel.endswith((".json", ".yml", ".yaml", ".toml", ".env", ".config")):
            continue
        content = staged_blob(rel, base)
        for pattern, label in SECRET_PATTERNS:
            if pattern.search(content):
                failures.append(
                    "[enforce-agent-gates:hardcoded-secret] " + label + " in " + rel)
                break
    return failures


def find_active_worklog(changed):
    for rel in changed:
        if re.search(r"(^|/)docs/worklogs/.+\.md$", rel) and "README" not in rel:
            return Path(rel)
    hits = [h for h in sorted(Path(".").glob("docs/worklogs/*.md")) if "README" not in h.name]
    return hits[-1] if hits else None


def gate_worklog_and_gate_sections(source_changes, changed):
    if not source_changes:
        return []
    failures = []
    worklog = find_active_worklog(changed)
    if worklog is None or not worklog.exists():
        return ["[enforce-agent-gates:worklog-missing] project source changed but no worklog under docs/worklogs/ was produced (GATE.md 5-section evidence missing)."]
    text = worklog.read_text(encoding="utf-8", errors="replace")
    for section in MANDATORY_GATE_SECTIONS:
        if section not in text:
            failures.append("[enforce-agent-gates:worklog-section-missing] worklog " + str(worklog) + " missing section '" + section + "'")
    if "Expected Files" in text:
        tail = text.split("Expected Files", 1)[1]
        if not re.search(r"(?m)^\s*-\s*\[[ xX]\]\s+\S+", tail):
            failures.append("[enforce-agent-gates:expected-files-empty] worklog " + str(worklog) + ": 'Expected Files' has no concrete entry.")
    return failures


def gate_state_sync(source_changes, changed):
    """current/history sync is a hard block; project-map is only *reviewed* for
    shared-file impact, so its absence is a warning. Returns (failures, warnings)."""
    if not source_changes:
        return [], []
    changed_set = set(changed)

    def touched(predicate):
        return any(predicate(c) for c in changed_set)

    failures = []
    warnings = []
    if not touched(lambda c: re.search(r"docs/features/.+\.current\.md$", c)):
        failures.append("[enforce-agent-gates:current-not-updated] source changed but no feature '*.current.md' was updated.")
    if not touched(lambda c: re.search(r"docs/features/.+\.history\.md$", c)):
        failures.append("[enforce-agent-gates:history-not-appended] source changed but no feature '*.history.md' append was made.")
    if not touched(lambda c: c.endswith("docs/project-map.md")):
        warnings.append("[enforce-agent-gates:project-map-not-touched] 'docs/project-map.md' not touched - confirm no shared-file/impact change is unrecorded.")
    return failures, warnings



def _verification_section(text):
    lines = text.splitlines()
    start = None
    for i, l in enumerate(lines):
        if re.match(r"^#{1,6}\s", l) and re.search(r"(?i)verification|검증|##\s*5\b", l):
            start = i; break
    if start is None:
        return ""
    out = []
    for l in lines[start + 1:]:
        if re.match(r"^##\s", l):
            break
        out.append(l)
    return "\n".join(out)


def gate_verification_evidence(source_changes, changed):
    """A PASS with no cited command/exit is not evidence. Conservative: block only
    when the Verification section claims PASS but has NO evidence token at all
    (no backtick command, no code fence, no digit)."""
    if not source_changes:
        return []
    worklog = find_active_worklog(changed)
    if worklog is None or not worklog.exists():
        return []
    sec = _verification_section(worklog.read_text(encoding="utf-8", errors="replace"))
    if not sec.strip():
        return []
    claims = re.search(r"(?i)\bPASS\b|✅|완료|\bDONE\b", sec) is not None
    if not claims:
        return []
    has_evidence = ("`" in sec) or ("```" in sec) or (re.search(r"\d", sec) is not None)
    if not has_evidence:
        return ["[enforce-agent-gates:verification-without-evidence] worklog Verification claims PASS with no evidence at all "
                "(no command, no exit code). Cite the command and exit code, or mark PENDING."]
    return []


def gate_unexpected_files(source_changes, changed):
    if not source_changes:
        return []
    worklog = find_active_worklog(changed)
    if worklog is None or not worklog.exists():
        return []
    declared = worklog.read_text(encoding="utf-8", errors="replace")
    undeclared = [s for s in source_changes if Path(s).name not in declared and s not in declared]
    return ["[enforce-agent-gates:file-not-declared] source file not declared in worklog Expected Files: " + s for s in undeclared]


def main():
    parser = ArgumentParser(description="Evidence-First enforcement gate.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--staged", action="store_true", help="pre-commit mode")
    group.add_argument("--base", help="CI mode: base ref to diff against")
    parser.add_argument("--strict-scope", action="store_true",
                        help="treat undeclared-file scope findings as blocking (default: warn)")
    args = parser.parse_args()
    base = args.base if args.base else None

    if git("rev-parse", "--is-inside-work-tree").strip() != "true":
        # A tool error (1), not a validation failure (2). Nothing was found to
        # be wrong here -- the check simply could not run. This returned 2 for
        # three releases; every caller branches on `!= 0` only, so the change is
        # invisible to the hook and to CI, and it removes a contradiction with
        # check-document-sync, which already exits 1 on this same condition.
        print("[enforce-agent-gates:not-a-repository] not inside a git "
              "repository - this gate reads the staged diff and has nothing to "
              "read.", file=sys.stderr)
        return 1

    changed = changed_files(base)
    source_changes = [c for c in changed if is_project_source(c)]

    failures = []
    warnings = []

    failures += gate_secret_scan(changed, base)
    failures += gate_worklog_and_gate_sections(source_changes, changed)
    state_failures, state_warnings = gate_state_sync(source_changes, changed)
    failures += state_failures
    warnings += state_warnings

    scope_findings = gate_unexpected_files(source_changes, changed)
    if args.strict_scope:
        failures += scope_findings
    else:
        warnings += scope_findings

    failures += gate_verification_evidence(source_changes, changed)

    mode = ("CI diff vs " + base) if base else "staged (pre-commit)"
    print("Evidence-First enforcement gate")
    print("  mode           : " + mode)
    print("  changed files  : " + str(len(changed)))
    print("  project source : " + str(len(source_changes)))
    for w in warnings:
        print("  WARN  " + w)

    if not source_changes and not failures:
        print("  result         : PASS (no project source change to govern)")
        return 0

    if failures:
        print("  result         : BLOCKED")
        for f in failures:
            print("  FAIL  " + f, file=sys.stderr)
        print("\nRun the workflow before committing (prompts/0-sync-and-orient.md -> prompts/GATE.md). "
              "If source was changed out of order, follow docs/core/recovery-mode.md. "
              "Explicit human override: git commit --no-verify", file=sys.stderr)
        return 2

    print("  result         : PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
