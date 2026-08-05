# UI validation

Windows Forms produces no rendered document, so the rendered-output layer reads the designer control tree instead. The full rationale is in [`../references/ui-evidence-contract.md`](../references/ui-evidence-contract.md).

## Required

```bash
python stacks/csharp-winforms/tools/extract_designer_tree.py \
  --designer {FORM}.Designer.cs \
  --output {EVIDENCE}/tree.json

python stacks/csharp-winforms/tools/check_designer_spec.py \
  --tree {EVIDENCE}/tree.json \
  --spec {EVIDENCE}/spec.json
```

The specification is written during Gate §1 Analysis from the source asset, before the form exists. A specification written afterwards describes whatever was built and proves nothing.

## Evidence

- the specification file, committed with the worklog;
- the extracted tree, committed with the worklog;
- the comparison command and its exit code;
- every warning, with a stated reason for each container reported as empty.

## Ordering

```text
source asset
→ screen specification (§1 Analysis)
→ implementation
→ designer-tree extraction
→ comparison (§5 Verification)
```

## Runtime, accessibility, and colour

These layers need a running window. Without a confirmed `ui-automation` capability there is no deterministic way to observe them, and the record is `PENDING` with the reason — not `PASS`.

When an automation harness is confirmed, add its commands here and state which layer each one covers. Do not let one harness invocation stand in for all three layers.

## Manual inspection

A screenshot taken by a person is a useful aid and is not evidence. It is not reproducible by exit code and is not recorded as a passing gate.
