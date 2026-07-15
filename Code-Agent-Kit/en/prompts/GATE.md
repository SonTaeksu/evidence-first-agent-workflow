# Mandatory Execution Gate

Every file-producing task must use the five headings below **without renaming or omitting them**. Empty required sections mean implementation cannot begin or completion cannot be claimed.

```text
1 Analysis
→ 2 Task
→ 3 Todo and Micro-Verify
→ 4 Checklist
→ 5 Verification
```

## Failure routing

- Local implementation or test failure with valid assumptions → repeat only the failed Todo.
- Wrong assumption, unknown capability, source conflict, or scope mismatch → return to Analysis.
- Unexecuted validation → `PENDING`, never `PASS`.

## 0. Evidence before Analysis

When applicable:

- image → Reference Image Manifest;
- SPA → rendered-DOM Screen Specification;
- static HTML → preserved source and bounded inspection;
- stack fact → primary-source provenance;
- large MCP result → summarize required fact and provenance, then discard unnecessary retrieval text.

## 1. Analysis

Copy and fill this structure:

```markdown
## 1. Analysis

- Git baseline and incoming changes:
- Project Map route:
- Feature current:
- Related Files:
- Shared-file impact:
- Source evidence:
- Official or primary-source provenance:
- Assumptions:
- Unknowns:
- `⟨verification required⟩` items:

### Environment Capability Decision

| Capability | Status | Evidence | Selected Path |
|---|---|---|---|
```

Do not implement during Analysis.

Capability enforcement:

1. read the Project Map capability result;
2. repeat the decision here;
3. obey the stack prohibition rule.

`unknown` blocks the dependent implementation.

## 2. Task

```markdown
## 2. Task

- Objective:
- Acceptance criteria:
- Out of scope:
- Validation commands:

### Expected Files

- [ ]

### Acknowledged Unexpected Files

- [ ] path — reason, impact, required regression
```

Expected Files are an estimate. Unexpected files require explicit acknowledgment.

## 3. Todo and Micro-Verify

```markdown
## 3. Todo and Micro-Verify

**Progress:** 0 / N

- [ ] Todo
  - Change:
  - Micro-Verify:
  - Result:
  - Failure action: repeat Todo / return to Analysis
```

### Mandatory decomposition defaults

Create the block list before code when any applies:

- two or more grids or data collections;
- three or more user actions;
- multiple dashboard, KPI, card, chart, matrix, or table blocks;
- frontend and backend contracts change together;
- more than one deployable artifact;
- stack profile declares a stricter threshold.

## 4. Checklist

```markdown
## 4. Checklist

- [ ] Architecture and naming
- [ ] Contract synchronization
- [ ] Source fidelity
- [ ] Capability decision enforced
- [ ] Artifact, rendered output, and runtime separately checked
- [ ] Required visual blocks are non-empty
- [ ] Error, loading, empty, and placeholder states
- [ ] Color and accessibility evidence
- [ ] Security and trust boundaries
- [ ] Shared-file reverse impact
- [ ] No unrelated changes
- [ ] State documents ready to synchronize
```

## 5. Verification

```markdown
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
```

## Completion

Production feature work requires:

- required validation passes;
- feature current updated with `code-verified`;
- append-only feature history entry with commit and PR when available;
- Project Map and Shared File Reverse Index updated;
- worklog closed or archived;
- final Git Diff reviewed.

An isolated demo is exempt from production current/history updates until promoted. It still requires its own README and stated validation.
