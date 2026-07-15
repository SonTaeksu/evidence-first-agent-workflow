# Pre-commit Validation

Run the full gate before a release commit.

```powershell
./scripts/pre-commit-validate.ps1
```

```bash
./scripts/pre-commit-validate.sh
```

## Non-runtime governance and tool gates

- agent configuration and thin-adapter validation;
- Python tool compilation;
- stack-readiness pass/fail self-test;
- React + ASP.NET Core stack readiness;
- state-model pass/fail self-test;
- sample state-model validation;
- build-log pass/fail self-test;
- Reference Image Manifest and ΔE self-test;
- SPA grid and visual-block completeness self-test.

## Application gates

- frontend install, static color, type check, tests, build;
- backend restore, build, tests;
- Playwright E2E;
- runtime axe and computed-color evidence;
- Docker build unless explicitly skipped.

Docker skip:

```powershell
./scripts/pre-commit-validate.ps1 -SkipDocker
```

```bash
SKIP_DOCKER=1 ./scripts/pre-commit-validate.sh
```

A skipped gate remains PENDING.

## Source evidence helpers

```powershell
./scripts/create-reference-image-manifest.ps1 -Image C:\reference\design.png
./scripts/create-spa-screen-spec.ps1 -Source C:\reference\mockup.html
```
