# SPDX-License-Identifier: MPL-2.0
<#
  check_kit_selfcheck.ps1 — PowerShell twin of check_kit_selfcheck.py.

  Runs the kit's own seed material through the kit's own validation.

  This twin exists because a PowerShell-only machine is exactly where the seed
  assertion matters most. Before the coupling was changed, deleting a required
  document from a seed reported CLEAN and exit 0; leaving that as the permanent
  state of a Python-less machine was not acceptable.

  Both implementations invoke the readiness validator as a subprocess and
  classify its findings by identifier, so the two have the same shape rather
  than one mirroring a Python function it cannot call. See the .py twin for why
  the module import was removed.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  the kit passes its own checks
    2  a seed or a shipped stack is blocked by the kit's own validation
    1  tool error
#>
# [CmdletBinding()] is not decoration. Without it a PowerShell script is a
# *simple* script: an argument it does not recognise is quietly collected into
# $args and ignored. A mistyped `-AllowProvisonal` would run the check with the
# switch off and report success. The .py twin exits 1 on an unknown flag, so the
# two also disagreed on every typo -- and no case noticed until one was added.
[CmdletBinding()]
param(
    [string]$Root = ".",
    [string[]]$Seed = @()
)

$ErrorActionPreference = "Stop"

$DefaultSeeds = @("templates/stack-profile", "stacks/_template")

# Identifiers, not sentences, so that rewording the validator cannot switch this
# check off the way it did once already.
$StructuralIdentifiers = @(
    "check-stack-readiness:missing-document",
    "check-stack-readiness:bad-schema",
    "check-stack-readiness:declared-state-mismatch"
)

$Validator = "tools/check-stack-readiness/check_stack_readiness.ps1"

$StackTable = "stacks/README.md"
$TableDirectoryRx = [regex]'`(stacks/[A-Za-z0-9._-]+)`'


$IdentifierRx = [regex]"\[([a-z0-9][a-z0-9/_-]*:[a-z0-9-]+)\]"
$StateLineRx = [regex]"(?mi)^Stack readiness:\s*(\w+)\s*$"

# The PowerShell running this script, used to launch the validator. `pwsh` may
# not be on PATH, and on Windows PowerShell the executable is powershell.exe.
$Shell = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName

# ---------------------------------------------------------------------------
function Read-AllText {
    # Python's read_text() normalises CRLF to LF; ReadAllText does not, and the
    # line splitting below depends on it.
    param([string]$Path)
    return ([System.IO.File]::ReadAllText($Path) -replace "`r`n", "`n")
}

function Invoke-Validator {
    param([string]$RootPath, [string]$StackPath)
    $script = Join-Path $RootPath $Validator
    if (-not (Test-Path -LiteralPath $script -PathType Leaf)) {
        throw "[check-kit-selfcheck:validator-missing] readiness validator not found: $Validator"
    }
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $output = (& $Shell @("-NoProfile", "-NonInteractive", "-File", $script,
                          "-Stack", $StackPath) 2>&1 | Out-String)
    $code = $LASTEXITCODE
    $ErrorActionPreference = $previous

    # The validator failing to run is not the same event as the validator
    # reaching a verdict, and must not be reported as a clean seed.
    if ($code -eq 1) {
        throw ("[check-kit-selfcheck:validator-failed] readiness validator could not run on " +
               $StackPath + ": " + $output.Trim())
    }

    $state = ""
    $stateMatch = $StateLineRx.Match($output)
    if ($stateMatch.Success) { $state = $stateMatch.Groups[1].Value.ToLower() }

    $identifiers = @()
    foreach ($hit in $IdentifierRx.Matches($output)) {
        $value = $hit.Groups[1].Value
        if ($identifiers -notcontains $value) { $identifiers += $value }
    }
    return @{ state = $state; identifiers = @($identifiers | Sort-Object) }
}

