# SPDX-License-Identifier: MPL-2.0
<#
  check_git_scope.ps1 — PowerShell twin of check_git_scope.py.

  Checks the final Git change set against expected and acknowledged files.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  the change set matches expected plus acknowledged scope
    2  scope mismatch
    1  tool error
#>
# [CmdletBinding()] is not decoration. Without it a PowerShell script is a
# *simple* script: an argument it does not recognise is quietly collected into
# $args and ignored. A mistyped `-AllowProvisonal` would run the check with the
# switch off and report success. The .py twin exits 1 on an unknown flag, so the
# two also disagreed on every typo -- and no case noticed until one was added.
[CmdletBinding()]
param(
    [string]$Design,
    [string]$Expected,
    [string]$ExpectedFile,
    [string]$Ack,
    [string]$AckFile,
    [string]$Base,
    [string]$Scope = "",
    [string]$Root,
    [switch]$Strict
)

$ErrorActionPreference = "Stop"

# ---------------------------------------------------------------------------
function Invoke-GitIn {
    # Returns a hashtable so callers can branch on the exit code the way the
    # Python side branches on CompletedProcess.returncode.
    param([string]$WorkingDirectory, [string[]]$Arguments)
    $previous = Get-Location
    $previousPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        Set-Location -LiteralPath $WorkingDirectory
        $out = & git @Arguments 2>$null
        $code = $LASTEXITCODE
    } catch {
        $out = @()
        $code = 1
    } finally {
        $ErrorActionPreference = $previousPreference
        Set-Location -LiteralPath $previous
    }
    if ($null -eq $out) { $out = @() }
    return @{ code = $code; text = (@($out) -join "`n") }
}

function Get-Normalized {
    # Mirrors normalize(): note that Python's lstrip("./") strips any leading run
    # of '.' and '/' characters, not the literal prefix "./".
    param([string]$Value)
    $out = ($Value -replace '\\', '/').Trim()
    $out = $out.Trim([char]34).Trim([char]39)
    return $out.TrimStart([char]46, [char]47)
}

function Get-ParsedList {
    param([string]$Inline, [string]$FilePath)
    $values = @()
    if ($Inline) { $values += ($Inline -split "[,`n]") }
    if ($FilePath) {
        $text = [System.IO.File]::ReadAllText($FilePath) -replace "`r`n", "`n"
        # Python's splitlines() drops a single trailing newline rather than
        # yielding a final empty element.
        $values += ($text -split "`n")
        if ($values.Count -gt 0 -and $text.EndsWith("`n")) {
            $values = $values[0..($values.Count - 2)]
        }
    }
    $result = @()
    foreach ($value in $values) {
        $cleaned = $value.Trim().TrimStart([char]45, [char]42, [char]91, [char]32,
                                           [char]93, [char]120, [char]88).Trim()
        $cleaned = $cleaned.Trim([char]96)
        $cleaned = Get-Normalized $cleaned
        if ($cleaned -and ($cleaned.Contains("/") -or $cleaned.Contains("."))) {
            if ($result -notcontains $cleaned) { $result += $cleaned }
        }
    }
    return @($result)
}

function Get-ExpectedFromDesign {
    param([string]$DesignPath)
    $text = [System.IO.File]::ReadAllText($DesignPath) -replace "`r`n", "`n"
    # Single-quoted, and it has to be. In a double-quoted PowerShell string the
    # `$(` of `$([\s\S]*?)` opens a subexpression, and the script fails to parse
    # at all -- the twin errors instead of running, which is a whole gate silently
    # gone on a Python-less machine.
    #
    # \z, not \Z: .NET's \Z also matches before a final newline, Python's \Z does
    # not. With \Z the section would end one character early on a file that ends
    # in a newline, which is every file.
    $match = [regex]::Match(
        $text, '^## Expected Files\s*$([\s\S]*?)(?=^## |\z)',
        [System.Text.RegularExpressions.RegexOptions]::Multiline)
    if (-not $match.Success) {
        throw "[check-git-scope:design-without-expected-files] Design does not contain a '## Expected Files' section."
    }
    $result = @()
    foreach ($hit in ([regex]'`([^`]+)`').Matches($match.Groups[1].Value)) {
        $value = $hit.Groups[1].Value
        if ($value.Contains("*")) { continue }
        if ($value.EndsWith("/")) { continue }
        $normalized = Get-Normalized $value
        if ($result -notcontains $normalized) { $result += $normalized }
    }
    return @($result)
}

