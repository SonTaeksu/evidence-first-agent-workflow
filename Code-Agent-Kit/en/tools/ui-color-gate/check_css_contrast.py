# SPDX-License-Identifier: MPL-2.0
"""Deterministically check configured CSS foreground/background contrast pairs."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


HEX_COLOR = re.compile(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


def strip_comments(css: str) -> str:
    return re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)


def matching_brace(text: str, opening: int) -> int:
    depth = 0
    for index in range(opening, len(text)):
        if text[index] == "{":
            depth += 1
        elif text[index] == "}":
            depth -= 1
            if depth == 0:
                return index
    raise ValueError("Unmatched CSS brace.")


def parse_declarations(body: str) -> dict[str, str]:
    declarations: dict[str, str] = {}
    for raw in body.split(";"):
        if ":" not in raw:
            continue
        name, value = raw.split(":", 1)
        name = name.strip().lower()
        value = value.strip()
        if name and value:
            declarations[name] = value
    return declarations


def parse_rules(css: str) -> dict[str, dict[str, str]]:
    rules: dict[str, dict[str, str]] = {}

    def walk(segment: str) -> None:
        cursor = 0
        while True:
            opening = segment.find("{", cursor)
            if opening < 0:
                break

            prelude = segment[cursor:opening].strip()
            closing = matching_brace(segment, opening)
            body = segment[opening + 1 : closing]

            if prelude.startswith("@"):
                walk(body)
            elif prelude:
                declarations = parse_declarations(body)
                for selector in prelude.split(","):
                    normalized = selector.strip()
                    if normalized:
                        rules.setdefault(normalized, {}).update(declarations)

            cursor = closing + 1

    walk(strip_comments(css))
    return rules


def normalize_hex(value: str) -> str:
    value = value.strip()
    if not HEX_COLOR.fullmatch(value):
        raise ValueError(f"Only literal hex colors are supported, got: {value}")

    digits = value[1:]
    if len(digits) == 3:
        digits = "".join(char * 2 for char in digits)
    return f"#{digits.lower()}"


def channel(value: int) -> float:
    normalized = value / 255
    return (
        normalized / 12.92
        if normalized <= 0.04045
        else math.pow((normalized + 0.055) / 1.055, 2.4)
    )


def luminance(color: str) -> float:
    color = normalize_hex(color)
    red = int(color[1:3], 16)
    green = int(color[3:5], 16)
    blue = int(color[5:7], 16)
    return (
        0.2126 * channel(red)
        + 0.7152 * channel(green)
        + 0.0722 * channel(blue)
    )


def contrast_ratio(foreground: str, background: str) -> float:
    first = luminance(foreground)
    second = luminance(background)
    lighter = max(first, second)
    darker = min(first, second)
    return (lighter + 0.05) / (darker + 0.05)


def resolve_value(
    reference: dict[str, Any],
    rules: dict[str, dict[str, str]],
) -> str:
    literal = reference.get("value")
    if literal:
        return normalize_hex(str(literal))

    selector = str(reference["selector"])
    property_name = str(reference["property"]).lower()

    if selector not in rules:
        raise ValueError(f"Selector not found: {selector}")
    if property_name not in rules[selector]:
        raise ValueError(
            f"Property '{property_name}' not found for selector '{selector}'."
        )

    return normalize_hex(rules[selector][property_name])


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--css", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        rules = parse_rules(args.css.read_text(encoding="utf-8"))
        config = json.loads(args.config.read_text(encoding="utf-8"))

        results: list[dict[str, Any]] = []
        failures: list[dict[str, Any]] = []

        for check in config["checks"]:
            foreground = resolve_value(check["foreground"], rules)
            background = resolve_value(check["background"], rules)
            minimum = float(check.get("minimum", 4.5))
            ratio = contrast_ratio(foreground, background)

            result = {
                "name": check["name"],
                "foreground": foreground,
                "background": background,
                "ratio": round(ratio, 3),
                "minimum": minimum,
                "status": "PASS" if ratio >= minimum else "FAIL",
            }
            results.append(result)
            if ratio < minimum:
                failures.append(result)

        payload = {
            "css": args.css.as_posix(),
            "config": args.config.as_posix(),
            "checks": results,
            "status": "PASS" if not failures else "FAIL",
        }

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        for result in results:
            print(
                f"{result['status']:4} "
                f"{result['ratio']:>5.2f}:1 >= {result['minimum']:>4.1f}:1 "
                f"{result['name']} "
                f"({result['foreground']} on {result['background']})"
            )

        return 2 if failures else 0
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
