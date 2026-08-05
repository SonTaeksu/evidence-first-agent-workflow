# check-script-parity

Proves that each `.py` check and its `.ps1` twin reach the **same verdict**, so a machine without Python is judged the same way as everyone else.

```bash
python tools/check-script-parity/check_script_parity.py --root .
python tools/check-script-parity/check_script_parity.py --root . --status
python tools/check-script-parity/check_script_parity.py --root . --tool check-shell-safety
```

## What it compares

Not the exit code alone — two implementations can both exit `2` for entirely different reasons and look identical. Each case compares a pair:

```text
(exit code, set of finding identifiers printed)
```

Identifiers are `<tool>:<finding-id>`, emitted by the tool itself. See [`../../docs/core/finding-identifiers.md`](../../docs/core/finding-identifiers.md).

## And agreement is not enough either

Two twins can be wrong in the same way and still agree. So every case pins the exit code the convention requires:

| Verdict | Exit |
|---|---|
| pass | `0` |
| validation failure | `2` |
| tool error | `1` |

A case where the twins agree but both disagree with `expect` is reported as `CONV` — a convention violation, counted separately from a parity mismatch, and still exit `2`. That makes the exit-code convention a machine verdict rather than a documented intention.

## Requirements

PowerShell must be on `PATH` — `pwsh` is preferred, `powershell` accepted. **Without it this tool exits `1`, not `0`.** An unverified twin recorded as verified is worse than one recorded as unverified.

`pwsh` 7 is enough. Windows PowerShell 5.1 cannot be installed on Linux, so the twins are written to its subset — no `&&`, no `??`, no ternary, no `-Parallel` — and 5.1-specific behaviour is confirmed on Windows.

## Fixtures

Owned by this harness, not borrowed from each tool's `self_test`. A harness that reads a tool's internals breaks whenever that tool is refactored, and then it stops being run.

Where a fixture must satisfy a tool's own requirement list, the harness **imports that list** from the tool rather than copying it, so the two cannot drift apart.

Cases that read git rather than the filesystem set `"git": True`, and the harness builds a real repository with one commit on `main`. Line endings and path separators in git's output are a real source of divergence between the two implementations, and only a real repository exercises it.

## Reading the status report

```text
  OK  check-shell-safety      twinned            11 case(s)
  --  check-git-scope         not started        -
  --  check-last              identifiers only   -

  twinned 6 / 19 tools, 47 case(s) total
  remaining: check-agent-config, check-git-scope, ...
```

`--status` walks the tree, so it answers "how far did this get" by measuring rather than by remembering. Prefer it over any hand-written progress list.

Exit codes:

- `0`: every case agrees and every pinned expectation holds
- `2`: a parity mismatch or a convention violation
- `1`: tool error, including no PowerShell available
