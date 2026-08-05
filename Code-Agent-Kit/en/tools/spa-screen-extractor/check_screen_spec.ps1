# SPDX-License-Identifier: MPL-2.0
<#
  check_screen_spec.ps1 — deliberately not a twin.

  Screen capture needs Playwright, which drives a real browser. There is no
  PowerShell equivalent, and a stub that guessed at the DOM would report screens
  that were never rendered.

  So this exits 1 (tool error), not 0. A stub that exited 0 would record an
  unchecked tree as checked, and that is the single failure the twinning work
  exists to prevent. Exiting 1 says "no verdict was reached", which is true.

  Excluded from tools/check-script-parity by name; the same reason is recorded in
  that tool's EXCLUDED table, so --status reports this as `n/a` with a reason
  rather than as unfinished work.
#>

[Console]::Error.WriteLine("[spa-screen-extractor:python-required] check_screen_spec.ps1 is a stub: this check cannot be implemented in PowerShell.")
[Console]::Error.WriteLine("Run the Python original instead:")
[Console]::Error.WriteLine("  python tools/spa-screen-extractor/check_screen_spec.py --help")
exit 1
