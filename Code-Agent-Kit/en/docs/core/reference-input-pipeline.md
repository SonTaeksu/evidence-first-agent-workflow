# Reference Input Pipeline

## Image input

```text
Original file
→ byte hash and metadata
→ EXIF orientation normalization
→ ICC and decoded-pixel hashes
→ palette, pixel grid, and named regions
→ lossless normalized PNG
→ LLM input
```

The multimodal preview is a convenience view, not the source of truth.

## Rendered implementation

```text
Browser DOM
→ computed-color evidence
→ axe contrast result
→ optional pixel baseline
→ reference-region comparison
```

## SPA HTML input

```text
Original SPA package
→ source-file hash
→ installed browser or Playwright render
→ rendered-DOM hash
→ grids, columns, sample rows, forms, and buttons
→ worklog screen specification
→ implementation extraction
→ deterministic completeness comparison
```

Use `tools/spa-screen-extractor/`. The complete SPA source should leave routine model context after the specification has been fixed.
