# check-shell-safety

Catches the script defects that pass review, work on the author's machine, and break on someone else's.

```bash
python tools/check-shell-safety/check_shell_safety.py --root .
python tools/check-shell-safety/self_test.py
```

| Finding | Why it breaks |
|---|---|
| `.ps1` with no UTF-8 BOM | PowerShell 5.1 reads it as the system ANSI code page. Non-ASCII literals become mojibake, and when one is used in a comparison or a regular expression the **verdict fails**, not just the display |
| `.sh` or git hook **with** a BOM | the shebang is no longer the first bytes, so the interpreter is not selected |
| PowerShell path cmdlet without `-LiteralPath` | `Test-Path`, `Resolve-Path`, `Get-Content`, `Remove-Item`, `New-Item` and friends glob `[ ] * ?` on the positional parameter. A directory named `project [old]` matches nothing and the script proceeds as if the file were absent |
| Unquoted shell variable in a path position | `cd $ROOT` splits on the first space, and a Windows checkout under `My Projects` is the normal case |

Exit codes:

- `0`: clean
- `2`: one or more findings
- `1`: tool or file error

Comment lines are skipped, `-LiteralPath` is recognised after other switches, and a quoted literal path is not mistaken for a variable. Seven of the eleven self-test cases assert that something is **accepted** — a false positive here would make every script look broken and the operator would stop running the check, which costs more than the defect it was meant to catch. See [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §2.

Rules and rationale: [`../../docs/core/command-and-process-safety.md`](../../docs/core/command-and-process-safety.md).
