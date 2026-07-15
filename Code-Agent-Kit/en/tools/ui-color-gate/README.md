# UI Color Gate

This gate externalizes UI color judgment so a smaller model does not need to infer color correctness from an image.

## Included checks

### 1. Color contrast gate

`@axe-core/playwright` runs the `color-contrast` rule against the rendered page.

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm run e2e:color
```

A contrast violation causes a non-zero exit code.

### 2. Computed color evidence

The same test exports the rendered values of:

- `color`
- `background-color`
- `border-color`
- font size
- font weight
- a short text sample
- a stable selector hint

The JSON attachment can be given to a smaller LLM instead of asking it to guess colors from a screenshot.

### 3. Optional visual baseline gate

```bash
npm run e2e:visual
```

Playwright compares desktop and narrow screenshots against approved baselines. Baselines must be reviewed before commit. Visual snapshots may vary across operating systems and browser versions, so CI should use a pinned Playwright browser environment.

## Boundaries

Automated contrast testing cannot detect every accessibility or design defect. A passing contrast gate does not prove that colors match a designer's intended palette. Use the visual baseline for exact appearance and human review for brand decisions.
