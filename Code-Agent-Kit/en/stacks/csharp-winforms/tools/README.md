# csharp-winforms stack tools

Deterministic evidence for the rendered-output layer of a UI framework that has no rendered document.

```bash
python tools/extract_designer_tree.py --designer {FORM}.Designer.cs --output tree.json
python tools/check_designer_spec.py --tree tree.json --spec spec.json
python tools/self_test.py
```

## extract_designer_tree.py

Parses `InitializeComponent` into a control tree: name, type, parent, text, container flag, child count.

Comments are blanked before matching, with equal-length replacement so offsets and line numbers are unchanged, and string literals are preserved. A control mentioned only in a comment does not enter the tree, and a `//` inside a literal does not truncate the line.

A name counts as a control only when it is both declared as a field and constructed with `new`. That excludes form property assignments such as `this.ClientSize = new System.Drawing.Size(...)`.

Exit codes: `0` a tree was produced, `2` no form found, `1` tool error.

## check_designer_spec.py

Compares the tree against a specification written during Gate §1 Analysis.

| Finding | Verdict |
|---|---|
| Required control absent, mistyped, or misparented | FAIL |
| Form name differs from the declaration | FAIL |
| Container with no children | WARN |

The empty-container case is a warning because a container may legitimately be filled at runtime. Blocking it would fail correct code, and one false positive teaches the operator to bypass the gate — see [`../../../docs/core/gate-design-principles.md`](../../../docs/core/gate-design-principles.md) §1.

Exit codes: `0` satisfied, `2` a required control is missing or mistyped, `1` tool error.

## self_test.py

Fourteen cases. Half assert that something is removed; half assert that something is kept, including a `//` inside a string literal, length and line preservation, and the shipped skeleton parsing to exactly its five controls. The keep cases matter more: a stripper that eats a literal breaks correct code.
