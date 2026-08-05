# SPDX-License-Identifier: MPL-2.0
<#
  check_mirror_parity.ps1 — PowerShell twin of check_mirror_parity.py.

  Compares language mirrors against each other and against their own claims.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  mirrors agree and every checkable claim matches
    2  orphan path, differing shared source, or a claim contradicted by measurement
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
    [string[]]$Mirror = @(),
    [string[]]$IdenticalSuffix = @()
)

$ErrorActionPreference = "Stop"

$DefaultMirrors = @("en", "ko")

# Not prose. Translated mirrors share these verbatim.
$IdenticalSuffixes = @(".py", ".sh", ".ps1", ".js", ".cs")

$Manifest = "KIT-MANIFEST.json"
$CountKey = "mirrored_file_count"
$RuleKey = "mirrored_file_count_rule"

# Build residue. Never part of a mirror, and produced by running any Python tool
# in place, so it is excluded from measurement and reported as a warning rather
# than a failure.
$ResidueDirs = @("__pycache__", ".evidence-first")
$ResidueSuffixes = @(".pyc", ".pyo")

# Locally generated evidence. .gitignore already declares these paths as
# generated, and the kit's own scripts write them. Without the exclusion, running
# the validation the kit tells you to run makes this gate report orphan paths.
$ResiduePathFragments = @("docs/evidence/generated/")

# Counting rules this tool knows how to measure. A manifest naming a rule that is
# absent here is reported as unverifiable rather than wrong.
$KnownRules = @("all-files")

# ---------------------------------------------------------------------------
function Test-Residue {
    param([string]$Relative)
    foreach ($part in ($Relative -split "/")) {
        if ($ResidueDirs -contains $part) { return $true }
    }
    foreach ($fragment in $ResiduePathFragments) {
        if ($Relative.Contains($fragment)) { return $true }
    }
    return ($ResidueSuffixes -contains [System.IO.Path]::GetExtension($Relative).ToLower())
}

function Get-RelativeFiles {
    # Returns every file path relative to $RootPath, posix-separated, split into
    # real content and build residue in one walk.
    param([string]$RootPath)
    $prefix = $RootPath.TrimEnd([char]47, [char]92)
    $content = @()
    $residue = @()
    $items = Get-ChildItem -LiteralPath $RootPath -Recurse -File -Force -ErrorAction SilentlyContinue
    foreach ($item in $items) {
        $relative = $item.FullName.Substring($prefix.Length).TrimStart([char]47, [char]92)
        $relative = $relative -replace '\\', '/'
        if (Test-Residue $relative) { $residue += $relative } else { $content += $relative }
    }
    return @{ content = @($content); residue = @($residue | Sort-Object) }
}

function Get-Digest {
    param([string]$Path)
    $stream = [System.IO.File]::OpenRead($Path)
    try {
        $sha = [System.Security.Cryptography.SHA256]::Create()
        try {
            $bytes = $sha.ComputeHash($stream)
        } finally {
            $sha.Dispose()
        }
    } finally {
        $stream.Dispose()
    }
    return ([System.BitConverter]::ToString($bytes) -replace '-', '').ToLower()
}

