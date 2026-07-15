# SPA HTML Reference

Place original SPA packages here only in private project repositories. Public workflow repositories should keep confidential assets outside Git.

## Process

1. Preserve the original package.
2. Record the source-file hash.
3. Render with an installed browser or Playwright.
4. Save rendered DOM when policy allows.
5. Run `tools/spa-screen-extractor/extract_spa.py`.
6. Store `screen-spec.md` and `screen-spec.json`.
7. Copy the extracted blocks, grids, columns, sample rows, forms, and buttons into the active worklog.
8. Remove the full SPA source from routine model context.
9. Extract the implementation and compare specifications before completion.

PowerShell:

```powershell
./scripts/create-spa-screen-spec.ps1 `
  -Source "C:\reference\mockup.html" `
  -Wait 3000
```

Headless execution can fall back to `extract_screen.js` in the browser console.
