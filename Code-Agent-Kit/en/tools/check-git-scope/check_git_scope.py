# SPDX-License-Identifier: MPL-2.0
"""Check the final Git change set against expected and acknowledged files.

Findings are tagged `[check-git-scope:<id>]`; see
docs/core/finding-identifiers.md. The identifier is printed for
`expected-unchanged` whether it blocks (`--strict`) or only warns — severity is
not part of an identifier, it lives in `enforcement-matrix.md`.

Exit codes:
  0  the change set matches expected plus acknowledged scope
  2  scope mismatch
  1  tool error
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


def run(
    root: Path,
    *args: str,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(args),
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )


def git_root(start: Path) -> Path | None:
    result = run(start, "git", "rev-parse", "--show-toplevel")
    if result.returncode != 0:
        return None
    return Path(result.stdout.strip()).resolve()


def normalize(value: str) -> str:
    return value.replace("\\", "/").strip().strip('"').strip("'").lstrip("./")


def parse_list(inline: str | None, path: Path | None) -> list[str]:
    values: list[str] = []

    if inline:
        values.extend(re.split(r"[,\n]", inline))

    if path:
        values.extend(path.read_text(encoding="utf-8").splitlines())

    result = []
    for value in values:
        cleaned = value.strip().lstrip("-*[ ]xX").strip().strip("`")
        cleaned = normalize(cleaned)
        if cleaned and ("/" in cleaned or "." in cleaned):
            result.append(cleaned)

    return list(dict.fromkeys(result))


def expected_from_design(design: Path) -> list[str]:
    text = design.read_text(encoding="utf-8")
    match = re.search(
        r"^## Expected Files\s*$([\s\S]*?)(?=^## |\Z)",
        text,
        flags=re.MULTILINE,
    )
    if not match:
        raise RuntimeError(
            "[check-git-scope:design-without-expected-files] Design does not "
            "contain a '## Expected Files' section."
        )

    return list(
        dict.fromkeys(
            normalize(value)
            for value in re.findall(r"`([^`]+)`", match.group(1))
            if "*" not in value and not value.endswith("/")
        )
    )


def resolve_base(root: Path, requested: str | None) -> str | None:
    candidates = []
    if requested:
        candidates.append(requested)
    candidates.extend(["origin/main", "main", "master"])

    for candidate in candidates:
        result = run(root, "git", "rev-parse", "--verify", "--quiet", candidate)
        if result.returncode == 0:
            return candidate
    return None


def parse_porcelain(value: str) -> set[str]:
    files = set()
    for line in value.splitlines():
        if not line.strip():
            continue
        path = line[3:] if len(line) > 3 else line.strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        files.add(normalize(path))
    return files


def changed_files(root: Path, base: str | None) -> set[str]:
    status = run(root, "git", "status", "--porcelain", "-uall")
    changed = parse_porcelain(status.stdout) if status.returncode == 0 else set()

    if base:
        committed = run(
            root,
            "git",
            "diff",
            "--name-only",
            f"{base}...HEAD",
            "--",
        )
        if committed.returncode == 0:
            changed.update(
                normalize(line)
                for line in committed.stdout.splitlines()
                if line.strip()
            )

    return changed


def match_path(changed: set[str], expected: str) -> str | None:
    for candidate in changed:
        if (
            candidate == expected
            or candidate.endswith("/" + expected)
            or expected.endswith("/" + candidate)
        ):
            return candidate
    return None


def apply_scope(paths: list[str], scope: str) -> list[str]:
    prefix = normalize(scope).strip("/")
    if not prefix:
        return paths
    return [
        value
        if value == prefix or value.startswith(prefix + "/")
        else f"{prefix}/{value}"
        for value in paths
    ]


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("--design", type=Path)
    parser.add_argument("--expected")
    parser.add_argument("--expected-file", type=Path)
    parser.add_argument("--ack")
    parser.add_argument("--ack-file", type=Path)
    parser.add_argument("--base")
    parser.add_argument("--scope", default="")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    try:
        expected = parse_list(args.expected, args.expected_file)
        if args.design:
            expected.extend(expected_from_design(args.design))
        expected = apply_scope(list(dict.fromkeys(expected)), args.scope)

        acknowledged = apply_scope(
            parse_list(args.ack, args.ack_file),
            args.scope,
        )

        if not expected:
            print(
                "SKIP: no expected files were supplied through design, "
                "--expected, or --expected-file."
            )
            return 0

        root = args.root.resolve()
        repository = git_root(root)

        if repository is None:
            missing = [
                value
                for value in expected
                if not (root / value).exists()
                and not Path(value).exists()
            ]
            print(
                "MODE: Git unavailable; checking expected artifact existence "
                "only."
            )
            if missing:
                for value in missing:
                    print(
                        "FAIL: [check-git-scope:expected-artifact-missing] "
                        f"expected artifact is missing: {value}"
                    )
                return 2

            print(
                f"PASS: all {len(expected)} expected artifacts exist. "
                "Unrelated-change detection was skipped."
            )
            return 0

        base = resolve_base(repository, args.base)
        changed = changed_files(repository, base)

        matched = {
            candidate
            for expected_path in expected
            if (candidate := match_path(changed, expected_path))
        }
        ack_matched = {
            candidate
            for ack_path in acknowledged
            if (candidate := match_path(changed, ack_path))
        }

        prefix = normalize(args.scope).strip("/")
        in_scope = {
            value
            for value in changed
            if not prefix
            or value == prefix
            or value.startswith(prefix + "/")
        }

        unexpected = sorted(in_scope - matched - ack_matched)
        missing = sorted(
            expected_path
            for expected_path in expected
            if match_path(changed, expected_path) is None
        )

        print(f"Base: {base or 'working tree only'}")
        print(f"Changed in scope: {len(in_scope)}")
        print(f"Expected: {len(expected)}")
        print(f"Acknowledged unexpected: {len(ack_matched)}")

        failures = 0
        if unexpected:
            failures += len(unexpected)
            print("\nUnexpected changed files:")
            for value in unexpected:
                print(f"  - [check-git-scope:unexpected-change] {value}")
            print(
                "Record a reason and impact in the worklog, then pass the "
                "file through --ack or --ack-file."
            )

        if missing:
            label = "FAIL" if args.strict else "WARN"
            print(f"\n{label}: expected but unchanged:")
            for value in missing:
                print(f"  - [check-git-scope:expected-unchanged] {value}")
            if args.strict:
                failures += len(missing)

        if failures:
            print(
                "\nFAIL: scope mismatch. Return to Analysis and update the "
                "design or restore unrelated files."
            )
            return 2

        print("\nPASS: changed files match expected plus acknowledged scope.")
        return 0
    except (OSError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
