# SPDX-License-Identifier: MPL-2.0
<#
  check_shell_safety.ps1 — PowerShell twin of check_shell_safety.py.

  A machine without Python has this as its only gate, so the two must agree on
  both the exit code and the finding identifiers. Verified by
  tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  clean
    2  one or more findings
    1  tool error
#>
# [CmdletBinding()] is not decoration. Without it a PowerShell script is a
# *simple* script: an argument it does not recognise is quietly collected into
# $args and ignored. A mistyped `-AllowProvisonal` would run the check with the
# switch off and report success. The .py twin exits 1 on an unknown flag, so the
# two also disagreed on every typo -- and no case noticed until one was added.
[CmdletBinding()]
param(
    [string]$Root = "."
)

$ErrorActionPreference = "Stop"

$SkipDirs = @(".git", "node_modules", "bin", "obj", "dist", "coverage",
              "__pycache__", ".venv", "target", "_archive")

# Cmdlets that glob on the positional path parameter and offer -LiteralPath as
# the fix. Every entry is asserted to really have that parameter by self_test.py,
# against the PowerShell actually installed.
$PsLiteralPathCmdlets = @("Test-Path", "Resolve-Path", "Get-Content", "Set-Content",
                          "Add-Content", "Remove-Item", "Get-Item", "Get-ChildItem",
                          "Copy-Item", "Move-Item", "Out-File", "Rename-Item")

# Cmdlets that glob but have no -LiteralPath to offer. New-Item was in the list
# above, which made the finding unsatisfiable: obeying it produced "A parameter
# cannot be found that matches parameter name 'LiteralPath'". That broke four
# twins at once and had already shipped broken in two more, on their --output
# path. A rule that cannot be obeyed is worse than no rule.
$PsNoLiteralPath = @{
    "New-Item" = "[System.IO.Directory]::CreateDirectory / [System.IO.File]::WriteAllText"
}

$ExtensionlessShell = @("pre-commit", "pre-push", "commit-msg", "post-merge")

$PsCall = [regex]("\b(" + ($PsLiteralPathCmdlets -join "|") +
                  ")\b((?:\s+-\w+(?:\s+[^\s|;)]+)?)*)\s+(\$\w+)")
$PsCallNoLiteral = [regex]("\b(" + (($PsNoLiteralPath.Keys | Sort-Object) -join "|") +
                  ")\b((?:\s+-\w+(?:\s+[^\s|;)]+)?)*)\s+(\$\w+)")
$ShUnquoted = [regex]'(?<![''"])\b(cd|cp|mv|rm|mkdir|source|\.)\s+(-\w+\s+)*(\$\{?\w+\}?)(?![''"\w])'

function Test-Residue([string]$relative) {
    foreach ($part in ($relative -split "/")) {
        if ($SkipDirs -contains $part) { return $true }
    }
    return $false
}

function Get-Bytes([string]$path) {
    return [System.IO.File]::ReadAllBytes($path)
}

function Test-Bom($bytes) {
    if ($bytes.Length -lt 3) { return $false }
    return ($bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF)
}

function Get-Ps1BomFinding([string]$path, [string]$relative) {
    $bytes = Get-Bytes $path
    if (Test-Bom $bytes) { return @() }
    $text = [System.Text.Encoding]::UTF8.GetString($bytes)
    $nonAscii = 0
    foreach ($ch in $text.ToCharArray()) {
        if ([int][char]$ch -gt 127) { $nonAscii++ }
    }
    if ($nonAscii -gt 0) {
        $detail = "$nonAscii non-ASCII character(s) will be misread as ANSI"
    } else {
        $detail = "no non-ASCII text yet, but the next edit that adds some will break"
    }
    return @("${relative}:1: [check-shell-safety:ps1-bom] missing UTF-8 BOM - $detail")
}

function Get-NoBomFinding([string]$path, [string]$relative) {
    if (Test-Bom (Get-Bytes $path)) {
        return @("${relative}:1: [check-shell-safety:sh-bom] has a UTF-8 BOM - the shebang is no longer first")
    }
    return @()
}

