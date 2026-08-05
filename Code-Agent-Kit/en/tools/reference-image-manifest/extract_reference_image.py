# SPDX-License-Identifier: MPL-2.0
"""Create a deterministic manifest before an image is sent to a multimodal LLM."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import io
import json
import math
import sys
from pathlib import Path
from typing import Any

# The kit's exit-code convention differs from argparse's: a usage error is a
# tool error (1), not a validation failure (2). See tools/_lib/kit_cli.py.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "_lib"))
from kit_cli import ArgumentParser  # noqa: E402

try:
    from PIL import Image, ImageCms, ImageOps
except ImportError as error:  # pragma: no cover
    raise SystemExit(
        "Pillow is required. Install with: python -m pip install Pillow"
    ) from error


ORIENTATION_NAMES = {
    1: "normal",
    2: "mirror-horizontal",
    3: "rotate-180",
    4: "mirror-vertical",
    5: "mirror-horizontal-rotate-270-cw",
    6: "rotate-90-cw",
    7: "mirror-horizontal-rotate-90-cw",
    8: "rotate-270-cw",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def pixel_hash(image: Image.Image) -> str:
    normalized = image.convert("RGBA")
    digest = hashlib.sha256()
    digest.update(f"{normalized.width}x{normalized.height}:RGBA\0".encode())
    digest.update(normalized.tobytes())
    return digest.hexdigest()


def rgba_to_hex(rgba: tuple[int, int, int, int]) -> str:
    red, green, blue, alpha = rgba
    return f"#{red:02X}{green:02X}{blue:02X}{alpha:02X}"


def color_record(rgba: tuple[int, int, int, int]) -> dict[str, Any]:
    return {
        "rgba": list(rgba),
        "hex_rgba": rgba_to_hex(rgba),
        "hex_rgb": rgba_to_hex(rgba)[:7],
    }


def get_icc_description(profile_bytes: bytes) -> str | None:
    try:
        profile = ImageCms.ImageCmsProfile(io.BytesIO(profile_bytes))
        description = getattr(profile.profile, "profile_description", None)
        return str(description).strip() if description else None
    except Exception:
        return None


def dominant_colors(
    image: Image.Image,
    count: int,
    max_sample_size: int = 512,
) -> list[dict[str, Any]]:
    rgba = image.convert("RGBA")
    scale = min(1.0, max_sample_size / max(rgba.width, rgba.height))
    if scale < 1:
        rgba = rgba.resize(
            (
                max(1, round(rgba.width * scale)),
                max(1, round(rgba.height * scale)),
            ),
            Image.Resampling.LANCZOS,
        )

    quantized = rgba.quantize(
        colors=max(1, min(count, 256)),
        method=Image.Quantize.FASTOCTREE,
    ).convert("RGBA")

    colors = quantized.getcolors(maxcolors=quantized.width * quantized.height)
    if not colors:
        return []

    total = quantized.width * quantized.height
    result = []
    for pixels, rgba_value in sorted(colors, reverse=True)[:count]:
        rgba_tuple = tuple(int(value) for value in rgba_value)
        result.append(
            {
                **color_record(rgba_tuple),
                "pixels": pixels,
                "percentage": round((pixels / total) * 100, 4),
            }
        )
    return result


def grid_samples(image: Image.Image, size: int) -> list[dict[str, Any]]:
    rgba = image.convert("RGBA")
    if size < 2:
        raise ValueError("Grid size must be at least 2.")

    result = []
    for row in range(size):
        y = round((rgba.height - 1) * row / (size - 1))
        for column in range(size):
            x = round((rgba.width - 1) * column / (size - 1))
            value = tuple(int(v) for v in rgba.getpixel((x, y)))
            result.append(
                {
                    "grid": [column, row],
                    "normalized": [
                        round(x / max(1, rgba.width - 1), 6),
                        round(y / max(1, rgba.height - 1), 6),
                    ],
                    "pixel": [x, y],
                    **color_record(value),
                }
            )
    return result


def resolve_region(
    value: dict[str, Any],
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    units = value.get("units", "pixels")
    x = float(value["x"])
    y = float(value["y"])
    region_width = float(value["width"])
    region_height = float(value["height"])

    if units == "normalized":
        x *= width
        y *= height
        region_width *= width
        region_height *= height
    elif units != "pixels":
        raise ValueError(f"Unsupported region units: {units}")

    left = max(0, min(width - 1, math.floor(x)))
    top = max(0, min(height - 1, math.floor(y)))
    right = max(left + 1, min(width, math.ceil(x + region_width)))
    bottom = max(top + 1, min(height, math.ceil(y + region_height)))
    return left, top, right, bottom


def region_record(
    image: Image.Image,
    region: dict[str, Any],
    palette_size: int,
) -> dict[str, Any]:
    box = resolve_region(region, image.width, image.height)
    crop = image.convert("RGBA").crop(box)
    pixel_source = (
        crop.get_flattened_data()
        if hasattr(crop, "get_flattened_data")
        else crop.getdata()
    )
    pixels = list(pixel_source)

    count = len(pixels)
    average = tuple(
        round(sum(pixel[channel] for pixel in pixels) / count)
        for channel in range(4)
    )
    center = tuple(
        int(value)
        for value in crop.getpixel(
            (max(0, crop.width // 2), max(0, crop.height // 2))
        )
    )

    return {
        "name": region["name"],
        "box": list(box),
        "size": [crop.width, crop.height],
        "average": color_record(average),
        "center": color_record(center),
        "dominant_colors": dominant_colors(crop, palette_size),
    }


def load_regions(path: Path | None) -> list[dict[str, Any]]:
    if path is None:
        return []
    payload = json.loads(path.read_text(encoding="utf-8"))
    regions = payload.get("regions")
    if not isinstance(regions, list):
        raise ValueError("Region config must contain a 'regions' array.")
    return regions


def save_normalized_png(
    image: Image.Image,
    output: Path,
    icc_profile: bytes | None,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    kwargs: dict[str, Any] = {"format": "PNG", "optimize": False}
    if icc_profile:
        kwargs["icc_profile"] = icc_profile
    image.convert("RGBA").save(output, **kwargs)


def main() -> int:
    parser = ArgumentParser()
    parser.add_argument("image", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--normalized-png", type=Path)
    parser.add_argument("--regions", type=Path)
    parser.add_argument("--palette-size", type=int, default=16)
    parser.add_argument("--region-palette-size", type=int, default=5)
    parser.add_argument("--grid-size", type=int, default=9)
    args = parser.parse_args()

    try:
        source_bytes = args.image.read_bytes()
        regions = load_regions(args.regions)

        with Image.open(io.BytesIO(source_bytes)) as source:
            source.load()
            raw = source.copy()
            exif = source.getexif()
            orientation = int(exif.get(274, 1))
            normalized = ImageOps.exif_transpose(source).copy()

            icc_profile = source.info.get("icc_profile")
            if icc_profile is not None and not isinstance(icc_profile, bytes):
                icc_profile = bytes(icc_profile)

            alpha = normalized.convert("RGBA").getchannel("A")
            alpha_extrema = alpha.getextrema()

            manifest = {
                "schema": "evidence-first/reference-image-manifest/v1",
                "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
                "source": {
                    "filename": args.image.name,
                    "path": args.image.as_posix(),
                    "bytes": len(source_bytes),
                    "sha256": sha256_bytes(source_bytes),
                    "format": source.format,
                    "mime_type": Image.MIME.get(source.format or ""),
                    "mode": source.mode,
                    "raw_dimensions": [source.width, source.height],
                    "exif_orientation": orientation,
                    "exif_orientation_name": ORIENTATION_NAMES.get(
                        orientation, "unknown"
                    ),
                },
                "normalized": {
                    "mode": "RGBA",
                    "dimensions": [normalized.width, normalized.height],
                    "orientation_applied": orientation != 1,
                    "raw_decoded_pixel_sha256": pixel_hash(raw),
                    "normalized_pixel_sha256": pixel_hash(normalized),
                    "has_alpha": "A" in normalized.getbands(),
                    "alpha_extrema": list(alpha_extrema),
                },
                "color_profile": {
                    "icc_present": bool(icc_profile),
                    "icc_bytes": len(icc_profile or b""),
                    "icc_sha256": (
                        sha256_bytes(icc_profile) if icc_profile else None
                    ),
                    "icc_description": (
                        get_icc_description(icc_profile)
                        if icc_profile
                        else None
                    ),
                },
                "dominant_colors": dominant_colors(
                    normalized,
                    args.palette_size,
                ),
                "grid_samples": grid_samples(normalized, args.grid_size),
                "regions": [
                    region_record(
                        normalized,
                        region,
                        args.region_palette_size,
                    )
                    for region in regions
                ],
                "usage": {
                    "instruction": (
                        "Give this manifest and the normalized lossless PNG "
                        "to the agent before any resized or multimodal preview."
                    ),
                    "do_not_replace_source": True,
                },
            }

            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(
                json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )

            if args.normalized_png:
                save_normalized_png(
                    normalized,
                    args.normalized_png,
                    icc_profile,
                )

        print(f"Manifest: {args.output}")
        if args.normalized_png:
            print(f"Normalized PNG: {args.normalized_png}")
        print(f"Source SHA-256: {manifest['source']['sha256']}")
        print(
            "Normalized pixel SHA-256: "
            f"{manifest['normalized']['normalized_pixel_sha256']}"
        )
        print(
            f"Dominant colors: {len(manifest['dominant_colors'])}, "
            f"grid samples: {len(manifest['grid_samples'])}, "
            f"regions: {len(manifest['regions'])}"
        )
        return 0
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
