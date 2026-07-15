# 이력

> Append-only Project-level History입니다. Feature 상세는 `features/*.history.md`에 둡니다. Correction은 새 Entry입니다.

## 2026-07-13 / SAMPLE-001 / 최초 TaskFlow 샘플

### 유형

feature

### 변경 내용

- React + TypeScript Frontend를 추가했습니다.
- ASP.NET Core Minimal API를 추가했습니다.
- 통제된 작업 Status Transition을 추가했습니다.
- Backend, Frontend, E2E Test 소스를 추가했습니다.
- 저장소 Root에 프로젝트 범위 MCP 설정을 추가했습니다.
- Validation Script와 상태 문서를 추가했습니다.

### 변경 이유

워크플로우 공개 검증에 사용할 수 있는 주류 기술 기반의 재현 가능한 첫 샘플을 제공하기 위해서입니다.

### 증거

- 소스 파일 생성 완료
- 공개 MCP Endpoint 문서화 완료
- 로컬 또는 CI Build 증거는 아직 필요함

### 영향

- `frontend/**`
- `backend/**`
- `docs/**`
- `scripts/**`
- 저장소 Stack Profile

### Validation

- Source Structure: PASS
- Frontend TypeScript 검사: PASS
- Frontend Component Test: PASS
- Frontend Production Build: PASS
- Backend Build: PENDING
- Backend Tests: PENDING
- E2E: PENDING

### 실패 분류

- ENVIRONMENT: 생성 환경에 .NET SDK가 없음

### 최종 상태

샘플 구조는 완성됐지만 로컬 또는 CI 명령이 통과하기 전까지 완전히 검증됐다고 표현하면 안 됩니다.## 2026-07-13 / SAMPLE-002 / 다중 에이전트 설정과 결정론적 색상 게이트

### 유형

feature

### 변경 내용

- Codex, Roo Code, Zoo Code, Cline, Claude Code용 프로젝트 지침을 추가했습니다.
- Microsoft Learn 및 Context7 MCP 공통 설정 예제를 추가했습니다.
- 정적 CSS Contrast Validation을 추가했습니다.
- Playwright axe `color-contrast`와 Computed Color 증거 Test를 추가했습니다.
- 선택형 Playwright Visual Baseline Test를 추가했습니다.
- 4.5:1 설정 기준에 못 미치던 문자 색상 두 곳을 수정했습니다.

### 증거

- 에이전트 설정 검사: PASS
- 정적 색상 검사: PASS 18/18
- TypeScript 검사: PASS
- Vitest: PASS
- Production Build: PASS
- Playwright Test 목록 및 구문 확인: PASS
- Browser Runtime: 생성 환경의 `ERR_BLOCKED_BY_ADMINISTRATOR` 정책으로 PENDING
- Backend: 생성 환경에 .NET SDK가 없어 PENDING

### 영향

- Root 에이전트 설정 파일
- `.roo/**`
- `.clinerules/**`
- `.mcp.json`
- `CLAUDE.md`
- `agent-configs/**`
- `tools/check-agent-config/**`
- `tools/ui-color-gate/**`
- Frontend 색상 및 Visual E2E Test

### 최종 상태

Browser가 필요하지 않은 결정론적 Validation은 통과했습니다. 커밋 전에 로컬 또는 CI에서 Browser, Backend, Docker Gate를 실행해야 합니다.

## 2026-07-13 / SAMPLE-003 / Reference Image 보존 Pipeline

### 유형

feature

### 변경 내용

- 멀티모달 변환 이전의 Image Evidence 생성을 추가했습니다.
- 원본 Byte Hash, ICC, EXIF 방향, Decoded Pixel Hash, 주요 색상, Pixel Grid, 이름 있는 영역 추출을 추가했습니다.
- 방향 보정 무손실 PNG를 추가했습니다.
- 이름 있는 Reference 영역과 Browser Computed Color 증거의 ΔE00 비교를 추가했습니다.
- 정상 통과와 의도적 불일치 실패 자체 검사를 추가했습니다.
- 대표 SPA Package가 준비될 때까지 SPA HTML 분기를 예약 상태로 두었습니다.

### Validation

- Reference Image Manifest 자체 검사: PASS
- ICC 및 정규화 Pixel 보존 검사: PASS
- 영역 추출 검사: PASS
- Reference/Runtime 정확 색상 비교: PASS
- 의도적 불일치: PASS — 비교 도구가 종료 코드 2 반환
- 통합 후 Frontend TypeScript, Vitest, Production Build: PASS

### 최종 상태

디자인 이미지를 플랫폼 Preview 변형 이전에 구조화 Evidence로 고정할 수 있습니다. SPA HTML 처리는 의도적으로 보류 상태입니다.

## 2026-07-14 / SAMPLE-004 / Code Agent Kit 운영 기능 통합

### 유형

feature

### 변경 내용

- 설치 Browser, Playwright, Console, 저장된 DOM 방식의 Rendered SPA DOM 추출을 추가했습니다.
- Rendered DOM 및 Source File Hash를 추가했습니다.
- Generic Reference/Implementation 화면 완전성 검사를 추가했습니다.
- Prompt Router, 필수 Gate, Worklog Resume Point, Demo 격리, `.agentignore`를 추가했습니다.
- 사람용 Guide와 Agent Rule 경계를 추가했습니다.
- Git Scope 검사에 인정 파일과 Git 없는 환경 Fallback을 추가했습니다.
- 선택형 Stack `SKILL.md` Routing을 추가했습니다.
- 기존 Image Manifest를 Primary로 유지하고 Code Agent Kit Palette Script를 Backup으로 보존했습니다.

### Validation

- SPA Rendered DOM 추출 자체 검사: PASS
- Grid, Column, Sample Row, Form, Button 추출: PASS
- 화면 완전성 정상 통과: PASS
- 의도적 Column 누락: PASS, 종료 코드 2
- Developer Guide Static 추출: PASS
- Code Agent Kit Backup Palette 추출: PASS
- Python Compile 및 Agent 설정 검사: PASS

### 최종 상태

이전에 보류했던 SPA 분기를 구현했습니다. 원본 Kit의 Stack 전용 Validator는 Generic Workflow Core 밖에 유지합니다.

## 2026-07-14 / SAMPLE-005 / State 및 Design Intent Model 복원

### 유형

change

### Version Control

- Baseline: v0.1.4 Working Tree
- Branch: 기록 없음
- Commit: Uncommitted Release Candidate
- Pull Request: 없음

### 변경

- 공개 Design Concepts Ledger와 Architecture Decision 추가
- Feature Current, Append-only Feature History, 임시 Worklog 역할 복원
- Project Feature Routing, Shared File Reverse Index, Architecture State, Stack Input, Readiness Validation 추가
- Agent Adapter를 Pointer로 축소
- Visual Block Empty Detection 및 Layered Validation 추가

### 이유

Session Handoff 중 개념 손실을 막고 Stack 의존 사용자 입력을 명시하기 위함

### Evidence

- DESIGN-CONCEPTS Ledger
- Stack Readiness Self-test
- SPA Visual Block Self-test
- Concept Preservation Audit

### 영향 Feature 및 Architecture

- task-flow
- Project State Model
- Stack Extension Architecture

### Validation

- Tool Self-test: PASS
- Public Package 및 전체 Runtime Validation: 최종 Release 검사 PENDING

### State 동기화

- Project Current: 갱신
- Feature Current/History: 추가
- Project Map: 갱신
