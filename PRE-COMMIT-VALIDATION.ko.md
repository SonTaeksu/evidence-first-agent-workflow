# 커밋 전 Validation 보고서

[English](PRE-COMMIT-VALIDATION.md) | **한국어**

- Release Candidate: `v0.1.9-alpha`
- 날짜: `2026-08-04`
- 상태: **부분 완료 — Local 또는 CI Application Gate가 남음**

## 생성 환경에서 통과 — v0.1.9-alpha

| Gate | 결과 |
|---|---|
| Stack Readiness, `react-aspnetcore`, 양쪽 Mirror | PASS — exit 0 |
| Stack Readiness, `csharp-winforms`, 양쪽 Mirror | PASS — exit 0, 상태 READY |
| Kit Self-check, 양쪽 Mirror | PASS — exit 0, 두 Seed Template 모두 구조적 실패 없음 |
| Kit Self-check Self-test | PASS — 완전한 Seed 통과, 불완전한 Seed는 exit 2로 거부 |
| Mirror Parity, `en` vs `ko` | PASS — 각 327 경로, 고아 0, Shared Script 68개 Byte 동일, 경고 0 |
| Mirror Parity Self-test | PASS — 6/6 케이스 |
| 수치 주장 검증 | PASS — `mirrored_file_count` 327이 기록된 규칙의 실측과 일치 |
| Windows Forms Designer Tree Tool, 양쪽 Mirror | PASS — 14/14 케이스 |
| Kit Installation 검사, 양쪽 Mirror | PASS — exit 0 |
| Python 컴파일, 킷 전체 | PASS — 64개 File, 실패 0 |
| Sanitization Scan, 저장소 전체 | PASS — 689개 File, CLEAN, 경고 0 |
| 기존 Tool Self-test (state-model·build-log·stack-readiness·SPA extractor·reference-image) | PASS |

**합계: Gate 19개 실행, 실패 0.**

### 이번 릴리스가 수정한 결함과 발견 경로

| 결함 | 발견 주체 |
|---|---|
| `templates/stack-profile/`에 자기 Manifest가 요구하는 문서 누락 | 신규 Kit Self-check, 첫 실행 |
| `KIT-MANIFEST.json`의 File 개수가 어떤 규칙과도 불일치 | 신규 Mirror Parity 검사 |
| `docs/core/honesty-and-correction.md` (en) 문장 중간 절단 | 사람이 읽어서 발견. 이를 덮는 검사가 없음 |
| `enforcement-matrix.md`가 존재하지 않는 Tool 인용 | 사람이 읽어서 발견. 이를 덮는 검사가 없음 |

뒤의 두 건은 정직하게 기록합니다 — 네 건 중 두 건은 프로그램이 아니라 사람이 찾았습니다. 문서와 Tool 이름의 표류, 그리고 File 중간 절단은 현재 기계로 검사되지 않습니다.

## 생성 환경에서 통과 — v0.1.6-alpha 기준선

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
