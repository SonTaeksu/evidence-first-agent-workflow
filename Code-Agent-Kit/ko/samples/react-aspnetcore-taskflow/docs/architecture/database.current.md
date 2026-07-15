---
area: database
status: provisional
code-verified: "2026-07-14 @uncommitted-release-candidate"
updated: "2026-07-14T00:00:00Z"
---

# Database Architecture Current State

## Current Structure

- External Database 없음
- `InMemoryTaskRepository`가 Sample Persistence 담당
- API Restart 시 Data Reset

## 적용 중인 Decision

- EF Core, Dapper, Schema, Migration, Production Database를 추측하지 않음
- Owner가 Provider, Lifecycle, Migration, 운영 제약을 확인하기 전 Database 적용 Block

## 영향 Feature

- task-flow
