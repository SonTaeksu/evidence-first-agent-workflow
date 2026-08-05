# SPDX-License-Identifier: MPL-2.0
<#
  check_stack_readiness.ps1 — PowerShell twin of check_stack_readiness.py.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Evidence is measured, not declared: each cited path is resolved against the
  tree. See the .py twin for why -- a manifest with entirely invented evidence
  used to report READY, exit 0.

  STACK-INPUTS.md and STACK-READINESS.json are also compared, joined on a
  backticked key column. A disagreement is a warning, and a warning derives
  `provisional`, so a stack declaring `ready` with disagreeing files fails.

  Exit codes:
    0  ready, or provisional with -AllowProvisional
    2  blocked, unresolved required input, or unaccepted provisional state
    1  tool or file error
#>
param(
    [Parameter(Mandatory = $true)][string]$Stack,
    [string]$Manifest,
    [string]$Output,
    [switch]$AllowProvisional,
    [string]$ProjectRoot
)

$ErrorActionPreference = "Stop"

$Resolved = @("confirmed", "detected", "not-applicable")
$Allowed  = @("confirmed", "detected", "not-applicable", "unknown")
$RequiredDefault = @(
    "STACK.md", "STACK-INPUTS.md", "AGENTS.stack.md", "SKILL.md",
    "capability-detection.md", "feature-model.md", "artifact-contract.md",
    "communication-contract.md", "evidence-provenance.md",
    "references/_index.md", "references/pitfalls.md", "references/verified-facts.md",
    "skeletons/README.md", "validation/validation-profile.md"
)

function Get-Text($value) {
    if ($null -eq $value) { return "" }
    return [string]$value
}

function Test-Empty($value) {
    if ($null -eq $value) { return $true }
    if ($value -is [System.Collections.IEnumerable] -and -not ($value -is [string])) {
        return (@($value).Count -eq 0)
    }
    return [string]::IsNullOrEmpty([string]$value)
}



$InputsDocument = "STACK-INPUTS.md"
$BacktickedRx = [regex]'`([^`]+)`'

function Get-DocumentStatuses {
    # The statuses the human-facing tables in STACK-INPUTS.md claim, joined to the
    # manifest through a backticked key column. Joining on the prose would break the
    # moment somebody improved a sentence.
    #
    # A key with no row returns nothing: being unable to compare is not the same as
    # disagreeing.
    param([string]$StackPath, $Keys)
    $result = @{}
    $document = Join-Path $StackPath $InputsDocument
    if (-not (Test-Path -LiteralPath $document -PathType Leaf)) { return $result }
    try {
        $text = [System.IO.File]::ReadAllText($document) -replace "`r`n", "`n"
    } catch {
        return $result
    }
    foreach ($line in ($text -split "`n")) {
        $stripped = $line.Trim()
        if (-not $stripped.StartsWith("|")) { continue }
        $cells = @($stripped.Trim([char]124) -split "\|" | ForEach-Object { $_.Trim() })
        if ($cells.Count -lt 2) { continue }
        $matched = $null
        foreach ($cell in $cells) {
            foreach ($hit in $BacktickedRx.Matches($cell)) {
                $token = $hit.Groups[1].Value
                if ($Keys -contains $token) { $matched = $token; break }
            }
            if ($matched) { break }
        }
        if ($null -eq $matched) { continue }
        $status = $cells[$cells.Count - 1].Trim().Trim([char]96).ToLower()
        if (-not $status) { $status = "unknown" }
        if (-not $result.ContainsKey($matched)) { $result[$matched] = @() }
        if ($result[$matched] -notcontains $status) { $result[$matched] += $status }
    }
    return $result
}

