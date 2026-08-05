# SPDX-License-Identifier: MPL-2.0
<#
  enforce_gates.ps1 — PowerShell twin of enforce_gates.py.

  The commit-layer hard gate. On a machine without Python this is the *only*
  thing standing between an undocumented change and the repository, so the two
  implementations must agree on the exit code and on the finding identifiers.
  Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel,
  no null-conditional.

  Exit codes:
    0  all enforced gates pass (or nothing relevant changed)
    2  a hard gate failed -> commit/PR is blocked
    1  tool error -- no verdict could be reached (e.g. not a git repository)
#>
# [CmdletBinding()] is not decoration. Without it a PowerShell script is a
# *simple* script: an argument it does not recognise is quietly collected into
# $args and ignored. A mistyped `-AllowProvisonal` would run the check with the
# switch off and report success. The .py twin exits 1 on an unknown flag, so the
# two also disagreed on every typo -- and no case noticed until one was added.
[CmdletBinding()]
param(
    [switch]$Staged,
    [string]$Base,
    [switch]$StrictScope
)

$ErrorActionPreference = "Stop"

$SourceSuffixes = @(
    ".cs", ".csproj", ".fs", ".vb",
    ".ts", ".tsx", ".js", ".jsx", ".vue", ".svelte",
    ".java", ".kt", ".go", ".rs", ".py",
    ".ex", ".exs", ".php", ".rb",
    ".xjs", ".xfdl", ".xml"
)

$WorkflowRoots = @(
    "docs", "prompts", "templates", "stacks", "tools", "scripts",
    "demos", "reference-assets", "agent-configs", "samples", "LICENSES",
    ".codex", ".roo", ".clinerules", ".agent-state", ".agent-evidence",
    ".github"
)
$IgnoredParts = @(
    ".git", ".vs", "bin", "obj", "node_modules",
    "dist", "coverage", "__pycache__", ".venv"
)

$MandatoryGateSections = @("## 1. Analysis", "## 2. Task", "## 3.", "## 4.", "## 5.")

$SecretPatterns = @(
    @{ rx = [regex]"(?i)(password|passwd|pwd)\s*[:=]\s*['`"][^'`"]{3,}['`"]"; label = "hardcoded password" },
    @{ rx = [regex]"(?i)(secret|api[_-]?key|access[_-]?key|token)\s*[:=]\s*['`"][A-Za-z0-9_\-]{12,}['`"]"; label = "hardcoded secret/key/token" },
    @{ rx = [regex]"-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"; label = "private key" },
    @{ rx = [regex]"AKIA[0-9A-Z]{16}"; label = "AWS access key id" }
)
$SecretAllow = [regex]"(\.example($|\.)|\.sample($|\.)|/tests?/|\.test\.|\.spec\.|_test\.|README|\.md$)"

$ConfigSuffixes = @(".json", ".yml", ".yaml", ".toml", ".env", ".config")

# ---------------------------------------------------------------------------
function Invoke-Git {
    # Mirrors the Python helper: stdout only, never throws, exit code ignored.
    # git writes to stderr on failure and the Python side discards that, so the
    # redirection here is what keeps the two outputs identical.
    param([string[]]$Arguments)
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $out = & git @Arguments 2>$null
    } catch {
        $out = @()
    }
    $ErrorActionPreference = $previous
    if ($null -eq $out) { return "" }
    return ($out -join "`n")
}

function Get-ChangedFiles {
    param([string]$BaseRef)
    if ($BaseRef) {
        $out = Invoke-Git @("diff", "--name-only", "--diff-filter=ACMR", $BaseRef, "--")
    } else {
        $out = Invoke-Git @("diff", "--cached", "--name-only", "--diff-filter=ACMR")
    }
    $files = @()
    foreach ($line in ($out -split "`r?`n")) {
        $relative = $line.Trim() -replace '\\', '/'
        # Python's str.lstrip("./") strips any leading run of '.' and '/'
        # characters, not the literal prefix "./" -- matching that exactly
        # matters for a path like "./x" and for one like "../x".
        $relative = $relative.TrimStart([char]46, [char]47)
        if ($relative) { $files += $relative }
    }
    return $files
}

function Get-StagedBlob {
    param([string]$RelativePath, [string]$BaseRef)
    if ($BaseRef) { $ref = $BaseRef + ":" + $RelativePath } else { $ref = ":" + $RelativePath }
    $previous = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    $out = & git show $ref 2>$null
    $code = $LASTEXITCODE
    $ErrorActionPreference = $previous
    if ($code -ne 0) {
        if (Test-Path -LiteralPath $RelativePath) {
            return [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $RelativePath).Path)
        }
        return ""
    }
    if ($null -eq $out) { return "" }
    return ($out -join "`n")
}

function Get-PathParts {
    param([string]$RelativePath)
    return @($RelativePath -split "/" | Where-Object { $_ -ne "" })
}