function Resolve-BaseRef {
    param([string]$RepositoryPath, [string]$Requested)
    $candidates = @()
    if ($Requested) { $candidates += $Requested }
    $candidates += @("origin/main", "main", "master")
    foreach ($candidate in $candidates) {
        $result = Invoke-GitIn $RepositoryPath @("rev-parse", "--verify", "--quiet", $candidate)
        if ($result.code -eq 0) { return $candidate }
    }
    return ""
}

function Get-PorcelainPaths {
    param([string]$Value)
    $files = @()
    foreach ($line in ($Value -split "`r?`n")) {
        if (-not $line.Trim()) { continue }
        if ($line.Length -gt 3) { $path = $line.Substring(3) } else { $path = $line.Trim() }
        if ($path.Contains(" -> ")) { $path = $path.Substring($path.IndexOf(" -> ") + 4) }
        $normalized = Get-Normalized $path
        if ($files -notcontains $normalized) { $files += $normalized }
    }
    return @($files)
}

function Get-ChangedSet {
    param([string]$RepositoryPath, [string]$BaseRef)
    $status = Invoke-GitIn $RepositoryPath @("status", "--porcelain", "-uall")
    $changed = @()
    if ($status.code -eq 0) { $changed = Get-PorcelainPaths $status.text }

    if ($BaseRef) {
        $committed = Invoke-GitIn $RepositoryPath @("diff", "--name-only", ($BaseRef + "...HEAD"), "--")
        if ($committed.code -eq 0) {
            foreach ($line in ($committed.text -split "`r?`n")) {
                if (-not $line.Trim()) { continue }
                $normalized = Get-Normalized $line
                if ($changed -notcontains $normalized) { $changed += $normalized }
            }
        }
    }
    return @($changed)
}

function Find-MatchingPath {
    param([string[]]$Changed, [string]$ExpectedPath)
    foreach ($candidate in $Changed) {
        if ($candidate -eq $ExpectedPath) { return $candidate }
        if ($candidate.EndsWith("/" + $ExpectedPath)) { return $candidate }
        if ($ExpectedPath.EndsWith("/" + $candidate)) { return $candidate }
    }
    return $null
}

function Apply-Scope {
    param([string[]]$Paths, [string]$ScopeValue)
    $prefix = (Get-Normalized $ScopeValue).Trim([char]47)
    if (-not $prefix) { return @($Paths) }
    $out = @()
    foreach ($value in $Paths) {
        if ($value -eq $prefix -or $value.StartsWith($prefix + "/")) {
            $out += $value
        } else {
            $out += ($prefix + "/" + $value)
        }
    }
    return @($out)
}