function Compare-Document {
    # Warn when STACK-INPUTS.md and STACK-READINESS.json disagree. A warning derives
    # `provisional`, so a stack declaring `ready` with disagreeing files fails on the
    # declared-state mismatch. Intended, not a side effect -- see the .py twin.
    param([string]$StackPath, $ManifestStatuses)
    $messages = @()
    $keys = @($ManifestStatuses.Keys)
    $documented = Get-DocumentStatuses $StackPath $keys
    foreach ($key in ($documented.Keys | Sort-Object)) {
        if (-not $ManifestStatuses.ContainsKey($key)) { continue }
        $expected = $ManifestStatuses[$key]
        $statuses = @($documented[$key])
        if ($statuses -notcontains $expected) {
            $shown = (($statuses | Sort-Object) -join ", ")
            $messages += ("[check-stack-readiness:inputs-document-drift] " + $key + ": " +
                $InputsDocument + " says '" + $shown + "' but STACK-READINESS.json says '" +
                $expected + "'. Both must agree - the document is what a person reads and " +
                "the manifest is what this check reads. Update whichever is behind.")
        }
    }
    return @($messages)
}

# Files whose presence marks the root of the project a stack governs.
$RootMarkers = @("AGENTS.md", "DESIGN-CONCEPTS.md", "repository-manifest.json")
$GlobCharacters = @([char]42, [char]63, [char]91)   # * ? [

function Find-ProjectRoot {
    param([string]$StackPath)
    $current = $StackPath
    while ($true) {
        foreach ($marker in $RootMarkers) {
            if (Test-Path -LiteralPath (Join-Path $current $marker)) { return $current }
        }
        $parent = [System.IO.Path]::GetDirectoryName($current)
        if (-not $parent -or $parent -eq $current) { break }
        $current = $parent
    }
    return $StackPath
}

function Test-EvidenceResolves {
    # Does this one evidence reference name something that exists?
    #
    # Resolved against the stack directory first, then the project root, because a
    # profile legitimately cites its own documents *and* files in the project it
    # governs. A leading `/` means project-root-relative and nothing else.
    param([string]$StackPath, [string]$RootPath, [string]$Reference)
    $text = (Get-Text $Reference).Trim() -replace '\\', '/'
    if (-not $text) { return $false }
    if ($text.StartsWith("/")) {
        $bases = @($RootPath)
        $text = $text.TrimStart([char]47)
    } else {
        $bases = @($StackPath, $RootPath)
    }
    if (-not $text) { return $false }
    $isGlob = $false
    foreach ($character in $GlobCharacters) {
        if ($text.IndexOf($character) -ge 0) { $isGlob = $true; break }
    }
    foreach ($base in $bases) {
        if ($isGlob) {
            # The wildcard is split off and passed as -Filter, so the *base* path is
            # still matched literally with -LiteralPath. That matters: a project
            # living under a directory called `project [old]` is the exact case the
            # kit's shell-safety rule guards, and using -Path here would have made
            # this tool fail on it while looking correct.
            $patternDirectory = [System.IO.Path]::GetDirectoryName($text)
            $pattern = [System.IO.Path]::GetFileName($text)
            $searchBase = $base
            if ($patternDirectory) { $searchBase = Join-Path $base $patternDirectory }
            if (Test-Path -LiteralPath $searchBase) {
                $hits = @(Get-ChildItem -LiteralPath $searchBase -Filter $pattern -Force -ErrorAction SilentlyContinue)
                if ($hits.Count -gt 0) { return $true }
            }
        } elseif (Test-Path -LiteralPath (Join-Path $base $text)) {
            return $true
        }
    }
    return $false
}


function Measure-Evidence {
    param([string]$StackPath, [string]$RootPath, [string]$Label, [string]$Key, $Evidence)
    $found = @()
    $missing = @()
    foreach ($reference in @($Evidence)) {
        if (Test-EvidenceResolves $StackPath $RootPath (Get-Text $reference)) {
            $found += (Get-Text $reference)
        } else {
            $missing += (Get-Text $reference)
        }
    }
    # At least one must resolve, not all: a profile may list several candidate
    # manifests and a project with only some of them is not thereby unevidenced.
    # Nothing resolving is the forgery, and that fails.
    if ($found.Count -eq 0) {
        return @{ failure = ("[check-stack-readiness:evidence-not-found] " + $Label + " " + $Key +
                             ": no cited evidence exists (" + ($missing -join ", ") + ")");
                  warning = "" }
    }
    if ($missing.Count -gt 0) {
        return @{ failure = "";
                  warning = ("[check-stack-readiness:evidence-partly-missing] " + $Label + " " +
                             $Key + ": " + ($missing -join ", ")) }
    }
    return @{ failure = ""; warning = "" }
}

