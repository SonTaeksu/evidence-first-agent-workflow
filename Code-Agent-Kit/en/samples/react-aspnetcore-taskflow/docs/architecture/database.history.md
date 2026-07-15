# Database Architecture History

> Append-only.

## 2026-07-14 / DATA-BASELINE / Record intentional in-memory scope

- Commit: uncommitted release candidate
- Pull request: none
- Decision: retain in-memory storage for the public sample
- Reason: database choice is project-owner input, not a generic workflow assumption
- Evidence: repository implementation and stack capability profile
- Affected features: task-flow
- Required regression: backend tests when changed