function Test-Seed {
    param([string]$RootPath, [string]$Relative)
    $source = Join-Path $RootPath $Relative
    if (-not (Test-Path -LiteralPath $source -PathType Container)) {
        return @{ ok = $true; notes = @("skipped (absent): " + $Relative) }
    }
    if (-not (Test-Path -LiteralPath (Join-Path $source "STACK-READINESS.json") -PathType Leaf)) {
        return @{ ok = $true; notes = @("skipped (not a stack seed): " + $Relative) }
    }

    $temporary = Join-Path ([System.IO.Path]::GetTempPath()) ([System.Guid]::NewGuid().ToString())
    # [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
    # -LiteralPath parameter at all (only -Path, which expands wildcards), so a
    # path containing [ ] * ? cannot be created safely through it. The .NET call
    # is literal by definition and creates intermediate directories.
    [void][System.IO.Directory]::CreateDirectory($temporary)
    try {
        $copy = Join-Path $temporary "seed-stack"
        Copy-Item -LiteralPath $source -Destination $copy -Recurse -Force
        $result = Invoke-Validator $RootPath $copy
    } finally {
        Remove-Item -LiteralPath $temporary -Recurse -Force -ErrorAction SilentlyContinue
    }

    $structural = @()
    foreach ($identifier in $result.identifiers) {
        if ($StructuralIdentifiers -contains $identifier) { $structural += $identifier }
    }
    if ($structural.Count -gt 0) {
        $notes = @()
        foreach ($identifier in $structural) {
            $notes += ("[check-kit-selfcheck:seed-structurally-invalid] " + $Relative +
                       ": [" + $identifier + "]")
        }
        return @{ ok = $false; notes = $notes }
    }
    return @{ ok = $true; notes = @($Relative + ": no structural failure") }
}

