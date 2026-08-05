# SPDX-License-Identifier: MPL-2.0
<#
  check_build_log.ps1 — PowerShell twin of check_build_log.py.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Regex note: Python's `re` and .NET's regex engine agree on the constructs used
  by the default patterns (inline (?im), non-capturing groups, \b). A config may
  supply anything, so the parity harness carries a capturing-group case — if the
  two engines ever count matches differently, that case fails rather than the
  difference reaching a developer's machine silently.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  PASS
    2  an error pattern matched, or a required success pattern is absent
    1  tool error
#>
param(
    [Parameter(Mandatory = $true, Position = 0)][string]$Log,
    [string]$Config,
    [string]$Output
)

$ErrorActionPreference = "Stop"

$DefaultErrors = @(
    '(?im)^\s*(?:error|fatal)\b',
    '(?i)\bbuild failed\b',
    '(?i)\bgeneration failed\b',
    '(?i)\bcompilation failed\b'
)

function Get-ListOrDefault($object, [string]$name, $fallback) {
    if ($null -eq $object) { return $fallback }
    if ($object.PSObject.Properties.Name -notcontains $name) { return $fallback }
    return @($object.$name)
}

try {
    $logPath = (Resolve-Path -LiteralPath $Log).Path
    $text = [System.IO.File]::ReadAllText($logPath, [System.Text.Encoding]::UTF8)

    $configData = $null
    if ($Config) {
        $configPath = (Resolve-Path -LiteralPath $Config).Path
        $configData = Get-Content -Raw -LiteralPath $configPath -Encoding UTF8 | ConvertFrom-Json
    }

    $errorPatterns  = Get-ListOrDefault $configData "error_patterns" $DefaultErrors
    $ignorePatterns = Get-ListOrDefault $configData "ignore_patterns" @()
    $requiredSuccess = Get-ListOrDefault $configData "required_success_patterns" @()

    $filtered = $text
    foreach ($pattern in $ignorePatterns) {
        $filtered = [regex]::Replace($filtered, [string]$pattern, "")
    }

    $errors = @()
    foreach ($pattern in $errorPatterns) {
        $count = ([regex]::Matches($filtered, [string]$pattern)).Count
        if ($count -gt 0) {
            $errors += [ordered]@{ pattern = [string]$pattern; matches = $count }
        }
    }

    $missingSuccess = @()
    foreach ($pattern in $requiredSuccess) {
        if (-not [regex]::IsMatch($filtered, [string]$pattern)) {
            $missingSuccess += [string]$pattern
        }
    }

    if ($errors.Count -eq 0 -and $missingSuccess.Count -eq 0) {
        $status = "PASS"
    } else {
        $status = "FAIL"
    }

    if ($Output) {
        $report = [ordered]@{
            schema = "evidence-first/build-log-check/v1"
            status = $status
            log    = ($logPath -replace '\\', '/')
            errors = $errors
            missing_success_patterns = $missingSuccess
        }
        $directory = Split-Path -Parent $Output
        if ($directory -and -not (Test-Path -LiteralPath $directory)) {
            # [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
            # -LiteralPath parameter at all -- only -Path, which globs [ ] * ? -- so
            # there is no safe New-Item form. The .NET call is literal by definition
            # and creates intermediate directories.
            [void][System.IO.Directory]::CreateDirectory($directory)
        }
        ($report | ConvertTo-Json -Depth 6) + "`n" | Set-Content -LiteralPath $Output -Encoding UTF8
    }

    Write-Output "Build log check: $status"
    foreach ($item in $errors) {
        [Console]::Error.WriteLine("[check-build-log:error-pattern-matched] " +
            $item.pattern + " (" + $item.matches + " matches)")
    }
    foreach ($pattern in $missingSuccess) {
        [Console]::Error.WriteLine("[check-build-log:missing-success-pattern] $pattern")
    }

    if ($status -eq "PASS") { exit 0 }
    exit 2
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
