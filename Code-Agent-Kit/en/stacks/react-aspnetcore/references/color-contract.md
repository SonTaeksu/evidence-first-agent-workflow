# Color and theme contract (React + ASP.NET Core)

Goal: reproduce a **reference screenshot** (e.g. a WinForms ERP screen) faithfully in React.
The reference is the **source of truth** — do not invent a theme, do not fall back to a
framework default palette (no Bootstrap blue, no Tailwind default surfaces).

## 1. Extract, do not eyeball

Run **both** manifest tools on the reference image (a vision model sees a preprocessed
image, so hand-picked hex is unreliable):

```bash
# role-mapped palette (which color is background / line / text / accent / status)
python tools/reference-image-manifest/extract_palette.py <ref.png> --colors 16 \
  --regions "x,y,w,h=header; x,y,w,h=primaryButton"

# exact evidence: hashes, ICC, dominant colors, normalized PNG (for ΔE comparison)
python tools/reference-image-manifest/extract_reference_image.py --image <ref.png> ...
```

`extract_palette` gives the **role mapping** you bind to the UI; `extract_reference_image`
gives the **ΔE evidence** you verify against. Use both.

## 2. Bind the extracted colors to tokens

Write the extracted hex values into **CSS variables** (one tokens file, e.g.
`src/styles/tokens.css` `:root { --color-... }`). Components reference **tokens only** —
no ad-hoc hex, no framework default theme for themable surfaces.

| Role | Token | Source |
|---|---|---|
| Page background | `--bg` | palette achromatic (light) |
| Surface / panel | `--surface` | palette achromatic |
| Border / grid line | `--line` | palette achromatic (gray) |
| Text / muted text | `--text` / `--text-muted` | palette achromatic |
| Accent / primary | `--accent` | palette chromatic (dominant chroma) |
| Status | `--status-red/-yellow/-green` | status convention (R/Y/G) |

## 3. Verify — hard gate (completion is blocked on mismatch)

- **ΔE reference match:** `python tools/reference-image-manifest/compare_manifest_to_runtime.py` — rendered computed colors vs the reference palette; fail if ΔE00 exceeds the threshold.
- **Runtime color gate:** the Playwright `e2e/color-gate.spec.ts` asserts key elements (header, primary button, grid line, status chips) resolve to the **token** colors within tolerance.
- **Default-theme guard:** flag if themable surfaces use framework-default colors instead of tokens.

A build that compiles or a screen that renders is **not** color fidelity — that is a
separate layer (`docs/core/validation-layers.md`). Record the color layer separately.