# ---------------------------------------------------------------------------
try {
    $rootPath = [System.IO.Path]::GetFullPath(
        [System.IO.Path]::Combine((Get-Location).Path, $Root))
    $names = $Mirror
    if ($names.Count -eq 0) { $names = $DefaultMirrors }

    $roots = @{}
    foreach ($name in $names) { $roots[$name] = Join-Path $rootPath $name }

    $missingMirrors = @()
    foreach ($name in $names) {
        if (-not (Test-Path -LiteralPath $roots[$name] -PathType Container)) { $missingMirrors += $name }
    }
    if ($missingMirrors.Count -gt 0) {
        throw ("[check-mirror-parity:mirror-missing] mirror directory not found: " +
               ($missingMirrors -join ", "))
    }
    if ($names.Count -lt 2) {
        throw "[check-mirror-parity:too-few-mirrors] at least two mirrors are required"
    }

    $suffixes = @($IdenticalSuffixes)
    foreach ($suffix in $IdenticalSuffix) {
        if ($suffix.StartsWith(".")) { $suffixes += $suffix } else { $suffixes += ("." + $suffix) }
    }

    Write-Output ("Mirror parity: " + ($names -join ", ") + " under " + $rootPath)

    $walked = @{}
    foreach ($name in $names) { $walked[$name] = Get-RelativeFiles $roots[$name] }

    # -- 1. path parity ------------------------------------------------------
    $union = New-Object System.Collections.Generic.HashSet[string]
    $sets = @{}
    foreach ($name in $names) {
        $set = New-Object System.Collections.Generic.HashSet[string]
        foreach ($relative in $walked[$name].content) {
            [void]$set.Add($relative)
            [void]$union.Add($relative)
        }
        $sets[$name] = $set
    }

    $pathFailures = @()
    foreach ($relative in (@($union) | Sort-Object)) {
        $absent = @()
        $present = @()
        foreach ($name in $names) {
            if ($sets[$name].Contains($relative)) { $present += $name } else { $absent += $name }
        }
        if ($absent.Count -gt 0 -and $absent.Count -lt $names.Count) {
            $pathFailures += ("[check-mirror-parity:orphan-path] " + $relative +
                              " (in " + ($present -join "/") +
                              "; missing from " + ($absent -join "/") + ")")
        }
    }
    Write-Output ("  paths: " + $sets[$names[0]].Count + " in " + $names[0])

    # -- 2. shared source identity -------------------------------------------
    $base = $names[0]
    $shared = @()
    foreach ($relative in $walked[$base].content) {
        if ($suffixes -contains [System.IO.Path]::GetExtension($relative).ToLower()) { $shared += $relative }
    }
    $shared = @($shared | Sort-Object)

    $sourceFailures = @()
    $compared = 0
    foreach ($relative in $shared) {
        $expected = Get-Digest (Join-Path $roots[$base] $relative)
        foreach ($name in $names) {
            if ($name -eq $base) { continue }
            $other = Join-Path $roots[$name] $relative
            if (-not (Test-Path -LiteralPath $other -PathType Leaf)) { continue }
            $compared++
            if ((Get-Digest $other) -ne $expected) {
                $sourceFailures += ("[check-mirror-parity:shared-source-differs] between " +
                                    $base + " and " + $name + ": " + $relative)
            }
        }
    }
    Write-Output ("  shared source compared: " + $compared)

    # -- 3. counted claims ---------------------------------------------------
    $claimFailures = @()
    $warnings = @()
    foreach ($name in $names) {
        $manifestPath = Join-Path $roots[$name] $Manifest
        if (-not (Test-Path -LiteralPath $manifestPath -PathType Leaf)) { continue }
        # NOT $manifest. PowerShell variable names are case-insensitive, so a
        # local `$manifest` *is* the script-level `$Manifest` holding the filename
        # "KIT-MANIFEST.json". Overwriting it with a parsed object made the next
        # mirror's path lookup fail, so only the first mirror was ever checked --
        # and comparing identifier *sets* hid it, because the set was the same
        # while the count was wrong.
        $manifestData = [System.IO.File]::ReadAllText($manifestPath) | ConvertFrom-Json
        $claimProperty = $manifestData.PSObject.Properties[$CountKey]
        if ($null -eq $claimProperty) { continue }
        $claimed = $claimProperty.Value

        $rule = ""
        $ruleProperty = $manifestData.PSObject.Properties[$RuleKey]
        if ($null -ne $ruleProperty -and $null -ne $ruleProperty.Value) {
            $rule = ([string]$ruleProperty.Value).Trim()
        }
        $measuredPaths = $walked[$name].content

        if (-not $rule) {
            $warnings += ("[check-mirror-parity:count-rule-absent] " + $name + "/" + $Manifest +
                          ": " + $CountKey + "=" + $claimed + " has no " + $RuleKey +
                          "; cannot verify (all files measured: " + $measuredPaths.Count + ")")
            continue
        }
        if ($KnownRules -notcontains $rule) {
            $warnings += ("[check-mirror-parity:count-rule-unknown] " + $name + "/" + $Manifest +
                          ": unknown " + $RuleKey + " '" + $rule + "'; cannot verify")
            continue
        }

        # all-files: the measurement is the count of non-residue files.
        $measured = $measuredPaths.Count
        if ($measured -ne $claimed) {
            $claimFailures += ("[check-mirror-parity:count-contradicted] " + $name + "/" + $Manifest +
                               ": " + $CountKey + " claims " + $claimed +
                               ", rule '" + $rule + "' measures " + $measured)
        }
    }

    foreach ($name in $names) {
        $residue = $walked[$name].residue
        if ($residue.Count -gt 0) {
            $warnings += ("[check-mirror-parity:build-residue] " + $name + ": " +
                          $residue.Count + " build residue file(s) present, e.g. " + $residue[0])
        }
    }

    $failures = @($pathFailures) + @($sourceFailures) + @($claimFailures)
    foreach ($warning in $warnings) { Write-Output ("  WARN  " + $warning) }
    if ($failures.Count -gt 0) {
        Write-Output ("  result: BLOCKED (" + $failures.Count + " finding(s))")
        foreach ($failure in $failures) { [Console]::Error.WriteLine("  FAIL  " + $failure) }
        exit 2
    }
    Write-Output ("  result: CLEAN (" + $warnings.Count + " warning(s))")
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
