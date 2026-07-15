# History

> Append-only project-level history. Feature details belong in `features/*.history.md`. Corrections are new entries.

## 2026-07-13 / SAMPLE-001 / Initial TaskFlow sample

### Type

feature

### Change

- Added a React + TypeScript frontend.
- Added an ASP.NET Core minimal API.
- Added controlled task-status transitions.
- Added backend, frontend, and E2E test sources.
- Added project-scoped MCP configuration at repository root.
- Added validation scripts and state documents.

### Reason

Provide a mainstream, reproducible first sample for public evaluation of the workflow.

### Evidence

- Source files generated.
- Public MCP endpoints documented.
- Local/CI build evidence still required.

### Impact

- `frontend/**`
- `backend/**`
- `docs/**`
- `scripts/**`
- repository stack profile

### Validation

- Source structure: PASS
- Frontend TypeScript check: PASS
- Frontend component test: PASS
- Frontend production build: PASS
- Backend build: PENDING
- Backend tests: PENDING
- E2E: PENDING

### Failure Categories

- ENVIRONMENT: .NET SDK unavailable in the generation environment.

### Final State

The sample is structurally complete but must not be described as validated until local or CI commands pass.## 2026-07-13 / SAMPLE-002 / Multi-agent setup and deterministic color gate

### Type

feature

### Change

- Added Codex, Roo Code, Zoo Code, Cline, and Claude Code project guidance.
- Added shared Microsoft Learn and Context7 MCP examples.
- Added static CSS contrast validation.
- Added Playwright axe `color-contrast` and computed-color evidence tests.
- Added optional Playwright visual baseline tests.
- Corrected two text colors found below the 4.5:1 configured threshold.

### Evidence

- Agent configuration validation: PASS
- Static color checks: PASS 18/18
- TypeScript check: PASS
- Vitest: PASS
- Production build: PASS
- Playwright test discovery: PASS
- Browser runtime: PENDING because the generation environment blocks navigation with `ERR_BLOCKED_BY_ADMINISTRATOR`
- Backend: PENDING because .NET SDK is not installed in the generation environment

### Impact

- root agent configuration files
- `.roo/**`
- `.clinerules/**`
- `.mcp.json`
- `CLAUDE.md`
- `agent-configs/**`
- `tools/check-agent-config/**`
- `tools/ui-color-gate/**`
- frontend color and visual E2E tests

### Final State

Non-browser deterministic validation passes. Runtime browser, backend, and Docker gates must run locally or in CI before commit.

## 2026-07-13 / SAMPLE-003 / Reference image preservation pipeline

### Type

feature

### Change

- Added pre-multimodal image evidence generation.
- Added original byte hash, ICC, EXIF orientation, decoded-pixel hashes, dominant colors, pixel grid, and named region extraction.
- Added an orientation-normalized lossless PNG.
- Added ΔE00 comparison between named reference regions and browser computed-color evidence.
- Added a passing and intentionally failing self-test.
- Reserved the SPA HTML branch until a representative prepared SPA package is supplied.

### Validation

- Reference-image manifest self-test: PASS
- ICC and normalized-pixel preservation test: PASS
- Region extraction test: PASS
- Reference/runtime exact color comparison: PASS
- Intentional mismatch: PASS — comparison returned exit code 2
- Frontend TypeScript, Vitest, and production build after integration: PASS

### Final State

Design images can now be converted into structured evidence before platform preview transformation. SPA HTML handling remains deliberately deferred.

## 2026-07-14 / SAMPLE-004 / Code Agent Kit operational integration

### Type

feature

### Change

- Added rendered SPA DOM extraction with installed-browser, Playwright, console, and saved-DOM paths.
- Added rendered-DOM and source-file hashes.
- Added generic reference-versus-implementation screen completeness checks.
- Added prompt router, mandatory Gate, worklog Resume Point, demo isolation, and `.agentignore`.
- Added human-guide and agent-rule separation.
- Upgraded Git scope checks with acknowledged files and no-Git fallback.
- Added optional stack `SKILL.md` routing.
- Kept the existing image manifest as primary and preserved the Code Agent Kit palette scripts as backup.

### Validation

- SPA rendered-DOM extraction self-test: PASS
- Grid, column, sample-row, form, and button extraction: PASS
- Screen completeness pass behavior: PASS
- Intentional missing-column behavior: PASS, exit code 2
- Developer-guide static extraction: PASS
- Code Agent Kit backup palette extraction: PASS
- Python compilation and agent-configuration checks: PASS

### Final State

The previously deferred SPA branch is implemented. Stack-specific validators from the original Kit remain outside the generic workflow core.

## 2026-07-14 / SAMPLE-005 / Restore state and design-intent model

### Type

change

### Version Control

- Baseline: v0.1.4 working tree
- Branch: not recorded
- Commit: uncommitted release candidate
- Pull request: none

### Change

- Added the public design-concepts ledger and architecture decisions.
- Restored feature current, append-only feature history, and temporary worklog responsibilities.
- Added project feature routing, shared-file reverse index, architecture state, stack inputs, and readiness validation.
- Slimmed agent adapters to pointers.
- Added visual-block empty detection and layered validation.

### Reason

Prevent concept loss during session handoff and make stack-dependent user inputs explicit.

### Evidence

- DESIGN-CONCEPTS ledger
- Stack readiness self-test
- SPA visual-block self-test
- Concept preservation audits

### Affected Features and Architecture

- task-flow
- project state model
- stack-extension architecture

### Validation

- Tool self-tests: PASS
- Public package and full runtime validation: pending final release checks

### State Synchronization

- Project current: updated
- Feature current/history: added
- Project Map: updated
