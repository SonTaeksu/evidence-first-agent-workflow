# SPDX-License-Identifier: MPL-2.0
<#
  check_state_model.ps1 — PowerShell twin of check_state_model.py.

  Validates project routing, feature state, history, and worklog structure.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  the state model is well-formed
    2  at least one structural finding
    1  tool error
#>
param(
    [Parameter(Mandatory = $true)][string]$ProjectDocs,
    [string]$WorklogTemplate = "templates/core/worklog.md"
)

$ErrorActionPreference = "Stop"

$ProjectMapSections = @(
    @("## Features"),
    @("## Architecture State"),
    @("## Environment Capabilities"),
    @("## Shared File Reverse Index")
)

$CurrentSections = @(
    @("## Current Behavior"),
    @("## Feature Boundary and Actions", "## Feature Boundary 및 Action"),
    @("## Contracts"),
    @("## Related Files by Role", "## 역할별 Related Files"),
    @("## Shared Dependencies"),
    @("## Environment Capability Decisions"),
    @("## Validation State"),
    @("## Known Issues"),
    @("## Next Candidate Work")
)

$WorklogSections = @(
    @("## 1. Analysis"),
    @("## 2. Task"),
    @("## 3. Todo and Micro-Verify", "## 3. Todo와 Micro-Verify"),
    @("## 4. Checklist"),
    @("## 5. Verification")
)

$FrontMatterFields = @("feature", "status", "code-verified", "last-pr", "updated", "stack")

# ---------------------------------------------------------------------------
function Read-Text {
    # Python's read_text() opens in text mode, so CRLF arrives as LF. ReadAllText
    # does not translate, and every `\n` in the patterns below would then fail to
    # match on a Windows-authored document — the twin would pass a tree the
    # Python side rejects. Normalising here is what keeps the two equal.
    param([string]$Path)
    $text = [System.IO.File]::ReadAllText($Path)
    return ($text -replace "`r`n", "`n")
}

function Get-FrontMatter {
    param([string]$Text)
    $match = [regex]::Match($Text, "^---\s*\n(.*?)\n---\s*\n",
                            [System.Text.RegularExpressions.RegexOptions]::Singleline)
    if ($match.Success) { return $match.Groups[1].Value }
    return ""
}

function Replace-First {
    # PowerShell's -replace is a global regex replace; Python's str.replace(a, b, 1)
    # is a single literal replacement. The worklog template relies on exactly one
    # substitution per fence marker, so a global replace would turn the closing
    # fence into a second opener and the front matter would never parse.
    param([string]$Text, [string]$Search, [string]$Replacement)
    $index = $Text.IndexOf($Search)
    if ($index -lt 0) { return $Text }
    return $Text.Substring(0, $index) + $Replacement +
           $Text.Substring($index + $Search.Length)
}

function Get-Head {
    param([string]$Text, [int]$Count)
    if ($Text.Length -le $Count) { return $Text }
    return $Text.Substring(0, $Count)
}

function Test-AppendOnlyDeclared {
    param([string]$Text)
    $head = Get-Head $Text 500
    return ($head.Contains("Append-only") -or $head.Contains("Append-only입니다"))
}

function Add-SectionFindings {
    param(
        [string]$Label,
        [string]$Text,
        [object[]]$Sections,
        [System.Collections.ArrayList]$Failures,
        [string]$Finding
    )
    foreach ($alternatives in $Sections) {
        $found = $false
        foreach ($section in $alternatives) {
            if ($Text.Contains($section)) { $found = $true; break }
        }
        if (-not $found) {
            [void]$Failures.Add(
                $Label + ": [check-state-model:" + $Finding +
                "] missing section '" + $alternatives[0] + "'")
        }
    }
}

