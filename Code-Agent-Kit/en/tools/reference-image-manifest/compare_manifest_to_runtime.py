# SPDX-License-Identifier: MPL-2.0
"""Compare named reference-image regions with browser computed-color evidence."""

from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path
from typing import Any


RGB_PATTERN = re.compile(
    r"rgba?\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\s*,\s*"
    r"(\d+(?:\.\d+)?)(?:\s*,\s*[\d.]+)?\s*\)"
)
HEX_PATTERN = re.compile(r"^#([0-9a-fA-F]{6})(?:[0-9a-fA-F]{2})?$")


def parse_color(value: str) -> tuple[int, int, int]:
    value = value.strip()
    match = HEX_PATTERN.fullmatch(value)
    if match:
        digits = match.group(1)
        return tuple(int(digits[index : index + 2], 16) for index in (0, 2, 4))

    match = RGB_PATTERN.fullmatch(value)
    if match:
        return tuple(
            max(0, min(255, round(float(channel))))
            for channel in match.groups()
        )

    raise ValueError(f"Unsupported color value: {value}")


def srgb_channel(value: int) -> float:
    normalized = value / 255
    return (
        normalized / 12.92
        if normalized <= 0.04045
        else ((normalized + 0.055) / 1.055) ** 2.4
    )


def rgb_to_lab(rgb: tuple[int, int, int]) -> tuple[float, float, float]:
    red, green, blue = (srgb_channel(value) for value in rgb)

    x = (red * 0.4124564 + green * 0.3575761 + blue * 0.1804375) / 0.95047
    y = red * 0.2126729 + green * 0.7151522 + blue * 0.0721750
    z = (red * 0.0193339 + green * 0.1191920 + blue * 0.9503041) / 1.08883

    delta = 6 / 29

    def f(value: float) -> float:
        return (
            value ** (1 / 3)
            if value > delta**3
            else value / (3 * delta**2) + 4 / 29
        )

    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)


def delta_e_2000(
    lab1: tuple[float, float, float],
    lab2: tuple[float, float, float],
) -> float:
    l1, a1, b1 = lab1
    l2, a2, b2 = lab2
    c1 = math.hypot(a1, b1)
    c2 = math.hypot(a2, b2)
    c_bar = (c1 + c2) / 2
    g = 0.5 * (1 - math.sqrt(c_bar**7 / (c_bar**7 + 25**7)))
    a1_prime = (1 + g) * a1
    a2_prime = (1 + g) * a2
    c1_prime = math.hypot(a1_prime, b1)
    c2_prime = math.hypot(a2_prime, b2)

    def hue(a: float, b: float) -> float:
        angle = math.degrees(math.atan2(b, a))
        return angle + 360 if angle < 0 else angle

    h1_prime = hue(a1_prime, b1)
    h2_prime = hue(a2_prime, b2)
    delta_l = l2 - l1
    delta_c = c2_prime - c1_prime

    hue_difference = h2_prime - h1_prime
    if c1_prime * c2_prime == 0:
        delta_h_angle = 0
    elif abs(hue_difference) <= 180:
        delta_h_angle = hue_difference
    elif hue_difference > 180:
        delta_h_angle = hue_difference - 360
    else:
        delta_h_angle = hue_difference + 360

    delta_h = (
        2
        * math.sqrt(c1_prime * c2_prime)
        * math.sin(math.radians(delta_h_angle / 2))
    )
    l_bar = (l1 + l2) / 2
    c_prime_bar = (c1_prime + c2_prime) / 2

    if c1_prime * c2_prime == 0:
        h_prime_bar = h1_prime + h2_prime
    elif abs(h1_prime - h2_prime) <= 180:
        h_prime_bar = (h1_prime + h2_prime) / 2
    elif h1_prime + h2_prime < 360:
        h_prime_bar = (h1_prime + h2_prime + 360) / 2
    else:
        h_prime_bar = (h1_prime + h2_prime - 360) / 2

    t = (
        1
        - 0.17 * math.cos(math.radians(h_prime_bar - 30))
        + 0.24 * math.cos(math.radians(2 * h_prime_bar))
        + 0.32 * math.cos(math.radians(3 * h_prime_bar + 6))
        - 0.20 * math.cos(math.radians(4 * h_prime_bar - 63))
    )
    delta_theta = 30 * math.exp(-(((h_prime_bar - 275) / 25) ** 2))
    r_c = 2 * math.sqrt(c_prime_bar**7 / (c_prime_bar**7 + 25**7))
    s_l = 1 + (0.015 * (l_bar - 50) ** 2) / math.sqrt(
        20 + (l_bar - 50) ** 2
    )
    s_c = 1 + 0.045 * c_prime_bar
    s_h = 1 + 0.015 * c_prime_bar * t
    r_t = -math.sin(math.radians(2 * delta_theta)) * r_c

    return math.sqrt(
        (delta_l / s_l) ** 2
        + (delta_c / s_c) ** 2
        + (delta_h / s_h) ** 2
        + r_t * (delta_c / s_c) * (delta_h / s_h)
    )


def runtime_items(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and isinstance(payload.get("items"), list):
        return payload["items"]
    raise ValueError("Runtime evidence must be an array or an object with items.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--runtime", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    try:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        runtime = runtime_items(
            json.loads(args.runtime.read_text(encoding="utf-8"))
        )
        config = json.loads(args.config.read_text(encoding="utf-8"))

        regions = {
            region["name"]: region
            for region in manifest.get("regions", [])
        }
        results = []
        failures = []

        for check in config["checks"]:
            region = regions.get(check["reference_region"])
            if not region:
                raise ValueError(
                    f"Reference region not found: {check['reference_region']}"
                )

            selector_pattern = re.compile(check["runtime_selector"])
            candidates = [
                item
                for item in runtime
                if selector_pattern.search(str(item.get("selector", "")))
            ]
            if not candidates:
                raise ValueError(
                    f"Runtime selector did not match: "
                    f"{check['runtime_selector']}"
                )

            runtime_item = candidates[0]
            property_name = check["runtime_property"]
            if property_name not in runtime_item:
                raise ValueError(
                    f"Runtime property '{property_name}' is missing."
                )

            reference_source = check.get("reference_source", "average")
            reference_color = region[reference_source]["hex_rgb"]
            runtime_color = str(runtime_item[property_name])
            delta = delta_e_2000(
                rgb_to_lab(parse_color(reference_color)),
                rgb_to_lab(parse_color(runtime_color)),
            )
            maximum = float(check.get("max_delta_e", 5.0))
            status = "PASS" if delta <= maximum else "FAIL"

            result = {
                "name": check["name"],
                "reference_region": check["reference_region"],
                "reference_color": reference_color,
                "runtime_selector": runtime_item["selector"],
                "runtime_property": property_name,
                "runtime_color": runtime_color,
                "delta_e_2000": round(delta, 4),
                "max_delta_e": maximum,
                "status": status,
            }
            results.append(result)
            if status == "FAIL":
                failures.append(result)

        payload = {
            "schema": "evidence-first/reference-runtime-color-comparison/v1",
            "status": "PASS" if not failures else "FAIL",
            "checks": results,
        }

        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

        for result in results:
            print(
                f"{result['status']:4} ΔE00={result['delta_e_2000']:.3f} "
                f"<= {result['max_delta_e']:.3f} {result['name']}"
            )
        return 2 if failures else 0
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        json.JSONDecodeError,
    ) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
