# check-mirror-parity

Compares the language mirrors against each other and against their own counted claims.

```bash
python tools/check-mirror-parity/check_mirror_parity.py --root ..
python tools/check-mirror-parity/self_test.py
```

Run it from the directory that holds the mirrors, or point `--root` at it.

| Check | Verdict |
|---|---|
| Every mirror holds the same set of relative paths | FAIL on an orphan |
| Non-prose files (`.py`, `.sh`, `.ps1`, `.js`, `.cs`) are byte-identical across mirrors | FAIL on a difference |
| `mirrored_file_count` matches a measurement under the rule named by `mirrored_file_count_rule` | FAIL on a contradiction |
| A count with no recorded rule | WARN — the claim may be correct under a rule the document never wrote down |
| Build residue (`__pycache__`, `.pyc`, `.pyo`) | excluded from measurement, WARN if present |

Only the documentation is translated, so a difference in a script means the mirrors produce different verdicts on the same input. An orphan path means a link or a documented command is broken in one language.

Exit codes:

- `0`: mirrors agree and every checkable claim matches
- `2`: orphan path, differing shared source, or a claim contradicted by measurement
- `1`: tool or file error

`--mirror <name>` selects mirrors, `--identical-suffix <ext>` extends the shared-source set. Rationale in [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §2.
