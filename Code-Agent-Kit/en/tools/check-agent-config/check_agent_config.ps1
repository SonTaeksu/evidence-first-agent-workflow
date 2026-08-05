# SPDX-License-Identifier: MPL-2.0
<#
  check_agent_config.ps1 — deliberately not a twin.

  This reads .codex/config.toml, and neither Windows PowerShell 5.1 nor
  PowerShell 7 has a TOML parser. A hand-rolled one would have to cope with
  multi-line strings, inline tables, arrays of tables and date types; getting any
  of those wrong produces a false alarm, and one false alarm is enough for an
  operator to pass --no-verify permanently.

  A partial twin was considered and rejected. .mcp.json and .roo/mcp.json are
  readable from PowerShell, so "check the JSON, skip the TOML" is tempting -- and
  it would mean a machine with Python catches a TOML defect while a machine
  without it passes the same tree. Preventing exactly that is why twins exist.
  Half a check is worse than none, because it makes people think they have one.

  So this exits 1 (tool error), not 0. A stub that exited 0 would record an
  unchecked tree as checked, and that is the single failure the twinning work
  exists to prevent. Exiting 1 says "no verdict was reached", which is true.

  Excluded from tools/check-script-parity by name; the same reason is recorded in
  that tool's EXCLUDED table, so --status reports this as `n/a` with a reason
  rather than as unfinished work.
#>

[Console]::Error.WriteLine("[check-agent-config:python-required] check_agent_config.ps1 is a stub: this check cannot be implemented in PowerShell.")
[Console]::Error.WriteLine("Run the Python original instead:")
[Console]::Error.WriteLine("  python tools/check-agent-config/check_agent_config.py --root .")
exit 1