try {
    $stackPath = (Resolve-Path -LiteralPath $Stack).Path
    if ($ProjectRoot) {
        $rootPath = (Resolve-Path -LiteralPath $ProjectRoot).Path
    } else {
        $rootPath = Find-ProjectRoot $stackPath
    }
    if ($Manifest) {
        $manifestPath = (Resolve-Path -LiteralPath $Manifest).Path
    } else {
        $manifestPath = Join-Path $stackPath "STACK-READINESS.json"
    }
    # NOTE: PowerShell variable names are case-insensitive, so a local named
    # $manifest would BE the [string]$Manifest parameter and the parsed object
    # would be coerced to a string - every check then silently finds nothing.
    $manifestData = Get-Content -Raw -LiteralPath $manifestPath -Encoding UTF8 | ConvertFrom-Json

    $failures = @()
    $warnings = @()
    # Notes are advisory only and are merged into $warnings *after* the derived
    # state is computed, so they are reported and cannot move it. A warning would
    # derive `provisional` and then contradict a manifest declaring `ready`.
    $notes = @()

    # -- required documents ------------------------------------------------
    $requiredDocuments = $RequiredDefault
    if ($manifestData.PSObject.Properties.Name -contains "required_documents") {
        $declaredDocs = $manifestData.required_documents
        if ($declaredDocs -is [string] -or -not ($declaredDocs -is [System.Collections.IEnumerable])) {
            $failures += "[check-stack-readiness:bad-schema] required_documents must be an array."
            $requiredDocuments = @()
        } else {
            $requiredDocuments = @($declaredDocs)
        }
    }
    foreach ($relative in $requiredDocuments) {
        $candidate = Join-Path $stackPath ([string]$relative)
        $ok = $false
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            if ((Get-Item -LiteralPath $candidate).Length -gt 0) { $ok = $true }
        }
        if (-not $ok) {
            $failures += "[check-stack-readiness:missing-document] $relative"
        }
    }

    # -- inputs ------------------------------------------------------------
    $inputs = @()
    if ($manifestData.PSObject.Properties.Name -contains "inputs") {
        $declaredInputs = $manifestData.inputs
        if ($declaredInputs -is [string] -or -not ($declaredInputs -is [System.Collections.IEnumerable])) {
            $failures += "[check-stack-readiness:bad-schema] inputs must be an array."
        } else {
            $inputs = @($declaredInputs)
        }
    }
    foreach ($item in $inputs) {
        $key = "<missing-key>"
        if ($item.PSObject.Properties.Name -contains "key") { $key = Get-Text $item.key }
        $status = "unknown"
        if ($item.PSObject.Properties.Name -contains "status") { $status = Get-Text $item.status }
        $required = $false
        if ($item.PSObject.Properties.Name -contains "required") { $required = [bool]$item.required }
        $evidence = $null
        if ($item.PSObject.Properties.Name -contains "evidence") { $evidence = $item.evidence }

        if ($Allowed -notcontains $status) {
            $failures += "[check-stack-readiness:invalid-status] input ${key}: '$status'"
            continue
        }
        if ($required -and ($Resolved -notcontains $status)) {
            $failures += "[check-stack-readiness:input-unresolved] $key"
        }
        if (($status -eq "confirmed" -or $status -eq "detected") -and (Test-Empty $evidence)) {
            $failures += "[check-stack-readiness:input-without-evidence] $key ($status)"
        }
        elseif ($Resolved -contains $status -and $status -ne "not-applicable") {
            $measured = Measure-Evidence $stackPath $rootPath "input" $key $evidence
            if ($measured.failure) { $failures += $measured.failure }
            if ($measured.warning) { $notes += $measured.warning }
        }
        if ((-not $required) -and $status -eq "unknown") {
            $warnings += "[check-stack-readiness:optional-input-unresolved] $key"
        }
    }

    # -- capabilities ------------------------------------------------------
    $capabilities = @()
    if ($manifestData.PSObject.Properties.Name -contains "capabilities") {
        $declaredCaps = $manifestData.capabilities
        if ($declaredCaps -is [string] -or -not ($declaredCaps -is [System.Collections.IEnumerable])) {
            $failures += "[check-stack-readiness:bad-schema] capabilities must be an array."
        } else {
            $capabilities = @($declaredCaps)
        }
    }
    foreach ($item in $capabilities) {
        $key = "<missing-key>"
        if ($item.PSObject.Properties.Name -contains "key") { $key = Get-Text $item.key }
        $status = "unknown"
        if ($item.PSObject.Properties.Name -contains "status") { $status = Get-Text $item.status }
        $evidence = $null
        if ($item.PSObject.Properties.Name -contains "evidence") { $evidence = $item.evidence }
        $selectedPath = ""
        if ($item.PSObject.Properties.Name -contains "selected_path") {
            $selectedPath = (Get-Text $item.selected_path).Trim()
        }
        $blocks = @()
        if ($item.PSObject.Properties.Name -contains "blocks") { $blocks = @($item.blocks) }

        if (@("present", "absent", "unknown", "not-applicable") -notcontains $status) {
            $failures += "[check-stack-readiness:invalid-status] capability ${key}: '$status'"
            continue
        }
        if ($status -eq "present" -or $status -eq "absent") {
            if (Test-Empty $evidence) {
                $failures += "[check-stack-readiness:capability-without-evidence] $key"
            }
            else {
                $measured = Measure-Evidence $stackPath $rootPath "capability" $key $evidence
                if ($measured.failure) { $failures += $measured.failure }
                if ($measured.warning) { $notes += $measured.warning }
            }
            if ([string]::IsNullOrEmpty($selectedPath)) {
                $failures += "[check-stack-readiness:capability-without-path] $key"
            }
        }
        if ($status -eq "unknown") {
            if ($blocks.Count -gt 0) {
                $rendered = "['" + ($blocks -join "', '") + "']"
                $failures += "[check-stack-readiness:blocking-capability-unresolved] ${key}; blocks=$rendered"
            } else {
                $warnings += "[check-stack-readiness:capability-unresolved] $key"
            }
        }
    }

    # Compared before the state is derived, because a disagreement has to be able
    # to move it.
    $manifestStatuses = @{}
    foreach ($item in $inputs) {
        if ($item.PSObject.Properties.Name -contains "key") {
            $k = Get-Text $item.key
            $s = "unknown"
            if ($item.PSObject.Properties.Name -contains "status") { $s = Get-Text $item.status }
            if ($k) { $manifestStatuses[$k] = $s }
        }
    }
    foreach ($item in $capabilities) {
        if ($item.PSObject.Properties.Name -contains "key") {
            $k = Get-Text $item.key
            $s = "unknown"
            if ($item.PSObject.Properties.Name -contains "status") { $s = Get-Text $item.status }
            if ($k) { $manifestStatuses[$k] = $s }
        }
    }
    $warnings += @(Compare-Document $stackPath $manifestStatuses)

    # -- derive ------------------------------------------------------------
    if ($failures.Count -gt 0) {
        $derived = "blocked"
    } elseif ($warnings.Count -gt 0) {
        $derived = "provisional"
    } else {
        $derived = "ready"
    }

    # Merged only now, after $derived was computed from $warnings alone.
    $warnings += $notes

    $declared = ""
    if ($manifestData.PSObject.Properties.Name -contains "declared_state") {
        $declared = (Get-Text $manifestData.declared_state).Trim()
    }
    if ($declared -and $declared -ne $derived) {
        $failures += ("[check-stack-readiness:declared-state-mismatch] declared '$declared' " +
                      "but derived '$derived'")
        $derived = "blocked"
    }

    if ($Output) {
        $report = [ordered]@{
            schema   = "evidence-first/stack-readiness-report/v1"
            stack    = ($stackPath -replace '\\', '/')
            manifest = ($manifestPath -replace '\\', '/')
            state    = $derived
            failures = $failures
            warnings = $warnings
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

    Write-Output ("Stack readiness: " + $derived.ToUpper())
    foreach ($warning in $warnings) { Write-Output "WARN: $warning" }
    foreach ($failure in $failures) { [Console]::Error.WriteLine("FAIL: $failure") }

    if ($failures.Count -gt 0) { exit 2 }
    if ($derived -eq "provisional" -and -not $AllowProvisional) { exit 2 }
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
