# check-last

Runs the checks that apply to what changed. **Takes no arguments**, which is the entire point.

```bash
python tools/check-last/check_last.py
```

## Why no arguments

Across twelve observed sessions the checks were run essentially zero times — not because anyone objected to them, but because running one meant first deciding *which files to pass*, and that decision was itself a step, and that step got skipped.

Every argument a check requires is a place it stops being run. See [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §7.

## Scope

| Invocation | Scope |
|---|---|
| `check_last.py` | files modified since the last run |
| `check_last.py --feature <name>` | the files that feature's `current.md` names in backticks |
| `check_last.py --all` | the whole tree |
| `check_last.py --mark` | reset the baseline and do nothing else |

The baseline is a file mtime at `.evidence-first/last-check`, **not a git commit**. Real sessions commit rarely, so a commit-based baseline drifts to "everything" and the tool becomes slow enough to avoid. Add `.evidence-first/` to `.gitignore`.

The marker is updated **before** the output is printed, so an interrupted run still leaves a correct baseline.

## What it routes to

| Changed | Check |
|---|---|
| `.ps1`, `.sh`, git hook | `check-shell-safety` |
| anything under `docs/` | `check-state-model` — only when `docs/project-map.md` exists, so a kit mirror is not judged as project state |
| anything under `stacks/<name>/` | `check-stack-readiness` for that stack |

A stack that **declares** `blocked` is skipped: it is supposed to validate as blocked, because its owner inputs are deliberately unresolved. Flagging it would put a false alarm in front of the operator on a correct tree, and one false alarm is enough for them to stop running this.

Exit codes:

- `0`: every applicable check passed, or nothing applicable changed
- `2`: at least one check failed
- `1`: tool error

```bash
python tools/check-last/self_test.py
```
