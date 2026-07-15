# Deterministic UI Gates

UI validation is split into three layers.

1. **Structure and behavior**: Playwright locators, status transitions, scrolling, and viewport checks.
2. **Color and accessibility**: axe `color-contrast` plus computed-color evidence.
3. **Exact appearance**: approved Playwright screenshot baselines.

The second layer is especially important for smaller models. The model is given structured rendered evidence and a pass/fail result instead of being asked to visually judge CSS color.

Run:

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm run e2e:color
```

Color, theme, badge, button, typography, or background changes cannot pass DoD without this gate.
