# Frontend Validation

Required:

```bash
npm run lint
npm run test
npm run build
```

For UI behavior:

```bash
npm run e2e
```

Evidence:

- command and exit code;
- test summary;
- production-build result;
- screenshot or Playwright result for layout changes;
- final frontend diff.

## Deterministic color gate

```bash
npm run e2e:color
```

Required after color, background, typography, badge, button, or theme changes.
