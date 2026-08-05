# UI evidence contract (C# Windows Forms)

## The problem this solves

The kit separates four validation layers, and the second one — rendered output — normally reads a rendered document. Windows Forms produces none. Without a substitute the layer silently collapses into "the build succeeded", which is exactly the failure `validation-layers.md` warns about: a passing compile with an empty screen.

## 1. Declare before you build

During Gate §1 Analysis, write the screen specification from the source asset, not from the implementation. It lists what the form must contain.

```json
{
  "form": "MainForm",
  "required_controls": [
    { "name": "panelInput", "type": "Panel", "parent": "MainForm" },
    { "name": "txtName", "type": "TextBox", "parent": "panelInput" },
    { "name": "btnGreet", "type": "Button", "parent": "MainForm" }
  ]
}
```

Writing the specification after the form exists proves nothing — it will describe whatever was built.

## 2. Extract, do not read by eye

```bash
python stacks/csharp-winforms/tools/extract_designer_tree.py \
  --designer src/MainForm.Designer.cs \
  --output docs/worklogs/evidence/mainform.tree.json
```

The extractor removes comments before matching, and preserves string literals while doing it. A control that appears only inside a comment is not in the tree; a `//` inside a literal does not truncate the line.

A control counts only when it is both declared as a field and constructed with `new`. That excludes form property assignments such as `this.ClientSize = new System.Drawing.Size(...)`, which are not controls.

## 3. Compare — this is the gate

```bash
python stacks/csharp-winforms/tools/check_designer_spec.py \
  --tree docs/worklogs/evidence/mainform.tree.json \
  --spec docs/worklogs/evidence/mainform.spec.json
```

| Finding | Verdict | Why |
|---|---|---|
| Required control absent | FAIL | the screen does not contain what was declared |
| Required control has the wrong type | FAIL | a Label where a TextBox was declared is not the screen |
| Required control has the wrong parent | FAIL | a control outside its declared container is misplaced |
| Form name differs | FAIL | the tree describes a different form |
| Container with no children | WARN | a container may legitimately be filled at runtime |

The empty-container case is a warning on purpose. Blocking it would fail correct code that populates a panel at runtime, and one false positive teaches the operator to bypass the gate.

## 4. What this does not prove

The control tree is a declaration, not a rendering. It does not establish position, colour, contrast, focus order at run time, or that the form opens at all. Record those layers separately:

| Layer | Evidence in this stack |
|---|---|
| Artifact / compile | MSBuild exit code |
| Rendered output | designer-tree comparison |
| Runtime behaviour | UI automation when the capability is confirmed; otherwise `PENDING` with a reason |
| Accessibility / colour | screenshot or automation evidence when available; otherwise `PENDING` with a reason |

Reporting runtime behaviour as `PASS` because the tree matched is a false claim. When no automation capability is confirmed, the honest record is `PENDING` and the reason.
