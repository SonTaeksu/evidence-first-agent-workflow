---
area: system
status: stable
code-verified: "2026-07-14 @uncommitted-release-candidate"
updated: "2026-07-14T00:00:00Z"
---

# System Architecture Current State

## Current Structure

```text
React/Vite frontend
→ JSON REST
→ ASP.NET Core Minimal API
→ domain transition rules
→ in-memory repository
```

## Decisions in Force

- Frontend uses one API module.
- Backend preserves Minimal API for the sample.
- UI and API contract changes are synchronized.
- Authentication and production persistence require owner decisions.

## Affected Features

- task-flow

## Validation and Evidence

- frontend baseline PASS;
- backend runtime PENDING;
- E2E PENDING.