# ---------------------------------------------------------------------------
try {
    $expectedPaths = @(Get-ParsedList $Expected $ExpectedFile)
    if ($Design) { $expectedPaths += @(Get-ExpectedFromDesign $Design) }
    $deduped = @()
    foreach ($value in $expectedPaths) { if ($deduped -notcontains $value) { $deduped += $value } }
    $expectedPaths = Apply-Scope $deduped $Scope

    $acknowledged = Apply-Scope (Get-ParsedList $Ack $AckFile) $Scope

    if ($expectedPaths.Count -eq 0) {
        Write-Output "SKIP: no expected files were supplied through design, --expected, or --expected-file."
        exit 0
    }

    if ($Root) {
        $rootPath = [System.IO.Path]::GetFullPath(
            [System.IO.Path]::Combine((Get-Location).Path, $Root))
    } else {
        $rootPath = (Get-Location).Path
    }

    $topLevel = Invoke-GitIn $rootPath @("rev-parse", "--show-toplevel")
    $repository = $null
    if ($topLevel.code -eq 0 -and $topLevel.text.Trim()) {
        $repository = [System.IO.Path]::GetFullPath($topLevel.text.Trim())
    }

    if ($null -eq $repository) {
        $missing = @()
        foreach ($value in $expectedPaths) {
            $underRoot = Join-Path $rootPath $value
            $underCwd = Join-Path (Get-Location).Path $value
            if (-not (Test-Path -LiteralPath $underRoot) -and -not (Test-Path -LiteralPath $underCwd)) {
                $missing += $value
            }
        }
        Write-Output "MODE: Git unavailable; checking expected artifact existence only."
        if ($missing.Count -gt 0) {
            foreach ($value in $missing) {
                Write-Output ("FAIL: [check-git-scope:expected-artifact-missing] expected artifact is missing: " + $value)
            }
            exit 2
        }
        Write-Output ("PASS: all " + $expectedPaths.Count +
                      " expected artifacts exist. Unrelated-change detection was skipped.")
        exit 0
    }

    $baseRef = Resolve-BaseRef $repository $Base
    $changed = @(Get-ChangedSet $repository $baseRef)

    $matched = @()
    foreach ($value in $expectedPaths) {
        $candidate = Find-MatchingPath $changed $value
        if ($candidate -and ($matched -notcontains $candidate)) { $matched += $candidate }
    }
    $ackMatched = @()
    foreach ($value in $acknowledged) {
        $candidate = Find-MatchingPath $changed $value
        if ($candidate -and ($ackMatched -notcontains $candidate)) { $ackMatched += $candidate }
    }

    $prefix = (Get-Normalized $Scope).Trim([char]47)
    $inScope = @()
    foreach ($value in $changed) {
        if (-not $prefix -or $value -eq $prefix -or $value.StartsWith($prefix + "/")) {
            $inScope += $value
        }
    }

    $unexpected = @()
    foreach ($value in $inScope) {
        if ($matched -notcontains $value -and $ackMatched -notcontains $value) { $unexpected += $value }
    }
    $unexpected = @($unexpected | Sort-Object)

    $missing = @()
    foreach ($value in $expectedPaths) {
        if ($null -eq (Find-MatchingPath $changed $value)) { $missing += $value }
    }
    $missing = @($missing | Sort-Object)

    if ($baseRef) { $baseLabel = $baseRef } else { $baseLabel = "working tree only" }
    Write-Output ("Base: " + $baseLabel)
    Write-Output ("Changed in scope: " + $inScope.Count)
    Write-Output ("Expected: " + $expectedPaths.Count)
    Write-Output ("Acknowledged unexpected: " + $ackMatched.Count)

    $failures = 0
    if ($unexpected.Count -gt 0) {
        $failures += $unexpected.Count
        Write-Output ""
        Write-Output "Unexpected changed files:"
        foreach ($value in $unexpected) {
            Write-Output ("  - [check-git-scope:unexpected-change] " + $value)
        }
        Write-Output "Record a reason and impact in the worklog, then pass the file through --ack or --ack-file."
    }

    if ($missing.Count -gt 0) {
        # The identifier is printed either way. Severity is not part of an
        # identifier -- it lives in enforcement-matrix.md next to it.
        if ($Strict) { $label = "FAIL" } else { $label = "WARN" }
        Write-Output ""
        Write-Output ($label + ": expected but unchanged:")
        foreach ($value in $missing) {
            Write-Output ("  - [check-git-scope:expected-unchanged] " + $value)
        }
        if ($Strict) { $failures += $missing.Count }
    }

    if ($failures -gt 0) {
        Write-Output ""
        Write-Output "FAIL: scope mismatch. Return to Analysis and update the design or restore unrelated files."
        exit 2
    }

    Write-Output ""
    Write-Output "PASS: changed files match expected plus acknowledged scope."
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