function Test-ShippedStacks {
    param([string]$RootPath)
    $stacks = Join-Path $RootPath "stacks"
    if (-not (Test-Path -LiteralPath $stacks -PathType Container)) {
        return @{ ok = $true; notes = @("skipped (absent): stacks/") }
    }

    $notes = @()
    $ok = $true
    $manifests = @(Get-ChildItem -LiteralPath $stacks -Directory -ErrorAction SilentlyContinue |
                   ForEach-Object { Join-Path $_.FullName "STACK-READINESS.json" } |
                   Where-Object { Test-Path -LiteralPath $_ -PathType Leaf } |
                   Sort-Object)
    foreach ($manifestPath in $manifests) {
        $stack = [System.IO.Path]::GetDirectoryName($manifestPath)
        $relative = ("stacks/" + [System.IO.Path]::GetFileName($stack))
        try {
            $manifest = [System.IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
        } catch {
            throw "invalid JSON in ${manifestPath}: $($_.Exception.Message)"
        }
        $declared = ""
        if ($null -ne $manifest.declared_state) { $declared = ([string]$manifest.declared_state).Trim() }
        if ($declared -ne "ready") { continue }

        $result = Invoke-Validator $RootPath $stack
        if ($result.identifiers.Count -gt 0 -or $result.state -ne "ready") {
            $ok = $false
            foreach ($identifier in $result.identifiers) {
                $notes += ("[check-kit-selfcheck:declared-ready-not-ready] " + $relative +
                           ": [" + $identifier + "]")
            }
            if ($result.identifiers.Count -eq 0) {
                $notes += ("[check-kit-selfcheck:declared-ready-not-ready] " + $relative +
                           ": derived state is " + $result.state + ", not ready")
            }
        } else {
            $notes += ($relative + ": ready")
        }
    }
    if ($notes.Count -eq 0) { $notes += "no stack declares ready" }
    return @{ ok = $ok; notes = $notes }
}


function Test-StackTable {
    # The hand-written table in stacks/README.md against the manifests.
    #
    # Only the *derived* columns are compared: which stack directories exist, and
    # the declared_state each manifest holds. The label and the "owner inputs"
    # column are prose written by a person and are left alone.
    #
    # The directory is matched from a backticked `stacks/<name>` cell rather than
    # from the prose label, so renaming a label cannot break the check and cannot
    # silently disable it either.
    param([string]$RootPath)
    $table = Join-Path $RootPath $StackTable
    if (-not (Test-Path -LiteralPath $table -PathType Leaf)) {
        return @{ ok = $true; notes = @("skipped (absent): " + $StackTable) }
    }

    $rows = @{}
    foreach ($line in ((Read-AllText $table) -split "`n")) {
        $trimmed = $line.Trim()
        if (-not $trimmed.StartsWith("|")) { continue }
        $cells = @($trimmed.Trim([char]124) -split "\|")
        $directory = $null
        foreach ($cell in $cells) {
            $hit = $TableDirectoryRx.Match($cell)
            if ($hit.Success) { $directory = $hit.Groups[1].Value; break }
        }
        if ($null -eq $directory) { continue }
        # Whichever cell mentions a state word; naming it by position would break
        # the moment a column is added.
        $rows[$directory] = ($cells -join " ")
    }

    $manifests = @{}
    $stacksRoot = Join-Path $RootPath "stacks"
    if (Test-Path -LiteralPath $stacksRoot -PathType Container) {
        $directories = @(Get-ChildItem -LiteralPath $stacksRoot -Directory -ErrorAction SilentlyContinue |
                         Sort-Object -Property Name)
        foreach ($directory in $directories) {
            if ($directory.Name.StartsWith("_")) { continue }
            $manifestPath = Join-Path $directory.FullName "STACK-READINESS.json"
            if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { continue }
            $parsed = (Read-AllText $manifestPath) | ConvertFrom-Json
            $declared = ""
            if ($null -ne $parsed.declared_state) { $declared = ([string]$parsed.declared_state).Trim() }
            $manifests["stacks/" + $directory.Name] = $declared
        }
    }

    $notes = @()
    $ok = $true
    foreach ($relative in ($manifests.Keys | Sort-Object)) {
        $declared = $manifests[$relative]
        if (-not $rows.ContainsKey($relative)) {
            $ok = $false
            $notes += ("[check-kit-selfcheck:stack-table-row-missing] " + $StackTable +
                       " has no row for " + $relative + " (declares '" + $declared + "')")
            continue
        }
        if ($declared -and -not $rows[$relative].Contains($declared)) {
            $ok = $false
            $notes += ("[check-kit-selfcheck:stack-table-state-stale] " + $StackTable +
                       " row for " + $relative + " does not mention its declared state '" +
                       $declared + "'")
        } else {
            $notes += ($relative + ": table agrees with the manifest")
        }
    }
    foreach ($relative in ($rows.Keys | Sort-Object)) {
        if (-not $manifests.ContainsKey($relative)) {
            $ok = $false
            $notes += ("[check-kit-selfcheck:stack-table-row-orphan] " + $StackTable +
                       " has a row for " + $relative + ", which has no readiness manifest")
        }
    }
    if ($notes.Count -eq 0) { $notes += ($StackTable + ": no stack rows to compare") }
    return @{ ok = $ok; notes = @($notes) }
}

# ---------------------------------------------------------------------------
try {
    $rootPath = [System.IO.Path]::GetFullPath(
        [System.IO.Path]::Combine((Get-Location).Path, $Root))
    $seeds = $Seed
    if ($seeds.Count -eq 0) { $seeds = $DefaultSeeds }

    $failures = @()
    Write-Output ("Kit self-check: " + $rootPath)

    foreach ($relative in $seeds) {
        $result = Test-Seed $rootPath $relative
        foreach ($note in $result.notes) {
            if ($result.ok) { Write-Output ("  OK    " + $note) }
            else { Write-Output ("  FAIL  " + $note) }
        }
        if (-not $result.ok) { $failures += $result.notes }
    }

    $result = Test-ShippedStacks $rootPath
    foreach ($note in $result.notes) {
        if ($result.ok) { Write-Output ("  OK    " + $note) }
        else { Write-Output ("  FAIL  " + $note) }
    }
    if (-not $result.ok) { $failures += $result.notes }

    $result = Test-StackTable $rootPath
    foreach ($note in $result.notes) {
        if ($result.ok) { Write-Output ("  OK    " + $note) }
        else { Write-Output ("  FAIL  " + $note) }
    }
    if (-not $result.ok) { $failures += $result.notes }

    if ($failures.Count -gt 0) {
        Write-Output ("  result: BLOCKED (" + $failures.Count + " finding(s))")
        foreach ($failure in $failures) { [Console]::Error.WriteLine("  FAIL  " + $failure) }
        exit 2
    }
    Write-Output "  result: CLEAN"
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
