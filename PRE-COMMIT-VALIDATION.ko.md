# 커밋 전 Validation 보고서

[English](PRE-COMMIT-VALIDATION.md) | **한국어**

- Release Candidate: `v0.1.6-alpha`
- 날짜: `2026-07-14`
- 상태: **부분 완료 — Local 또는 CI Application Gate가 남음**

## 생성 환경에서 통과

| Gate | 결과 |
|---|---|
| Agent 설정 및 얇은 Adapter 검사 | PASS |
| MCP JSON/TOML 구조 | PASS |
| Python Workflow Tool Compile | PASS |
| React + ASP.NET Core Stack Readiness | PASS |
| Stack Readiness Ready/Blocked Self-test | PASS |
| Sample Feature State Model | PASS |
| State Model 정상/실패 Self-test | PASS |
| Build Log 정상/실패 Self-test | PASS |
| Reference Image Manifest 및 ΔE 비교 | PASS |
| SPA Grid, Form, Button, Visual Block 추출 | PASS |
| Missing Column 실패 동작 | PASS — Exit Code 2 |
| Empty Visual Block 실패 동작 | PASS — Exit Code 2 |
| Browser Console JavaScript Syntax | PASS |
| Portable Kit Mirror 경로 일치 | PASS — EN/KO 동일 경로 |
| Portable Kit 자체 포함 Link | PASS — 0개 오류 |
| `.ko.md` 접미사 제거 | PASS — 0개 |
| 정적 CSS Contrast 기준선 | PASS — 18/18 |
| Markdown Local Link | PASS — 0개 오류 |
| JSON/TOML/YAML Syntax | PASS — 0개 오류 |
| 한국어 문서 Coverage | PASS — 211/211 |
| 민감/Private Scan | PASS — 0개 |

## 이전 Frontend 기준선

마지막으로 실행한 Frontend Type Check, Vitest, Vite Build는 v0.1.3에서 PASS했습니다. v0.1.5는 Governance, Tool, 문서, Package Metadata를 변경하지만 `npm ci`와 명령을 다시 실행하기 전에는 새 Frontend PASS라고 주장하지 않습니다.

## Release Commit 전 남은 항목

| Gate | 상태 | 이유 |
|---|---|---|
| v0.1.6 Frontend npm ci/lint/test/build | PENDING | 완전한 npm Dependency 접근 필요 |
| ASP.NET Core Restore/Build/Test | PENDING | 생성 환경에 .NET SDK 없음 |
| 일반 Playwright Runtime E2E | PENDING | 생성 환경 Browser Runtime 차단 |
| Runtime axe 및 Computed Color | PENDING | Browser Runtime 차단 |
| Docker Build 및 Smoke Test | PENDING | Docker 없음 |
| 승인 Screenshot Baseline | 선택/PENDING | 사람의 Visual 승인 필요 |

## Local 필수 명령

```powershell
npx playwright install chromium
./scripts/pre-commit-validate.ps1
```

Docker를 의도적으로 사용할 수 없을 때만 `-SkipDocker`를 사용하고 Docker는 PENDING으로 유지합니다.

## Commit 판정

Work-in-progress Commit은 가능합니다. 필수 Local 또는 CI Application Gate가 통과하기 전에는 Release가 완전히 검증됐다고 설명하면 안 됩니다.
