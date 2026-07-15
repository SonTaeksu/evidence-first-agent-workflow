# Feature Worklog and Handoff — Task Name

```yaml
feature: feature-key
current: docs/features/feature-key.current.md
status: in-progress
started: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SSZ
branch: feature/example
baseline: main-commit
last_commit: none
gate_stage: 1-analysis
```

> This is a temporary checkpoint. A new session uses the header to identify the feature, then reads Git, Project Map, and feature current before the full worklog.

## Resume Point

- Next action:
- Current Gate stage:
- Files to open after current:
- Evidence already extracted:
- Source assets that do not need to be read again:
- Blocking `⟨verification required⟩` items:

## 1. Analysis

- Request:
- Target feature:
- Project Map route:
- Feature current summary:
- Git baseline and incoming changes:
- Affected files:
- Shared-file impact:
- Assumptions:
- Unknowns:

### Environment Capability Decision

| Capability | Status | Evidence | Selected Path |
|---|---|---|---|
| | present / absent / unknown | | |

### Source Evidence and Provenance

- Original asset hashes:
- Official or primary sources:
- Reference image manifest:
- SPA screen specification:
- Blocks, grids, columns, and rows:
- Color regions:
- Contract mapping:

## 2. Task

- Objective:
- Acceptance criteria:
- Out of scope:
- Validation commands:

### Expected Files

- [ ]

### Acknowledged Unexpected Files

- [ ] path — reason, impact, and required regression

## 3. Todo and Micro-Verify

**Progress:** 0 / 0

- [ ] Todo 1
  - Change:
  - Micro-Verify command:
  - Result:
  - Failure action: repeat Todo / return to Analysis
- [ ] Todo 2
  - Change:
  - Micro-Verify command:
  - Result:
  - Failure action: repeat Todo / return to Analysis

## 4. Checklist

- [ ] Architecture and naming
- [ ] Contract synchronization
- [ ] Source fidelity
- [ ] Artifact, rendered output, and runtime are separately verified
- [ ] Color and accessibility evidence
- [ ] Error, loading, empty, and placeholder states
- [ ] Security and trust boundaries
- [ ] Shared-file reverse impact
- [ ] No unrelated changes
- [ ] Human guide was not treated as an agent rule

## 5. Verification

| Layer or Gate | Command | Exit | Result | Evidence |
|---|---|---:|---|---|
| Artifact / Compile | | | | |
| Unit / Integration | | | | |
| Rendered Output | | | | |
| Runtime Behavior / E2E | | | | |
| Screen-spec completeness | | | | |
| Color / Accessibility | | | | |
| Git scope | | | | |
| Document sync | | | | |

## Corrections, Decisions, and Pending Items

- Correction:
- Decision:
- PENDING:

## Completion

- [ ] Required validation passed
- [ ] Feature current updated with code-verified commit
- [ ] Append-only feature history entry added
- [ ] Project Map and Shared File Reverse Index updated
- [ ] Active worklog closed or archived
- [ ] Final Git Diff reviewed
- [ ] Next feature starts in a fresh chat
