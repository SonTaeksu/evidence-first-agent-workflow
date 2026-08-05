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

## Appendix — what a failed completion looks like

Both of these were observed. Neither was reported as a failure at the time.

**A dashboard delivered as empty boxes.** The source mockup had six KPI tiles, five owner cards, a five-by-six matrix and a blocking-items table. What shipped was a title, a few KPI labels, and empty containers with borders. Two causes: the mockup exceeded the context limit so its data structure was never read — it was not split or searched, contrary to `docs/core/source-assets-guide.md` — and the build passed, which was mistaken for the work being done. **An empty screen compiles.**

**Three grids delivered as three empty containers.** The reference image showed three grids with named columns and rows. What shipped was three bordered rectangles. The cause: the task prompt was followed but its extraction steps were skipped, so the image was never decomposed into blocks, columns and rows. **A table is a grid bound to a dataset with rows in it, not an empty container of the right size.**

What prevents both is in this document already, and both runs skipped it:

- §1 requires the source evidence to be extracted **before** Analysis is written, not read casually;
- §3 requires a Todo block list when a screen has multiple data blocks — one block per Todo, each with its own Micro-Verify;
- §4 requires `Required visual blocks are non-empty` to be checked against the source, block by block;
- §5 records rendered output as a **separate layer** from compile, precisely because compile passes on an empty screen.

If the verification table shows `Artifact PASS` and nothing else, the work is not finished — it is unverified.