function Test-ProjectSource {
    param([string]$RelativePath)
    $parts = Get-PathParts $RelativePath
    foreach ($part in $parts) {
        if ($IgnoredParts -contains $part) { return $false }
    }
    if ($parts.Count -gt 0 -and ($WorkflowRoots -contains $parts[0])) { return $false }
    $extension = [System.IO.Path]::GetExtension($RelativePath).ToLower()
    return ($SourceSuffixes -contains $extension)
}

function Get-SecretFindings {
    param([string[]]$Changed, [string]$BaseRef)
    $failures = @()
    foreach ($relative in $Changed) {
        if ($SecretAllow.IsMatch($relative)) { continue }
        $extension = [System.IO.Path]::GetExtension($relative).ToLower()
        $isSource = $SourceSuffixes -contains $extension
        $isConfig = $false
        foreach ($suffix in $ConfigSuffixes) {
            if ($relative.EndsWith($suffix)) { $isConfig = $true; break }
        }
        if (-not $isSource -and -not $isConfig) { continue }
        $content = Get-StagedBlob $relative $BaseRef
        foreach ($pattern in $SecretPatterns) {
            if ($pattern.rx.IsMatch($content)) {
                $failures += "[enforce-agent-gates:hardcoded-secret] " + $pattern.label + " in " + $relative
                break
            }
        }
    }
    return $failures
}

function Find-ActiveWorklog {
    param([string[]]$Changed)
    $rx = [regex]"(^|/)docs/worklogs/.+\.md$"
    foreach ($relative in $Changed) {
        if ($rx.IsMatch($relative) -and $relative -notlike "*README*") { return $relative }
    }
    $directory = Join-Path (Get-Location).Path "docs/worklogs"
    if (-not (Test-Path -LiteralPath $directory)) { return $null }
    $hits = @(Get-ChildItem -LiteralPath $directory -Filter "*.md" -File -ErrorAction SilentlyContinue |
              Where-Object { $_.Name -notlike "*README*" } |
              Sort-Object -Property FullName)
    if ($hits.Count -eq 0) { return $null }
    # Python sorts full paths and takes the last one.
    return $hits[$hits.Count - 1].FullName
}

function Read-WorklogText {
    param([string]$Worklog)
    if (-not $Worklog) { return $null }
    if (-not (Test-Path -LiteralPath $Worklog)) { return $null }
    return [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $Worklog).Path)
}

function Get-WorklogFindings {
    param([string[]]$SourceChanges, [string[]]$Changed)
    if ($SourceChanges.Count -eq 0) { return @() }
    $failures = @()
    $worklog = Find-ActiveWorklog $Changed
    $text = Read-WorklogText $worklog
    if ($null -eq $text) {
        return @("[enforce-agent-gates:worklog-missing] project source changed but no worklog under docs/worklogs/ was produced (GATE.md 5-section evidence missing).")
    }
    foreach ($section in $MandatoryGateSections) {
        if (-not $text.Contains($section)) {
            $failures += "[enforce-agent-gates:worklog-section-missing] worklog " + $worklog + " missing section '" + $section + "'"
        }
    }
    if ($text.Contains("Expected Files")) {
        $index = $text.IndexOf("Expected Files")
        $tail = $text.Substring($index + "Expected Files".Length)
        if (-not ([regex]"(?m)^\s*-\s*\[[ xX]\]\s+\S+").IsMatch($tail)) {
            $failures += "[enforce-agent-gates:expected-files-empty] worklog " + $worklog + ": 'Expected Files' has no concrete entry."
        }
    }
    return $failures
}

function Get-StateFindings {
    param([string[]]$SourceChanges, [string[]]$Changed)
    # current/history sync is a hard block; project-map is only *reviewed* for
    # shared-file impact, so its absence is a warning.
    $result = @{ failures = @(); warnings = @() }
    if ($SourceChanges.Count -eq 0) { return $result }

    $currentRx = [regex]"docs/features/.+\.current\.md$"
    $historyRx = [regex]"docs/features/.+\.history\.md$"

    $hasCurrent = $false
    $hasHistory = $false
    $hasMap = $false
    foreach ($relative in ($Changed | Select-Object -Unique)) {
        if ($currentRx.IsMatch($relative)) { $hasCurrent = $true }
        if ($historyRx.IsMatch($relative)) { $hasHistory = $true }
        if ($relative.EndsWith("docs/project-map.md")) { $hasMap = $true }
    }
    if (-not $hasCurrent) {
        $result.failures += "[enforce-agent-gates:current-not-updated] source changed but no feature '*.current.md' was updated."
    }
    if (-not $hasHistory) {
        $result.failures += "[enforce-agent-gates:history-not-appended] source changed but no feature '*.history.md' append was made."
    }
    if (-not $hasMap) {
        $result.warnings += "[enforce-agent-gates:project-map-not-touched] 'docs/project-map.md' not touched - confirm no shared-file/impact change is unrecorded."
    }
    return $result
}

