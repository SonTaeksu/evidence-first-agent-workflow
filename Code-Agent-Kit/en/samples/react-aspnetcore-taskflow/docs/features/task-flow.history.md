# Feature History — Task Flow

> Append-only. Corrections are new entries.

## 2026-07-14 / TASKFLOW-BASELINE / State model migration

### Type

change

### Version Control

- Baseline: v0.1.4 working tree
- Branch: not recorded
- Commit: uncommitted release candidate
- Pull request: none

### Change

- Created a persistent feature current document.
- Created append-only feature history.
- Added capability decisions, related files by role, shared dependencies, and layered validation.

### Reason

Restore the original current/history/worklog responsibilities and make Task Flow modifications start from verified feature state.

### Evidence and Provenance

- Existing source and project history
- React and ASP.NET Core stack readiness profile
- Workflow concept ledger

### Impact

- Affected features: task-flow
- Shared files: project map and project current
- Required regression: documentation validation and later full sample validation

### Validation

- Artifact / Compile: baseline only
- Rendered Output: tool self-tests PASS
- Runtime Behavior: PENDING
- Accessibility / Color: static PASS, runtime PENDING

### State Synchronization

- Current updated: yes
- Project Map updated: yes
- Worklog archived: not applicable

### Final State

Task Flow now has a persistent feature-level starting state.