# ---------------------------------------------------------------------------
try {
    # GetFullPath, not Resolve-Path: Python's Path.resolve() does not require the
    # path to exist, and a missing --project-docs must reach the same finding as
    # on the Python side rather than dying here.
    $docs = [System.IO.Path]::GetFullPath(
        [System.IO.Path]::Combine((Get-Location).Path, $ProjectDocs))
    $failures = New-Object System.Collections.ArrayList
    $checks = @()

    $projectMap = Join-Path $docs "project-map.md"
    if (-not (Test-Path -LiteralPath $projectMap)) {
        [void]$failures.Add("[check-state-model:missing-project-map] Missing project-map.md")
    } else {
        $text = Read-Text $projectMap
        Add-SectionFindings "project-map.md" $text $ProjectMapSections $failures "project-map-section-missing"
        $checks += "project map"
    }

    $features = Join-Path $docs "features"
    $currentFiles = @()
    if (Test-Path -LiteralPath $features) {
        $currentFiles = @(Get-ChildItem -LiteralPath $features -Filter "*.current.md" -File -ErrorAction SilentlyContinue |
                          Where-Object { -not $_.Name.EndsWith(".current.ko.md") } |
                          Sort-Object -Property FullName)
    }
    if ($currentFiles.Count -eq 0) {
        [void]$failures.Add("[check-state-model:no-current-document] No feature current documents found.")
    }

    foreach ($current in $currentFiles) {
        $text = Read-Text $current.FullName
        $fm = Get-FrontMatter $text
        if (-not $fm) {
            [void]$failures.Add($current.Name +
                ": [check-state-model:missing-front-matter] missing YAML front matter")
        }
        foreach ($field in $FrontMatterFields) {
            $pattern = "(?m)^" + [regex]::Escape($field) + "\s*:"
            if (-not ([regex]$pattern).IsMatch($fm)) {
                [void]$failures.Add($current.Name +
                    ": [check-state-model:front-matter-field-missing] missing front-matter field " + $field)
            }
        }
        Add-SectionFindings $current.Name $text $CurrentSections $failures "current-section-missing"

        $featureKeyMatch = [regex]::Match($fm, "(?m)^feature\s*:\s*(.+)$")
        if ($featureKeyMatch.Success) {
            $featureKey = $featureKeyMatch.Groups[1].Value.Trim().Trim([char]34)
            $historyName = $featureKey + ".history.md"
            $history = Join-Path $features $historyName
            if (-not (Test-Path -LiteralPath $history)) {
                [void]$failures.Add($current.Name +
                    ": [check-state-model:missing-history] missing " + $historyName)
            } elseif (-not (Test-AppendOnlyDeclared (Read-Text $history))) {
                [void]$failures.Add($historyName +
                    ": [check-state-model:append-only-not-declared] append-only rule not declared")
            }
        }
        $checks += $current.Name
    }

    foreach ($area in @("system", "database")) {
        $architecture = Join-Path $docs "architecture"
        $current = Join-Path $architecture ($area + ".current.md")
        $history = Join-Path $architecture ($area + ".history.md")
        if (-not (Test-Path -LiteralPath $current)) {
            [void]$failures.Add("[check-state-model:missing-architecture-document] Missing architecture/" +
                $area + ".current.md")
        }
        if (-not (Test-Path -LiteralPath $history)) {
            [void]$failures.Add("[check-state-model:missing-architecture-document] Missing architecture/" +
                $area + ".history.md")
        } elseif (-not (Test-AppendOnlyDeclared (Read-Text $history))) {
            [void]$failures.Add("[check-state-model:append-only-not-declared] architecture/" +
                $area + ".history.md: append-only rule not declared")
        }
    }

    $template = $WorklogTemplate
    if (-not [System.IO.Path]::IsPathRooted($template)) {
        $cwdCandidate = Join-Path (Get-Location).Path $template
        if (Test-Path -LiteralPath $cwdCandidate) {
            $template = $cwdCandidate
        } else {
            $repository = $docs
            while ($true) {
                $parent = [System.IO.Path]::GetDirectoryName($repository)
                if (-not $parent -or $parent -eq $repository) { break }
                if ((Test-Path -LiteralPath (Join-Path $repository "DESIGN-CONCEPTS.md")) -or
                    (Test-Path -LiteralPath (Join-Path $repository "repository-manifest.json"))) { break }
                $repository = $parent
            }
            $template = Join-Path $repository $template
        }
    }

    # A missing template is a tool error, matching read_text() raising OSError on
    # the Python side. Reported through the catch below, not as a finding.
    $text = Read-Text $template
    $fenced = Replace-First $text '```yaml' "---"
    $fenced = Replace-First $fenced '```' "---"
    if (-not (Get-FrontMatter $fenced).Contains("current:") -and
        -not (Get-Head $text 500).Contains("current:")) {
        [void]$failures.Add("[check-state-model:template-missing-current-path] worklog template: missing current path")
    }
    Add-SectionFindings "worklog template" $text $WorklogSections $failures "template-section-missing"

    if ($failures.Count -gt 0) {
        foreach ($failure in $failures) { [Console]::Error.WriteLine("FAIL: " + $failure) }
        exit 2
    }

    Write-Output ("State model validation passed: " + ($checks -join ", "))
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