function Get-VerificationSection {
    param([string]$Text)
    $lines = $Text -split "`r?`n"
    $headingRx = [regex]"^#{1,6}\s"
    $subjectRx = [regex]"(?i)verification|검증|##\s*5\b"
    $stopRx = [regex]"^##\s"
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($headingRx.IsMatch($lines[$i]) -and $subjectRx.IsMatch($lines[$i])) { $start = $i; break }
    }
    if ($start -lt 0) { return "" }
    $out = @()
    for ($i = $start + 1; $i -lt $lines.Count; $i++) {
        if ($stopRx.IsMatch($lines[$i])) { break }
        $out += $lines[$i]
    }
    return ($out -join "`n")
}

function Get-VerificationFindings {
    param([string[]]$SourceChanges, [string[]]$Changed)
    # A PASS with no cited command/exit is not evidence. Conservative: block only
    # when the Verification section claims PASS but has NO evidence token at all.
    if ($SourceChanges.Count -eq 0) { return @() }
    $worklog = Find-ActiveWorklog $Changed
    $text = Read-WorklogText $worklog
    if ($null -eq $text) { return @() }
    $section = Get-VerificationSection $text
    if (-not $section.Trim()) { return @() }
    $claims = ([regex]"(?i)\bPASS\b|✅|완료|\bDONE\b").IsMatch($section)
    if (-not $claims) { return @() }
    $hasEvidence = $section.Contains("``") -or ([regex]"\d").IsMatch($section)
    if (-not $hasEvidence) {
        return @("[enforce-agent-gates:verification-without-evidence] worklog Verification claims PASS with no evidence at all (no command, no exit code). Cite the command and exit code, or mark PENDING.")
    }
    return @()
}

function Get-ScopeFindings {
    param([string[]]$SourceChanges, [string[]]$Changed)
    if ($SourceChanges.Count -eq 0) { return @() }
    $worklog = Find-ActiveWorklog $Changed
    $declared = Read-WorklogText $worklog
    if ($null -eq $declared) { return @() }
    $findings = @()
    foreach ($source in $SourceChanges) {
        $name = [System.IO.Path]::GetFileName($source)
        if (-not $declared.Contains($name) -and -not $declared.Contains($source)) {
            $findings += "[enforce-agent-gates:file-not-declared] source file not declared in worklog Expected Files: " + $source
        }
    }
    return $findings
}

# ---------------------------------------------------------------------------
try {
    $baseRef = ""
    if ($Base) { $baseRef = $Base }

    if ((Invoke-Git @("rev-parse", "--is-inside-work-tree")).Trim() -ne "true") {
        # A tool error (1), not a validation failure (2). See the .py twin.
        [Console]::Error.WriteLine("[enforce-agent-gates:not-a-repository] not inside a git repository - this gate reads the staged diff and has nothing to read.")
        exit 1
    }

    $changed = @(Get-ChangedFiles $baseRef)
    $sourceChanges = @($changed | Where-Object { Test-ProjectSource $_ })

    $failures = @()
    $warnings = @()

    $failures += @(Get-SecretFindings $changed $baseRef)
    $failures += @(Get-WorklogFindings $sourceChanges $changed)
    $state = Get-StateFindings $sourceChanges $changed
    $failures += @($state.failures)
    $warnings += @($state.warnings)

    $scopeFindings = @(Get-ScopeFindings $sourceChanges $changed)
    if ($StrictScope) { $failures += $scopeFindings } else { $warnings += $scopeFindings }

    $failures += @(Get-VerificationFindings $sourceChanges $changed)

    if ($baseRef) { $mode = "CI diff vs " + $baseRef } else { $mode = "staged (pre-commit)" }
    Write-Output "Evidence-First enforcement gate"
    Write-Output ("  mode           : " + $mode)
    Write-Output ("  changed files  : " + $changed.Count)
    Write-Output ("  project source : " + $sourceChanges.Count)
    foreach ($warning in $warnings) { Write-Output ("  WARN  " + $warning) }

    if ($sourceChanges.Count -eq 0 -and $failures.Count -eq 0) {
        Write-Output "  result         : PASS (no project source change to govern)"
        exit 0
    }

    if ($failures.Count -gt 0) {
        Write-Output "  result         : BLOCKED"
        foreach ($failure in $failures) { [Console]::Error.WriteLine("  FAIL  " + $failure) }
        [Console]::Error.WriteLine("")
        [Console]::Error.WriteLine("Run the workflow before committing (prompts/0-sync-and-orient.md -> prompts/GATE.md). If source was changed out of order, follow docs/core/recovery-mode.md. Explicit human override: git commit --no-verify")
        exit 2
    }

    Write-Output "  result         : PASS"
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
