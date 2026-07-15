# 커밋 전 Validation

Release Commit 전에 전체 Gate를 실행합니다.

```powershell
./scripts/pre-commit-validate.ps1
```

```bash
./scripts/pre-commit-validate.sh
```

## Runtime이 필요 없는 Governance 및 Tool Gate

- Agent 설정 및 얇은 Adapter 검사
- Python Tool Compile
- Stack Readiness 정상/실패 Self-test
- React + ASP.NET Core Stack Readiness
- State Model 정상/실패 Self-test
- Sample State Model Validation
- Build Log 정상/실패 Self-test
- Reference Image Manifest 및 ΔE Self-test
- SPA Grid 및 Visual Block 완전성 Self-test

## Application Gate

- Frontend Install, Static Color, Type Check, Test, Build
- Backend Restore, Build, Test
- Playwright E2E
- Runtime axe 및 Computed Color Evidence
- 명시적으로 Skip하지 않으면 Docker Build

Docker Skip:

```powershell
./scripts/pre-commit-validate.ps1 -SkipDocker
```

```bash
SKIP_DOCKER=1 ./scripts/pre-commit-validate.sh
```

Skip된 Gate는 PENDING입니다.

## Source Evidence Helper

```powershell
./scripts/create-reference-image-manifest.ps1 -Image C:\reference\design.png
./scripts/create-spa-screen-spec.ps1 -Source C:\reference\mockup.html
```
