# SPDX-License-Identifier: MPL-2.0
<#
  check_last.ps1 — PowerShell twin of check_last.py.

  Runs the checks that apply to what changed. Takes no arguments, for the reason
  given at length in the .py twin: every argument a check requires is a place it
  stops being run.

  This is a router, and the twin routes to `.ps1` where the original routes to
  `.py`. That is the whole point — on a machine without Python the sub-checks
  reachable from here are the PowerShell ones, and the two routings reach the
  same verdict only because tools/check-script-parity proves each sub-check pair
  equal. The router inherits its correctness from them.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  every applicable check passed
    2  at least one check failed
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
    [switch]$All,
    [string]$Feature,
    [switch]$Mark
)

$ErrorActionPreference = "Stop"

$MarkerRelative = ".evidence-first/last-check"

$SkipDirs = @(".git", "node_modules", "bin", "obj", "dist", "coverage",
              "__pycache__", ".venv", "target", "_archive", ".evidence-first")

$ShellSuffixes = @(".ps1", ".sh")
$ExtensionlessShell = @("pre-commit", "pre-push", "commit-msg", "post-merge")

$FeaturePathRx = [regex]'`([^`]+\.[A-Za-z0-9]+)`'

# The PowerShell that is running this script, used to launch the sub-checks.
# `pwsh` may not be on PATH -- this kit is routinely run from an extracted
# tarball -- and on Windows PowerShell the executable is powershell.exe, so
# neither name can be hardcoded.
$Shell = [System.Diagnostics.Process]::GetCurrentProcess().MainModule.FileName

# ---------------------------------------------------------------------------
function Test-Residue {
    # Python checks every component of the *absolute* path, because rglob yields
    # root-prefixed paths. Mirrored exactly rather than improved: a twin that is
    # more careful than its original still disagrees with it.
    param([string]$FullPath)
    foreach ($part in ($FullPath -split "[/\\]")) {
        if ($SkipDirs -contains $part) { return $true }
    }
    return $false
}

function Get-ChangedSince {
    param([string]$RootPath, [datetime]$Since)
    $found = @()
    $items = Get-ChildItem -LiteralPath $RootPath -Recurse -File -Force -ErrorAction SilentlyContinue
    foreach ($item in $items) {
        if (Test-Residue $item.FullName) { continue }
        if ($item.LastWriteTimeUtc -gt $Since) { $found += $item.FullName }
    }
    return @($found | Sort-Object)
}

function Get-AllFiles {
    param([string]$RootPath)
    return Get-ChangedSince $RootPath ([datetime]::MinValue)
}

function Get-FeatureFiles {
    param([string]$RootPath, [string]$Name)
    $docs = Join-Path $RootPath "docs"
    $candidates = @()
    if (Test-Path -LiteralPath $docs) {
        $candidates = @(Get-ChildItem -LiteralPath $docs -Recurse -File -Filter ($Name + ".current.md") -ErrorAction SilentlyContinue)
    }
    if ($candidates.Count -eq 0) {
        throw "[check-last:feature-document-missing] no current document found for feature '$Name'"
    }
    $found = @()
    foreach ($document in $candidates) {
        $text = [System.IO.File]::ReadAllText($document.FullName) -replace "`r`n", "`n"
        foreach ($match in $FeaturePathRx.Matches($text)) {
            $candidate = Join-Path $RootPath $match.Groups[1].Value
            if (Test-Path -LiteralPath $candidate -PathType Leaf) {
                $found += (Resolve-Path -LiteralPath $candidate).Path
            }
        }
    }
    return @($found | Sort-Object -Unique)
}

function Test-ShellScript {
    param([string]$FullPath)
    $extension = [System.IO.Path]::GetExtension($FullPath).ToLower()
    if ($ShellSuffixes -contains $extension) { return $true }
    return ($ExtensionlessShell -contains [System.IO.Path]::GetFileName($FullPath))
}

function Get-DeclaredState {
    param([string]$StackPath)
    $manifest = Join-Path $StackPath "STACK-READINESS.json"
    if (-not (Test-Path -LiteralPath $manifest)) { return "" }
    try {
        $parsed = [System.IO.File]::ReadAllText($manifest) | ConvertFrom-Json
    } catch {
        return ""
    }
    if ($null -eq $parsed.declared_state) { return "" }
    return ([string]$parsed.declared_state).Trim()
}

function Get-TouchedStacks {
    param([string]$RootPath, [string[]]$Files)
    $stacks = @()
    $prefix = $RootPath.TrimEnd([char]47, [char]92)
    foreach ($file in $Files) {
        if (-not $file.StartsWith($prefix)) { continue }
        $relative = $file.Substring($prefix.Length).TrimStart([char]47, [char]92)
        $parts = @($relative -split "[/\\]" | Where-Object { $_ -ne "" })
        if ($parts.Count -ge 2 -and $parts[0] -eq "stacks" -and $parts[1] -ne "_template") {
            $stack = Join-Path (Join-Path $RootPath "stacks") $parts[1]
            if (Test-Path -LiteralPath (Join-Path $stack "STACK-READINESS.json")) {
                if ($stacks -notcontains $stack) { $stacks += $stack }
            }
        }
    }
    return @($stacks | Sort-Object)
}

