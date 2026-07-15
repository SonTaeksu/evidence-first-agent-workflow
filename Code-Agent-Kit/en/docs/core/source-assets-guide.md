# Source Assets Guide

## Authority by asset type

For UI structure and behavior:

```text
Rendered HTML or SPA
→ reference image
→ prose description
```

For exact image-specific color evidence, the original image file and its manifest remain authoritative.

Conflicts must be reported rather than silently blended.

## Common rules

- Preserve the original file unchanged.
- Record a hash before model ingestion.
- Do not replace an unread source with a summary invented by the model.
- Separate extraction from implementation.
- Store extracted evidence in the worklog.
- Do not repeatedly load a large source after evidence has been fixed.

## Static HTML

- Preserve DOM, CSS, visible text, and scripts as evidence.
- Read large files in bounded sections.
- Search for style, data, table, form, and script regions first.
- Do not rewrite the full original file merely to inspect it.
- Replace mock data with explicit binding points while preserving UI structure.

## SPA HTML

Raw SPA source may contain only an empty mount element.

Required process:

1. launch or open the SPA;
2. wait for the useful UI to render;
3. save the rendered DOM when possible;
4. run `tools/spa-screen-extractor/extract_spa.py`;
5. store screen-spec Markdown and JSON;
6. put blocks, grids, columns, rows, controls, and buttons into the worklog;
7. remove the complete SPA source from routine model context;
8. extract the implemented application and run `check_screen_spec.py`.

Console and PowerShell fallbacks are documented in the tool README.

## Images

Required process:

1. keep the exact original bytes;
2. create a Reference Image Manifest;
3. preserve ICC, EXIF orientation, file hash, decoded-pixel hash, palette, grid samples, and named regions;
4. provide the manifest and normalized lossless PNG before any platform preview;
5. use runtime computed-color and ΔE00 comparison when exact color matters.

The Code Agent Kit palette scripts remain available only as backup.

## Security

Do not commit confidential customer assets to a public repository. Generated evidence can still contain text and colors from the source and must follow the same confidentiality rules.
