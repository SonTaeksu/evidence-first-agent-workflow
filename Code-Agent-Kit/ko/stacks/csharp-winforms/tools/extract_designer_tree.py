# SPDX-License-Identifier: MPL-2.0
"""Extract the control tree a Windows Forms designer file declares.

Windows Forms has no DOM, so the kit's rendered-output layer has no HTML to
inspect. The designer file is the nearest deterministic equivalent: it is
generated, it is the single declaration of what the form contains, and it can
be parsed without compiling or launching anything.

Comments are removed before any pattern is applied, and string literals are
preserved while doing it. A naive strip would drop a control that only appears
in a comment into the tree, and would corrupt any literal containing `//`.

Exit codes:
  0  a tree was produced
  2  no form was found in the input
  1  tool error
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CONTAINERS = {
    "FlowLayoutPanel",
    "GroupBox",
    "Panel",
    "SplitContainer",
    "SplitterPanel",
    "TabPage",
    "TableLayoutPanel",
    "ToolStripPanel",
}

CLASS_RE = re.compile(r"\bpartial\s+class\s+(\w+)")
FIELD_RE = re.compile(
    r"\b(?:private|protected|internal|public)\s+([\w.]+(?:<[\w., ]+>)?)\s+(\w+)\s*(?:=[^;]*)?;"
)
NEW_RE = re.compile(r"\bthis\.(\w+)\s*=\s*new\s+([\w.]+)\s*\(")

# The designer declares every control as a field and assigns it with `new`.
# Requiring both excludes form property assignments such as
# `this.ClientSize = new System.Drawing.Size(...)`, which are not controls.
NOT_CONTROL_TYPES = {"System.ComponentModel.IContainer", "IContainer"}
NOT_CONTROL_NAMES = {"components"}
CHILD_RE = re.compile(r"\bthis\.(\w+)\.Controls\.Add\(\s*this\.(\w+)\s*\)")
ROOT_RE = re.compile(r"(?<!\.)\bthis\.Controls\.Add\(\s*this\.(\w+)\s*\)")
TEXT_RE = re.compile(r'\bthis\.(\w+)\.Text\s*=\s*"((?:[^"\\]|\\.)*)"')


def strip_comments(text: str) -> str:
    """Blank out comments, preserving length, line breaks, and literals.

    Replacing rather than deleting keeps every character offset and line
    number identical to the original, so callers need no offset mapping.
    """
    out = list(text)
    index = 0
    length = len(text)
    while index < length:
        char = text[index]

        if char == '"' or char == "'":
            quote = char
            index += 1
            while index < length:
                if text[index] == "\\":
                    index += 2
                    continue
                if text[index] == quote:
                    index += 1
                    break
                if text[index] == "\n" and quote == '"':
                    break  # unterminated literal; do not swallow the file
                index += 1
            continue

        if char == "@" and text.startswith('@"', index):
            index += 2
            while index < length:
                if text.startswith('""', index):
                    index += 2
                    continue
                if text[index] == '"':
                    index += 1
                    break
                index += 1
            continue

        if text.startswith("//", index):
            while index < length and text[index] != "\n":
                out[index] = " "
                index += 1
            continue

        if text.startswith("/*", index):
            while index < length and not text.startswith("*/", index):
                if text[index] != "\n":
                    out[index] = " "
                index += 1
            for offset in range(index, min(index + 2, length)):
                out[offset] = " "
            index += 2
            continue

        index += 1

    return "".join(out)


def extract(source: str, path: str) -> dict:
    text = strip_comments(source)

    class_match = CLASS_RE.search(text)
    form = class_match.group(1) if class_match else ""

    declared = {name: kind for kind, name in FIELD_RE.findall(text)}
    constructed = {name: kind for name, kind in NEW_RE.findall(text)}
    types = {
        name: declared[name]
        for name in declared
        if name in constructed
        and name not in NOT_CONTROL_NAMES
        and declared[name] not in NOT_CONTROL_TYPES
    }

    parents: dict[str, str] = {}
    for parent, child in CHILD_RE.findall(text):
        parents[child] = parent
    for child in ROOT_RE.findall(text):
        parents.setdefault(child, form)
    texts = {name: value for name, value in TEXT_RE.findall(text)}

    controls = []
    for name in sorted(types):
        if name == form:
            continue
        kind = types[name]
        controls.append(
            {
                "name": name,
                "type": kind,
                "short_type": kind.rsplit(".", 1)[-1],
                "parent": parents.get(name, ""),
                "text": texts.get(name, ""),
                "is_container": kind.rsplit(".", 1)[-1] in CONTAINERS,
            }
        )

    children: dict[str, int] = {}
    for control in controls:
        parent = control["parent"]
        if parent:
            children[parent] = children.get(parent, 0) + 1
    for control in controls:
        control["child_count"] = children.get(control["name"], 0)

    return {
        "schema": "evidence-first/winforms-designer-tree/v1",
        "source": path,
        "form": form,
        "controls": controls,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract the control tree from a WinForms designer file."
    )
    parser.add_argument("--designer", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        source = args.designer.read_text(encoding="utf-8-sig")
        tree = extract(source, args.designer.as_posix())

        if not tree["form"]:
            print(
                f"ERROR: no partial class found in {args.designer}",
                file=sys.stderr,
            )
            return 2

        payload = json.dumps(tree, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(payload, encoding="utf-8")
        else:
            print(payload, end="")

        print(
            f"Designer tree: {tree['form']} "
            f"({len(tree['controls'])} control(s))",
            file=sys.stderr,
        )
        return 0
    except (OSError, TypeError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
