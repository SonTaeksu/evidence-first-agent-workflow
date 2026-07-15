# Code Agent Kit Palette Tools — Backup

These files are preserved from the user-provided Code Agent Kit as a fallback.

## Primary tool

Use `tools/reference-image-manifest/` first. It preserves:

- original file SHA-256;
- decoded-pixel SHA-256;
- ICC profile;
- EXIF orientation;
- lossless normalized PNG;
- palette and exact pixel grid;
- named regions;
- runtime ΔE00 comparison.

## Backup tools

- `extract_palette.py`: Pillow-based palette and region sampling
- `extract_palette_A.ps1`: lightweight region sampling with Windows `System.Drawing`
- `extract_palette_B.ps1`: automatic palette plus region sampling with Windows `System.Drawing`

Use the PowerShell variants when Python or Pillow cannot be installed in a closed Windows network. They are backup and cross-check tools, not replacements for the primary manifest.
