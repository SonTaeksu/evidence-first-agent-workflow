# SPDX-License-Identifier: MPL-2.0
<#
  check_script_parity.ps1 — deliberately not a twin.

  This is the twin harness itself, and it runs the .py side of every pair to
  compare against. On a machine without Python there is nothing to compare, so a
  PowerShell twin of it cannot do its job by construction. It is also a meta-tool:
  it blocks no commit and sits on no gate path, so the premise that a
  Python-less machine depends on it does not hold.

  So this exits 1 (tool error), not 0. A stub that exited 0 would record an
  unchecked tree as checked, and that is the single failure the twinning work
  exists to prevent. Exiting 1 says "no verdict was reached", which is true.

  Excluded from tools/check-script-parity by name; the same reason is recorded in
  that tool's EXCLUDED table, so --status reports this as `n/a` with a reason
  rather than as unfinished work.
#>

[Console]::Error.WriteLine("[check-script-parity:python-required] check_script_parity.ps1 is a stub: this check cannot be implemented in PowerShell.")
[Console]::Error.WriteLine("Run the Python original instead:")
[Console]::Error.WriteLine("  python tools/check-script-parity/check_script_parity.py --root .")
exit 1