function Get-Lines([string]$path) {
    # utf-8-sig equivalent: the BOM must not become a leading character.
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    if ($text.Length -gt 0 -and [int][char]$text[0] -eq 0xFEFF) {
        $text = $text.Substring(1)
    }
    return ($text -split "`r?`n")
}

function Get-LiteralPathFindings([string]$path, [string]$relative) {
    # Returns a hashtable so the advisory New-Item finding stays separate from the
    # blocking ones without changing the exit code.
    $findings = @()
    $warnings = @()
    $lines = Get-Lines $path
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^\s*#') { continue }
        foreach ($match in $PsCall.Matches($line)) {
            $cmdlet = $match.Groups[1].Value
            $switches = $match.Groups[2].Value
            $variable = $match.Groups[3].Value
            if ($switches -and $switches.Contains("-LiteralPath")) { continue }
            $findings += ("${relative}:" + ($i + 1) +
                ": [check-shell-safety:ps-literalpath] $cmdlet $variable without " +
                "-LiteralPath - a path containing [ ] * ? resolves to nothing")
        }
        foreach ($match in $PsCallNoLiteral.Matches($line)) {
            $cmdlet = $match.Groups[1].Value
            $variable = $match.Groups[3].Value
            # A warning, not a block. The hazard is real but narrower, and there is
            # no switch to add -- the fix is a different call, which is a judgement
            # about the surrounding code rather than a mechanical edit.
            $warnings += ("${relative}:" + ($i + 1) +
                ": [check-shell-safety:new-item-path] $cmdlet $variable globs " +
                "[ ] * ? and has no -LiteralPath - use " + $PsNoLiteralPath[$cmdlet])
        }
    }
    return @{ findings = @($findings); warnings = @($warnings) }
}

function Get-QuotingFindings([string]$path, [string]$relative) {
    $findings = @()
    $lines = Get-Lines $path
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line -match '^\s*#') { continue }
        foreach ($match in $ShUnquoted.Matches($line)) {
            $command = $match.Groups[1].Value
            $variable = $match.Groups[3].Value
            $findings += ("${relative}:" + ($i + 1) +
                ": [check-shell-safety:sh-quoting] $command $variable unquoted - " +
                'a path with a space splits into two arguments; use "' + $variable + '"')
        }
    }
    return $findings
}

try {
    $rootPath = (Resolve-Path -LiteralPath $Root).Path
    $findings = @()
    $warnings = @()
    $ps1Count = 0
    $shCount = 0

    $items = Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force -ErrorAction SilentlyContinue |
             Sort-Object FullName
    foreach ($item in $items) {
        $relative = $item.FullName.Substring($rootPath.Length).TrimStart([char]92, [char]47) -replace '\\', '/'
        if (Test-Residue $relative) { continue }

        $suffix = $item.Extension.ToLower()
        if ($suffix -eq ".ps1") {
            $ps1Count++
            $findings += Get-Ps1BomFinding $item.FullName $relative
            $pathResult = Get-LiteralPathFindings $item.FullName $relative
            $findings += $pathResult.findings
            $warnings += $pathResult.warnings
        }
        elseif ($suffix -eq ".sh" -or ($ExtensionlessShell -contains $item.Name)) {
            $shCount++
            $findings += Get-NoBomFinding $item.FullName $relative
            $findings += Get-QuotingFindings $item.FullName $relative
        }
    }

    Write-Output "Shell safety: $ps1Count PowerShell, $shCount shell file(s) under $rootPath"
    foreach ($warning in $warnings) { Write-Output "  WARN  $warning" }
    if ($findings.Count -gt 0) {
        Write-Output ("  result: BLOCKED (" + $findings.Count + " finding(s))")
        foreach ($finding in $findings) {
            [Console]::Error.WriteLine("  FAIL  $finding")
        }
        exit 2
    }
    Write-Output ("  result: CLEAN (" + $warnings.Count + " warning(s))")
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
