# SPDX-License-Identifier: MPL-2.0
<#
  check_sanitization.ps1 — PowerShell twin of check_sanitization.py.

  Public-release gate. Scans a tree for proprietary / organization-identifying
  strings and generic credential patterns.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  clean
    2  one or more denylisted or secret matches (release blocked)
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
    [string[]]$ExtraDeny = @(),
    [string[]]$AllowGlob = @(),
    [switch]$StrictReview
)

$ErrorActionPreference = "Stop"

# Hard-block: organization / product / proprietary identifiers.
# Kept byte-identical in meaning to the Python list; see that file for why each
# entry exists. This script is itself excluded from the scan, because the list
# below necessarily contains the very strings it forbids.
$Deny = @(
    @{ p = "한화\s*시스템"; why = "org name" },
    @{ p = "\bHanwha\b";                        why = "org name" },
    @{ p = "\bAONDev\b";                        why = "internal platform name" },
    @{ p = "\bOceanDev\b";                      why = "internal platform name" },
    @{ p = "nexacro-aondev";                    why = "internal stack pack folder/skill name" },
    @{ p = "\baondev\b";                        why = "internal identifier" },
    @{ p = "\bgfn_[A-Za-z]";                    why = "proprietary CommLib function prefix" },
    @{ p = "\blfn_[A-Za-z]";                    why = "proprietary CommLib function prefix" },
    @{ p = "cell_WF_";                          why = "project-specific class" },
    @{ p = "TOBESOFT";                          why = "vendor install path/brand" },
    @{ p = "Program Files.*Nexacro";            why = "absolute vendor SDK path" },
    @{ p = "nexacrodeploy";                     why = "vendor build tool path" }
)

$Review = @(
    @{ p = "\bNexacro\b"; why = "third-party trademark - confirm it is only a named example stack" },
    @{ p = "\bX-API\b";   why = "vendor API name - confirm generic context" }
)

$Secret = @(
    @{ p = "(?i)(password|passwd|pwd)\s*[:=]\s*['`"][^'`"]{3,}['`"]"; why = "hardcoded password" },
    @{ p = "(?i)(secret|api[_-]?key|access[_-]?key|token)\s*[:=]\s*['`"][A-Za-z0-9_\-]{12,}['`"]"; why = "hardcoded secret/key/token" },
    @{ p = "-----BEGIN (RSA |EC |OPENSSH |PGP )?PRIVATE KEY-----"; why = "private key" },
    @{ p = "AKIA[0-9A-Z]{16}"; why = "AWS access key id" }
)

$SkipDirs = @(".git", "node_modules", "bin", "obj", "dist", "coverage",
              "__pycache__", ".venv", "target", "check-sanitization")
$SkipSuffix = @(".png", ".jpg", ".jpeg", ".gif", ".ico", ".pdf", ".zip",
                ".woff", ".woff2", ".ttf", ".jar", ".dll", ".exe", ".lock")

try {
    $rootPath = (Resolve-Path -LiteralPath $Root).Path
    $allow = @()
    foreach ($pattern in $AllowGlob) { $allow += [regex]$pattern }

    $denyRules = @()
    foreach ($rule in $Deny) { $denyRules += @{ rx = [regex]$rule.p; why = $rule.why } }
    foreach ($pattern in $ExtraDeny) { $denyRules += @{ rx = [regex]$pattern; why = "extra-deny" } }
    $secretRules = @()
    foreach ($rule in $Secret) { $secretRules += @{ rx = [regex]$rule.p; why = $rule.why } }
    $reviewRules = @()
    foreach ($rule in $Review) { $reviewRules += @{ rx = [regex]$rule.p; why = $rule.why } }

    $blocks = @()
    $warns = @()
    $scanned = 0

    $items = Get-ChildItem -LiteralPath $rootPath -Recurse -File -Force -ErrorAction SilentlyContinue
    foreach ($item in $items) {
        $relative = $item.FullName.Substring($rootPath.Length).TrimStart([char]92, [char]47) -replace '\\', '/'

        $skip = $false
        foreach ($part in ($relative -split "/")) {
            if ($SkipDirs -contains $part) { $skip = $true; break }
        }
        if ($skip) { continue }
        if ($SkipSuffix -contains $item.Extension.ToLower()) { continue }
        $skipByAllow = $false
        foreach ($rx in $allow) { if ($rx.IsMatch($relative)) { $skipByAllow = $true; break } }
        if ($skipByAllow) { continue }

        $scanned++
        try {
            $text = [System.IO.File]::ReadAllText($item.FullName, [System.Text.Encoding]::UTF8)
        } catch { continue }

        $lines = $text -split "`r?`n"
        for ($i = 0; $i -lt $lines.Count; $i++) {
            $line = $lines[$i]
            $number = $i + 1
            $trimmed = $line.Trim()
            if ($trimmed.Length -gt 100) { $trimmed = $trimmed.Substring(0, 100) }

            foreach ($rule in $denyRules) {
                if ($rule.rx.IsMatch($line)) {
                    $blocks += "${relative}:${number}: [check-sanitization:denylisted-string] (" + $rule.why + ") " + $trimmed
                }
            }
            foreach ($rule in $secretRules) {
                if ($rule.rx.IsMatch($line)) {
                    $blocks += "${relative}:${number}: [check-sanitization:hardcoded-secret] (" + $rule.why + ") (redacted)"
                }
            }
            foreach ($rule in $reviewRules) {
                if ($rule.rx.IsMatch($line)) {
                    $entry = "${relative}:${number}: [check-sanitization:review-term] (" + $rule.why + ") " + $trimmed
                    if ($StrictReview) { $blocks += $entry } else { $warns += $entry }
                }
            }
        }
    }

    Write-Output ("Sanitization scan: " + $scanned + " files under " + $rootPath)
    foreach ($warning in $warns) { Write-Output ("  WARN  " + $warning) }
    if ($blocks.Count -gt 0) {
        Write-Output ("  result: BLOCKED (" + $blocks.Count + " finding(s))")
        foreach ($block in $blocks) { [Console]::Error.WriteLine("  FAIL  " + $block) }
        exit 2
    }
    Write-Output ("  result: CLEAN (" + $warns.Count + " warning(s))")
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
