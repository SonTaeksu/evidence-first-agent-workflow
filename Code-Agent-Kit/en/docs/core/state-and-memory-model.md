# State and Memory Model

## Document roles

| Document | Lifetime | Purpose |
|---|---|---|
| Project Map | project | Route to features, architecture state, capabilities, and shared dependencies |
| Feature current | persistent and mutable | Verified state used at the start of every later modification |
| Feature history | persistent and append-only | Human-readable index over commits and PRs |
| Feature worklog | temporary while active | Gate progress, Todo state, evidence, and Resume Point |
| Architecture current/history | project | System and database decisions that affect multiple features |

## Required start order

An active worklog identifies the unfinished task, but current state still must be read before implementation.

```text
worklog header
→ Git
→ Project Map
→ feature current
→ current Related Files
→ full worklog
→ resume
```

New work on a completed feature:

```text
Git
→ Project Map
→ feature current
→ Related Files
→ new worklog
→ Analysis
```

## Current state

Current contains only verified present state. It records:

- code-verified commit;
- last PR when available;
- behavior and contracts;
- files by role;
- shared dependencies;
- capability decisions;
- three-layer validation state;
- known issues;
- next candidate work.

## History

History is append-only.

- Never delete or silently edit a prior entry.
- A correction is a new entry referring to the incorrect entry.
- Record commit, PR, evidence, validation, impact, and shared-file regression.

## Worklog lifecycle

```text
create
→ update through Gate
→ complete
→ reflect verified results into current/history/Project Map
→ archive or close
```

An archived worklog is evidence of execution, not the starting state for a later feature change.