function Get-Plan {
    # Route the changed set to the checks that can judge it.
    param([string]$RootPath, [string[]]$Files, [bool]$Everything)
    $tools = Join-Path $RootPath "tools"
    $jobs = @()

    $anyShell = $false
    foreach ($file in $Files) { if (Test-ShellScript $file) { $anyShell = $true; break } }
    if ($Everything -or $anyShell) {
        $script = Join-Path $tools "check-shell-safety/check_shell_safety.ps1"
        if (Test-Path -LiteralPath $script -PathType Leaf) {
            $jobs += @{ label = "shell safety";
                        arguments = @("-NoProfile", "-NonInteractive", "-File", $script, "-Root", $RootPath) }
        }
    }

    $prefix = $RootPath.TrimEnd([char]47, [char]92)
    $stateTouched = $Everything
    if (-not $stateTouched) {
        foreach ($file in $Files) {
            if (-not $file.StartsWith($prefix)) { continue }
            $relative = $file.Substring($prefix.Length).TrimStart([char]47, [char]92)
            $parts = @($relative -split "[/\\]" | Where-Object { $_ -ne "" })
            if ($parts.Count -gt 0 -and $parts[0] -eq "docs") { $stateTouched = $true; break }
        }
    }
    $script = Join-Path $tools "check-state-model/check_state_model.ps1"
    # Only when this tree is a *project* using the kit. A kit mirror also has a
    # `docs/` directory, but it holds kit documentation, not project state --
    # judging it as project state is a false positive on a correct tree.
    if ($stateTouched -and (Test-Path -LiteralPath $script -PathType Leaf) -and
        (Test-Path -LiteralPath (Join-Path $RootPath "docs/project-map.md") -PathType Leaf)) {
        $jobs += @{ label = "state model";
                    arguments = @("-NoProfile", "-NonInteractive", "-File", $script,
                                  "-ProjectDocs", (Join-Path $RootPath "docs")) }
    }

    $script = Join-Path $tools "check-stack-readiness/check_stack_readiness.ps1"
    if (Test-Path -LiteralPath $script -PathType Leaf) {
        $stacksRoot = Join-Path $RootPath "stacks"
        if ($Everything -and (Test-Path -LiteralPath $stacksRoot)) {
            $manifests = @(Get-ChildItem -LiteralPath $stacksRoot -Directory -ErrorAction SilentlyContinue |
                           Where-Object { Test-Path -LiteralPath (Join-Path $_.FullName "STACK-READINESS.json") } |
                           Sort-Object -Property FullName)
            $stacks = @($manifests | ForEach-Object { $_.FullName })
        } else {
            $stacks = Get-TouchedStacks $RootPath $Files
        }
        foreach ($stack in $stacks) {
            # A stack that declares `blocked` is *supposed* to validate as
            # blocked -- its owner inputs are deliberately unresolved. Counting
            # that as a failure would flag every placeholder in the tree, and one
            # false alarm is enough for the operator to stop running this.
            if ((Get-DeclaredState $stack) -eq "blocked") { continue }
            $jobs += @{ label = "stack readiness: " + [System.IO.Path]::GetFileName($stack);
                        arguments = @("-NoProfile", "-NonInteractive", "-File", $script,
                                      "-Stack", $stack, "-AllowProvisional") }
        }
    }

    return $jobs
}

# ---------------------------------------------------------------------------
try {
    $rootPath = [System.IO.Path]::GetFullPath(
        [System.IO.Path]::Combine((Get-Location).Path, $Root))
    $marker = Join-Path $rootPath $MarkerRelative
    $markerDirectory = [System.IO.Path]::GetDirectoryName($marker)
    if (-not (Test-Path -LiteralPath $markerDirectory)) {
        # [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
        # -LiteralPath parameter at all (only -Path, which expands wildcards), so a
        # path containing [ ] * ? cannot be created safely through it. The .NET call
        # is literal by definition and creates intermediate directories.
        [void][System.IO.Directory]::CreateDirectory($markerDirectory)
    }

    $stamp = [System.DateTime]::UtcNow.Subtract(
        [datetime]"1970-01-01T00:00:00Z").TotalSeconds

    if ($Mark) {
        [System.IO.File]::WriteAllText($marker, "$stamp`n")
        Write-Output ("Baseline reset: " + $MarkerRelative)
        exit 0
    }

    if ($All) {
        $files = Get-AllFiles $rootPath
        $scope = "whole tree"
    } elseif ($Feature) {
        $files = Get-FeatureFiles $rootPath $Feature
        $scope = "feature '" + $Feature + "'"
    } elseif (Test-Path -LiteralPath $marker -PathType Leaf) {
        $since = (Get-Item -LiteralPath $marker).LastWriteTimeUtc
        $files = Get-ChangedSince $rootPath $since
        $scope = "changed since the last run"
    } else {
        $files = Get-AllFiles $rootPath
        $scope = "whole tree (no baseline yet)"
    }

    # Update the baseline before printing: an interrupted run must still leave a
    # correct marker, or the next run silently re-checks the world.
    [System.IO.File]::WriteAllText($marker, "$stamp`n")

    $jobs = @(Get-Plan $rootPath $files ([bool]$All))
    Write-Output ("check-last: " + $files.Count + " file(s), scope = " + $scope)

    if ($jobs.Count -eq 0) {
        Write-Output "  nothing applicable changed"
        Write-Output "  result: CLEAN"
        exit 0
    }

    $failures = @()
    foreach ($job in $jobs) {
        $previous = $ErrorActionPreference
        $ErrorActionPreference = "Continue"
        $output = (& $Shell @($job.arguments) 2>&1 | Out-String)
        $code = $LASTEXITCODE
        $ErrorActionPreference = $previous
        if ($code -eq 0) {
            Write-Output ("  OK    " + $job.label)
        } else {
            # The routed check's own identifiers travel with its output, which is
            # what makes this traceable to a rule instead of to the router.
            [Console]::Error.Write($output)
            Write-Output ("  FAIL  [check-last:routed-check-failed] " + $job.label)
            $failures += $job.label
        }
    }

    if ($failures.Count -gt 0) {
        Write-Output ("  result: BLOCKED (" + $failures.Count + " check(s) failed)")
        exit 2
    }
    Write-Output "  result: CLEAN"
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
