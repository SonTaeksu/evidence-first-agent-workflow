# Pre-commit Validation Report

**English** | [한국어](PRE-COMMIT-VALIDATION.ko.md)

- Release candidate: `v0.1.6-alpha`
- Date: `2026-07-14`
- Status: **PARTIAL — local or CI application gates remain**

## Passed in the generation environment

| Gate | Result |
|---|---|
| Agent configuration and thin-adapter validation | PASS |
| MCP JSON/TOML structure | PASS |
| Python workflow-tool compilation | PASS |
| React + ASP.NET Core stack readiness | PASS |
| Stack-readiness ready/blocked self-test | PASS |
| Sample feature-state model | PASS |
| State-model pass/fail self-test | PASS |
| Build-log pass/fail self-test | PASS |
| Reference Image Manifest and ΔE comparison | PASS |
| SPA grid, form, button, and visual-block extraction | PASS |
| Missing-column failure behavior | PASS — exit code 2 |
| Empty visual-block failure behavior | PASS — exit code 2 |
| Browser-console JavaScript syntax | PASS |
| Portable Kit mirror path parity | PASS — EN/KO identical paths |
| Portable Kit self-contained links | PASS — 0 errors |
| `.ko.md` suffix removal | PASS — 0 files |
| Static CSS contrast baseline | PASS — 18/18 |
| Markdown local links | PASS — 0 errors |
| JSON/TOML/YAML syntax | PASS — 0 errors |
| Korean documentation coverage | PASS — 211/211 |
| Sensitive/private scan | PASS — 0 matches |

## Previously verified frontend baseline

The last executed frontend type check, Vitest, and Vite build passed in v0.1.3. Version 0.1.5 changes governance, tools, documents, and package metadata but does not claim a fresh frontend PASS until `npm ci` and the commands run again.

## Still required before the release commit

| Gate | State | Reason |
|---|---|---|
| v0.1.6 frontend npm ci/lint/test/build | PENDING | requires complete npm dependency access |
| ASP.NET Core restore/build/test | PENDING | .NET SDK unavailable in generation environment |
| Normal Playwright runtime E2E | PENDING | browser runtime blocked in generation environment |
| Runtime axe and computed colors | PENDING | browser runtime blocked |
| Docker build and smoke test | PENDING | Docker unavailable |
| Approved screenshot baselines | OPTIONAL/PENDING | require human visual approval |

## Required local command

```powershell
npx playwright install chromium
./scripts/pre-commit-validate.ps1
```

Use `-SkipDocker` only when Docker is intentionally unavailable and keep Docker recorded as PENDING.

## Commit decision

A work-in-progress commit may record these changes. Do not describe the release as fully validated until the required local or CI application gates pass.
