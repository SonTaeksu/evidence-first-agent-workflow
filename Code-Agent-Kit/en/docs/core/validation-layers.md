# Validation Layers

Completion is not one boolean.

| Layer | Question | Typical Evidence |
|---|---|---|
| Artifact / Compile | Was a valid framework artifact produced? | compiler, generator, schema, build exit code |
| Rendered Output | Did the required structure and content appear? | screen specification, non-empty visual blocks, screenshot baseline |
| Runtime Behavior | Does the feature work with real interactions and contracts? | integration tests, E2E, runtime logs |
| Accessibility / Color | Is the rendered result readable and comparable to the reference? | axe, computed colors, contrast, ΔE00 |

A feature can have:

```text
Artifact PASS
Rendered Output FAIL
Runtime PENDING
```

That feature is not complete.

Stacks may add layers but must not collapse these distinctions when they apply.
