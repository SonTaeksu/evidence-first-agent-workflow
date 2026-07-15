# Reference Image Manifest

Turn a reference screenshot into color/structure **evidence** before any multimodal
transformation. Two complementary tools — run both:

- **`extract_palette.py`** — role-mapped palette: which hex is background / surface / line / text / accent, with status colors held to the R/Y/G convention. Supports `--regions` for precise control colors (header, primary button). This is what you **bind to UI tokens**. (`.ps1` wrappers: `extract_palette_A.ps1`, `extract_palette_B.ps1`.)
- **`extract_reference_image.py`** — exact evidence: original/decoded hashes, ICC, EXIF, dominant colors, named regions, and a normalized lossless PNG. This is the **ΔE evidence** base.
- **`compare_manifest_to_runtime.py`** — ΔE00 comparison of runtime computed colors vs the reference palette (the color verification gate).

Flow: run both extractors on the reference → bind the `extract_palette` roles to CSS
variable tokens → verify the rendered result with `compare_manifest_to_runtime.py`.

For the binding rules and the hard color gate, see
`stacks/react-aspnetcore/references/color-contract.md`.
