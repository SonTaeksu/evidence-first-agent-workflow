# SPDX-License-Identifier: MPL-2.0
"""Public-release sanitization gate.

Scans a tree for proprietary / organization-identifying strings that must not
appear in the open-source distribution, plus generic credential patterns.
Intended to run in CI and before any public release commit.

Exit codes:
  0  clean
  2  one or more denylisted / secret matches found (release blocked)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Hard-block: organization / product / proprietary identifiers.
DENY = [
    (r"한화\s*시스템", "org name (Hanwha Systems)"),
    (r"\bHanwha\b", "org name (Hanwha)"),
    (r"\bAONDev\b", "internal platform name (AONDev)"),
    (r"\bOceanDev\b", "internal platform name (OceanDev)"),
    (r"nexacro-aondev", "internal stack pack folder/skill name"),
    (r"\baondev\b", "internal identifier"),
    (r"\bgfn_[A-Za-z]", "proprietary CommLib function prefix (gfn_)"),
    (r"\blfn_[A-Za-z]", "proprietary CommLib function prefix (lfn_)"),
    (r"cell_WF_", "project-specific XCSS class"),
    (r"TOBESOFT", "vendor install path/brand"),
    (r"Program Files.*Nexacro", "absolute vendor SDK path"),
    (r"nexacrodeploy", "vendor build tool path"),
]

# Warn / review: third-party trademarks that may be OK as a named example stack.
REVIEW = [
    (r"\bNexacro\b", "third-party trademark - confirm it is only a named example stack"),
    (r"\bX-API\b", "vendor API name - confirm generic context"),
]

SECRET = [
    (re.compile(r"(?i)(password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{3,}['\"]"), "hardcoded password"),
    (re.compile(r"(?i)(secret|api[_-]?key|access[_-]?key|token)\s*[:=]\s*['\"][A-Za-z0-9_\-]{12,}['\"]"), "hardcoded secret/key/token"),
    (re.compile(r"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"), "private key"),
    (re.compile(r"AKIA[0-9A-Z]{16}"), "AWS access key id"),
]

SKIP_DIRS = {".git", "node_modules", "bin", "obj", "dist", "coverage",
             "__pycache__", ".venv", "target",
             # the gate's own denylist contains the forbidden terms as regex
             # literals; never scan the gate itself.
             "check-sanitization"}
SKIP_SUFFIX = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
               ".woff", ".woff2", ".ttf", ".jar", ".dll", ".exe", ".lock"}


def iter_files(root, allow):
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.suffix.lower() in SKIP_SUFFIX:
            continue
        rel = p.relative_to(root).as_posix()
        if any(a.search(rel) for a in allow):
            continue
        yield p, rel


def main():
    ap = argparse.ArgumentParser(description="Public-release sanitization gate.")
    ap.add_argument("--root", type=Path, default=Path("."))
    ap.add_argument("--extra-deny", action="append", default=[])
    ap.add_argument("--allow-glob", action="append", default=[])
    ap.add_argument("--strict-review", action="store_true")
    args = ap.parse_args()

    root = args.root.resolve()
    allow = [re.compile(a) for a in args.allow_glob]
    deny = [(re.compile(p), why) for p, why in DENY] + \
           [(re.compile(p), "extra-deny") for p in args.extra_deny]
    review = [(re.compile(p), why) for p, why in REVIEW]

    blocks = []
    warns = []
    scanned = 0

    for path, rel in iter_files(root, allow):
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for i, line in enumerate(text.splitlines(), 1):
            for rx, why in deny:
                if rx.search(line):
                    blocks.append(rel + ":" + str(i) + ": [" + why + "] " + line.strip()[:100])
            for rx, why in SECRET:
                if rx.search(line):
                    blocks.append(rel + ":" + str(i) + ": [" + why + "] (redacted)")
            for rx, why in review:
                if rx.search(line):
                    entry = rel + ":" + str(i) + ": [" + why + "] " + line.strip()[:100]
                    (blocks if args.strict_review else warns).append(entry)

    print("Sanitization scan: " + str(scanned) + " files under " + str(root))
    for w in warns:
        print("  WARN  " + w)
    if blocks:
        print("  result: BLOCKED (" + str(len(blocks)) + " finding(s))")
        for b in blocks:
            print("  FAIL  " + b, file=sys.stderr)
        return 2
    print("  result: CLEAN (" + str(len(warns)) + " warning(s))")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
