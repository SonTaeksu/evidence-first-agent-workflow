# SPDX-License-Identifier: MPL-2.0
<#
  check_document_sync.ps1 — PowerShell twin of check_document_sync.py.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Git output note: git emits LF-terminated, UTF-8 paths regardless of platform.
  Splitting on `\r?\n` and trimming each line keeps the two implementations
  agreeing on a Windows checkout with core.autocrlf enabled, where a naive
  split would leave a trailing CR on every path and no comparison would match.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  synchronized
    2  code changed without state, or a state/Project Map path is missing
    1  tool error, including "not inside a Git repository"
#>
param(
    [string]$Base = "main",
    [Parameter(Mandatory = $true)][string]$Scope,
    [Parameter(Mandatory = $true)][string]$Current,
    [Parameter(Mandatory = $true)][string]$History,
    [Parameter(Mandatory = $true)][string]$ProjectMap
)

$ErrorActionPreference = "Stop"

function Invoke-Git([string]$workingDirectory, [string[]]$gitArgs) {
    $previous = $PWD.Path
    try {
        Set-Location -LiteralPath $workingDirectory
        $output = & git @gitArgs 2>&1
        $code = $LASTEXITCODE
    } finally {
        Set-Location -LiteralPath $previous
    }
    return @{ code = $code; text = ($output | Out-String) }
}

function Get-GitLines([string]$workingDirectory, [string[]]$gitArgs) {
    $result = Invoke-Git $workingDirectory $gitArgs
    if ($result.code -ne 0) {
        $message = $result.text.Trim()
        if ([string]::IsNullOrEmpty($message)) { $message = "git command failed" }
        throw $message
    }
    $lines = @()
    foreach ($line in ($result.text -split "`r?`n")) {
        $trimmed = $line.Trim()
        if (-not [string]::IsNullOrEmpty($trimmed)) { $lines += $trimmed }
    }
    return $lines
}

try {
    $start = (Get-Location).Path
    $topLevel = Invoke-Git $start @("rev-parse", "--show-toplevel")
    if ($topLevel.code -ne 0) { throw "Not inside a Git repository." }
    $root = (Resolve-Path -LiteralPath $topLevel.text.Trim()).Path
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}

try {
    Get-GitLines $root @("rev-parse", "--verify", $Base) | Out-Null
    $changed = @{}
    foreach ($path in (Get-GitLines $root @("diff", "--name-only", $Base, "--"))) {
        $changed[($path -replace '\\', '/')] = $true
    }
    foreach ($path in (Get-GitLines $root @("ls-files", "--others", "--exclude-standard"))) {
        $changed[($path -replace '\\', '/')] = $true
    }
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}

$scopeName = $Scope.Trim([char]47)
$scoped = @()
foreach ($path in $changed.Keys) {
    if ($path.StartsWith($scopeName + "/")) { $scoped += $path }
}

$codeChanged = $false
foreach ($path in $scoped) {
    foreach ($part in @("frontend", "backend", "scripts")) {
        if ($path.StartsWith("$scopeName/$part/")) { $codeChanged = $true }
    }
}

$currentPosix    = $Current    -replace '\\', '/'
$historyPosix    = $History    -replace '\\', '/'
$projectMapPosix = $ProjectMap -replace '\\', '/'
$statePaths = @("$scopeName/$currentPosix", "$scopeName/$historyPosix", "$scopeName/$projectMapPosix")

$changedState = @()
foreach ($path in $statePaths) { if ($scoped -contains $path) { $changedState += $path } }

$errors = @()

if ($codeChanged -and $changedState.Count -eq 0) {
    $errors += ("[check-document-sync:state-not-updated] code changed but " +
                "current/history/project-map did not")
}

$scopeRoot = Join-Path $root $scopeName
$projectMapFile = Join-Path $scopeRoot $projectMapPosix
if (-not (Test-Path -LiteralPath $projectMapFile)) {
    $errors += "[check-document-sync:missing-project-map] $projectMapFile"
} else {
    $text = [System.IO.File]::ReadAllText($projectMapFile, [System.Text.Encoding]::UTF8)
    $candidates = @{}
    foreach ($match in ([regex]'`([^`]+)`').Matches($text)) {
        $item = $match.Groups[1].Value -replace '\\', '/'
        if ($item.Contains("/") -and -not $item.StartsWith("http://") -and -not $item.StartsWith("https://")) {
            $candidates[$item] = $true
        }
    }
    foreach ($item in ($candidates.Keys | Sort-Object)) {
        if (-not (Test-Path -LiteralPath (Join-Path $scopeRoot $item))) {
            $errors += "[check-document-sync:project-map-dangling-path] $item"
        }
    }
}

foreach ($state in @($Current, $History)) {
    if (-not (Test-Path -LiteralPath (Join-Path $scopeRoot $state))) {
        $errors += "[check-document-sync:missing-state-file] $state"
    }
}

if ($errors.Count -gt 0) {
    foreach ($item in $errors) { [Console]::Error.WriteLine("FAIL: $item") }
    exit 2
}

Write-Output "Document synchronization checks passed."
exit 0
