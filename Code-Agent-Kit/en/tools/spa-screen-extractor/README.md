# SPA Screen Extractor

The extractor reads the **rendered DOM**, not an empty SPA mount source.

## Extracted evidence

- grids, columns, sample rows, and approximate row count;
- forms and input controls;
- buttons and tabs;
- KPI, card, chart, matrix, and panel blocks;
- text/value/media/control presence;
- empty visual-block state;
- source-file and rendered-DOM SHA-256;
- rendering mode and wait time.

## Extract

Installed Edge, Chrome, or Chromium:

```powershell
python tools/spa-screen-extractor/extract_spa.py `
  --browser "C:\reference\mockup.html" `
  --wait 3000 `
  --json "reference-assets/evidence/mockup/screen-spec.json" `
  --out "reference-assets/evidence/mockup/screen-spec.md" `
  --save-dom "reference-assets/evidence/mockup/rendered.html"
```

Already captured rendered HTML:

```bash
python tools/spa-screen-extractor/extract_spa.py \
  --from-file rendered.html \
  --json screen-spec.json \
  --out screen-spec.md
```

Other supported paths:

- `--render`: Playwright, then installed-browser fallback;
- `--crawl`: bounded local HTML link traversal;
- `extract_screen.js`: browser-console fallback;
- `extract_screen.ps1`: lightweight PowerShell fallback.

## Completeness comparison

```bash
python tools/spa-screen-extractor/check_screen_spec.py \
  --reference reference-screen-spec.json \
  --implementation implementation-screen-spec.json \
  --require-rows \
  --strict-controls \
  --strict-visual-blocks \
  --reject-empty-visual-blocks \
  --output comparison.json
```

Exit code `2` is returned for missing grids, columns, rows, controls, buttons, visual blocks, type mismatches, or an implementation block that is empty while the reference is filled.

## Boundaries

Structural evidence is heuristic and stack-neutral. Stack validators may add binding, generated-file, or runtime-specific checks. Exact color evidence remains the responsibility of the Reference Image Manifest and UI Color Gate.

## Self-test

```bash
python tools/spa-screen-extractor/self_test.py
```

The self-test includes intentional missing-column and empty-visual-block failures.
