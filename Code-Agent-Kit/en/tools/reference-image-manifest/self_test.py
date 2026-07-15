# SPDX-License-Identifier: MPL-2.0
"""Self-test the reference image manifest and color comparison tools."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageCms


ROOT = Path(__file__).resolve().parent


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, *args],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    with tempfile.TemporaryDirectory() as temporary:
        folder = Path(temporary)
        image_path = folder / "reference.png"
        manifest_path = folder / "manifest.json"
        normalized_path = folder / "normalized.png"
        regions_path = folder / "regions.json"
        runtime_path = folder / "runtime.json"
        comparison_path = folder / "comparison.json"
        report_path = folder / "report.json"

        image = Image.new("RGB", (100, 100), "#FFFFFF")
        pixels = image.load()
        colors = {
            "top_left": (49, 86, 223),
            "top_right": (23, 32, 51),
            "bottom_left": (238, 242, 248),
            "bottom_right": (255, 255, 255),
        }
        for y in range(100):
            for x in range(100):
                if x < 50 and y < 50:
                    pixels[x, y] = colors["top_left"]
                elif x >= 50 and y < 50:
                    pixels[x, y] = colors["top_right"]
                elif x < 50:
                    pixels[x, y] = colors["bottom_left"]
                else:
                    pixels[x, y] = colors["bottom_right"]

        profile = ImageCms.ImageCmsProfile(
            ImageCms.createProfile("sRGB")
        ).tobytes()
        image.save(image_path, icc_profile=profile)

        regions_path.write_text(
            json.dumps(
                {
                    "regions": [
                        {
                            "name": "primary",
                            "units": "normalized",
                            "x": 0,
                            "y": 0,
                            "width": 0.5,
                            "height": 0.5,
                        },
                        {
                            "name": "text",
                            "units": "normalized",
                            "x": 0.5,
                            "y": 0,
                            "width": 0.5,
                            "height": 0.5,
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )

        extract = run(
            str(ROOT / "extract_reference_image.py"),
            str(image_path),
            "--output",
            str(manifest_path),
            "--normalized-png",
            str(normalized_path),
            "--regions",
            str(regions_path),
            "--grid-size",
            "5",
        )
        if extract.returncode != 0:
            print(extract.stdout)
            print(extract.stderr, file=sys.stderr)
            return 1

        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        assert manifest["source"]["sha256"]
        assert manifest["color_profile"]["icc_present"] is True
        assert manifest["normalized"]["dimensions"] == [100, 100]
        assert len(manifest["grid_samples"]) == 25
        assert manifest["regions"][0]["average"]["hex_rgb"] == "#3156DF"
        assert normalized_path.exists()

        runtime_path.write_text(
            json.dumps(
                {
                    "items": [
                        {
                            "selector": "button.primary-button",
                            "color": "rgb(255, 255, 255)",
                            "backgroundColor": "rgb(49, 86, 223)",
                        },
                        {
                            "selector": "h1.page-title",
                            "color": "rgb(23, 32, 51)",
                            "backgroundColor": "rgb(255, 255, 255)",
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )
        comparison_path.write_text(
            json.dumps(
                {
                    "checks": [
                        {
                            "name": "Primary button",
                            "reference_region": "primary",
                            "reference_source": "average",
                            "runtime_selector": r"\.primary-button$",
                            "runtime_property": "backgroundColor",
                            "max_delta_e": 1,
                        },
                        {
                            "name": "Title text",
                            "reference_region": "text",
                            "reference_source": "average",
                            "runtime_selector": r"\.page-title$",
                            "runtime_property": "color",
                            "max_delta_e": 1,
                        },
                    ]
                }
            ),
            encoding="utf-8",
        )

        compare = run(
            str(ROOT / "compare_manifest_to_runtime.py"),
            "--manifest",
            str(manifest_path),
            "--runtime",
            str(runtime_path),
            "--config",
            str(comparison_path),
            "--output",
            str(report_path),
        )
        if compare.returncode != 0:
            print(compare.stdout)
            print(compare.stderr, file=sys.stderr)
            return 1

        report = json.loads(report_path.read_text(encoding="utf-8"))
        assert report["status"] == "PASS"
        assert all(check["delta_e_2000"] == 0 for check in report["checks"])

        oriented_path = folder / "oriented.jpg"
        oriented_manifest_path = folder / "oriented-manifest.json"
        oriented = Image.new("RGB", (40, 20), "#3156DF")
        exif = Image.Exif()
        exif[274] = 6
        oriented.save(oriented_path, quality=95, exif=exif)

        oriented_extract = run(
            str(ROOT / "extract_reference_image.py"),
            str(oriented_path),
            "--output",
            str(oriented_manifest_path),
        )
        if oriented_extract.returncode != 0:
            print(oriented_extract.stdout)
            print(oriented_extract.stderr, file=sys.stderr)
            return 1

        oriented_manifest = json.loads(
            oriented_manifest_path.read_text(encoding="utf-8")
        )
        assert oriented_manifest["source"]["raw_dimensions"] == [40, 20]
        assert oriented_manifest["source"]["exif_orientation"] == 6
        assert oriented_manifest["normalized"]["dimensions"] == [20, 40]
        assert oriented_manifest["normalized"]["orientation_applied"] is True

        failed_runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
        failed_runtime["items"][0]["backgroundColor"] = "rgb(255, 0, 0)"
        runtime_path.write_text(
            json.dumps(failed_runtime),
            encoding="utf-8",
        )
        failed_compare = run(
            str(ROOT / "compare_manifest_to_runtime.py"),
            "--manifest",
            str(manifest_path),
            "--runtime",
            str(runtime_path),
            "--config",
            str(comparison_path),
        )
        assert failed_compare.returncode == 2

        print("Reference-image manifest self-test passed.")
        print(extract.stdout.strip())
        print(compare.stdout.strip())
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
