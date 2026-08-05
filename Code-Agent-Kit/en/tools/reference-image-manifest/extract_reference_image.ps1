# SPDX-License-Identifier: MPL-2.0
<#
  extract_reference_image.ps1 — deliberately not a twin.

  Pixel measurement needs PIL. Reimplementing colour quantisation and
  perceptual distance in PowerShell would produce numbers that disagree with
  the Python original, and a reference-image gate that disagrees with itself is
  worse than one that is absent: it teaches the operator to stop trusting it.

  So this exits 1 (tool error), not 0. A stub that exited 0 would record an
  unchecked tree as checked, and that is the single failure the twinning work
  exists to prevent. Exiting 1 says "no verdict was reached", which is true.

  Excluded from tools/check-script-parity by name; the same reason is recorded in
  that tool's EXCLUDED table, so --status reports this as `n/a` with a reason
  rather than as unfinished work.
#>

[Console]::Error.WriteLine("[reference-image-manifest:python-required] extract_reference_image.ps1 is a stub: this check cannot be implemented in PowerShell.")
[Console]::Error.WriteLine("Run the Python original instead:")
[Console]::Error.WriteLine("  python tools/reference-image-manifest/extract_reference_image.py --help")
exit 1
