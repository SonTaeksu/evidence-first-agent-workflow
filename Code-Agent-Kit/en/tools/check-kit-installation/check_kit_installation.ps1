# SPDX-License-Identifier: MPL-2.0
<#
  check_kit_installation.ps1 — PowerShell twin of check_kit_installation.py.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  the installed mirror is complete
    2  a required file or directory is missing, a language suffix remains,
       or a local Markdown link does not resolve
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

$RequiredFiles = @(
    "README.md",
    "AGENTS.md",
    "DESIGN-CONCEPTS.md",
    ".agentignore",
    ".mcp.json",
    ".codex/config.toml",
    ".roo/mcp.json",
    ".roo/rules/10-evidence-first.md",
    ".clinerules/10-evidence-first.md",
    "CLAUDE.md",
    "prompts/GATE.md",
    "prompts/0-sync-and-orient.md",
    "templates/core/worklog.md",
    "templates/core/feature.current.md",
    "templates/core/project-map.md",
    "docs/core/state-and-memory-model.md",
    "docs/getting-started/stack-input-requirements.md",
    "demos/README.md",
    "reference-assets/README.md",
    "tools/check-stack-readiness/check_stack_readiness.py",
    "tools/check-state-model/check_state_model.py",
    "tools/check-kit-selfcheck/check_kit_selfcheck.py",
    "tools/check-mirror-parity/check_mirror_parity.py",
    "tools/check-shell-safety/check_shell_safety.py",
    "tools/check-last/check_last.py",
    "prompts/7-update-the-kit.md",
    "docs/core/command-and-process-safety.md",
    "docs/core/gate-design-principles.md",
    "scripts/pre-commit-validate.ps1",
    "LICENSES.md",
    "KIT-MANIFEST.json"
)

$RequiredDirs = @(
    "docs", "prompts", "templates", "stacks", "tools",
    "scripts", "demos", "reference-assets", "agent-configs", "LICENSES"
)

$Link = [regex]'\[[^\]]+\]\(([^)]+)\)'

function Get-Relative([string]$full, [string]$root) {
    return $full.Substring($root.Length).TrimStart([char]92, [char]47) -replace '\\', '/'
}

try {
    $rootPath = (Resolve-Path -LiteralPath $Root).Path
    $failures = @()

    foreach ($relative in ($RequiredFiles | Sort-Object)) {
        $candidate = Join-Path $rootPath $relative
        if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) {
            $failures += "[check-kit-installation:missing-file] required file: $relative"
        }
    }

    foreach ($relative in ($RequiredDirs | Sort-Object)) {
        $candidate = Join-Path $rootPath $relative
        if (-not (Test-Path -LiteralPath $candidate -PathType Container)) {
            $failures += "[check-kit-installation:missing-directory] required directory: $relative"
        }
    }

    $allFiles = @(Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force -ErrorAction SilentlyContinue)

    foreach ($item in $allFiles) {
        if ($item.Name.Contains(".ko.md")) {
            $failures += ("[check-kit-installation:language-suffix] " + (Get-Relative $item.FullName $rootPath))
        }
    }

    foreach ($item in $allFiles) {
        if ($item.Extension.ToLower() -ne ".md") { continue }
        $relativeDoc = Get-Relative $item.FullName $rootPath
        $text = [System.IO.File]::ReadAllText($item.FullName, [System.Text.Encoding]::UTF8)
        foreach ($match in $Link.Matches($text)) {
            $raw = $match.Groups[1].Value
            $target = $raw.Trim().Trim([char]60, [char]62).Split("#")[0]
            if ([string]::IsNullOrEmpty($target)) { continue }
            if ($target.StartsWith("#") -or $target.StartsWith("http://") -or
                $target.StartsWith("https://") -or $target.StartsWith("mailto:") -or
                $target.Contains("://")) { continue }

            $combined = Join-Path $item.DirectoryName $target
            try {
                $resolved = [System.IO.Path]::GetFullPath($combined)
            } catch {
                $resolved = $null
            }
            if ($null -eq $resolved -or -not $resolved.StartsWith($rootPath, [System.StringComparison]::Ordinal)) {
                $failures += "${relativeDoc}: [check-kit-installation:link-escapes-root] $raw"
                continue
            }
            if (-not (Test-Path -LiteralPath $resolved)) {
                $failures += "${relativeDoc}: [check-kit-installation:missing-link-target] $raw"
            }
        }
    }

    if ($failures.Count -gt 0) {
        foreach ($failure in $failures) {
            [Console]::Error.WriteLine("FAIL: $failure")
        }
        exit 2
    }

    Write-Output ("Kit installation validation passed: " + $allFiles.Count + " files.")
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
