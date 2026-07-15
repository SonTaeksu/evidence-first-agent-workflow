---
area: system
status: stable
code-verified: "2026-07-14 @uncommitted-release-candidate"
updated: "2026-07-14T00:00:00Z"
---

# System Architecture Current State

## Current Structure

```text
React/Vite Frontend
→ JSON REST
→ ASP.NET Core Minimal API
→ Domain Transition Rule
→ In-memory Repository
```

## 적용 중인 Decision

- Frontend API Module 하나 사용
- Sample Backend Minimal API 유지
- UI와 API Contract 변경 동기화
- Authentication 및 Production Persistence는 Owner Decision 필요

## 영향 Feature

- task-flow

## Validation 및 Evidence

- Frontend 기준선 PASS
- Backend Runtime PENDING
- E2E PENDING
