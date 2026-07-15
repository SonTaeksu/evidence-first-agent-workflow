---
area: database
status: provisional
code-verified: "2026-07-14 @uncommitted-release-candidate"
updated: "2026-07-14T00:00:00Z"
---

# Database Architecture Current State

## Current Structure

- No external database.
- `InMemoryTaskRepository` owns sample persistence.
- Data resets on API restart.

## Decisions in Force

- Do not infer EF Core, Dapper, schema, migrations, or production database.
- Database adoption is blocked until an owner confirms provider, lifecycle, migration, and operational constraints.

## Affected Features

- task-flow
