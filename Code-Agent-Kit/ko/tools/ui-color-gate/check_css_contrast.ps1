# SPDX-License-Identifier: MPL-2.0
<#
  check_css_contrast.ps1 — PowerShell twin of check_css_contrast.py.

  Deterministically checks configured CSS foreground/background contrast pairs.

  A machine without Python has this as its only gate, so both must agree on the
  exit code and the finding identifiers. Verified by tools/check-script-parity.

  The WCAG relative-luminance arithmetic is IEEE-754 double on both sides, so the
  two agree bit-for-bit on the same input. The harness pins a pair that lands
  exactly on its minimum (#000 on #fff is exactly 21:1) because a boundary is
  where two implementations of the same formula would first diverge.

  Windows PowerShell 5.1 compatible: no &&, no ??, no ternary, no -Parallel.

  Exit codes:
    0  every configured pair meets its minimum
    2  at least one pair is below its minimum
    1  tool error -- including a colour this tool refuses to guess at
#>
param(
    [Parameter(Mandatory = $true)][string]$Css,
    [Parameter(Mandatory = $true)][string]$Config,
    [string]$Output
)

$ErrorActionPreference = "Stop"

# fullmatch() on the Python side. \z rather than $, because .NET's $ also matches
# before a trailing newline and would accept "#fff`n" as a colour.
$HexColor = [regex]'^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})\z'

# ---------------------------------------------------------------------------
function Remove-CssComments {
    param([string]$Css)
    return [regex]::Replace($Css, "/\*.*?\*/", "",
        [System.Text.RegularExpressions.RegexOptions]::Singleline)
}

function Find-MatchingBrace {
    param([string]$Text, [int]$Opening)
    $depth = 0
    for ($index = $Opening; $index -lt $Text.Length; $index++) {
        if ($Text[$index] -eq [char]123) { $depth++ }
        elseif ($Text[$index] -eq [char]125) {
            $depth--
            if ($depth -eq 0) { return $index }
        }
    }
    throw "[ui-color-gate:unmatched-brace] Unmatched CSS brace."
}

function Get-Declarations {
    param([string]$Body)
    $declarations = @{}
    foreach ($raw in ($Body -split ";")) {
        if (-not $raw.Contains(":")) { continue }
        $index = $raw.IndexOf(":")
        $name = $raw.Substring(0, $index).Trim().ToLower()
        $value = $raw.Substring($index + 1).Trim()
        if ($name -and $value) { $declarations[$name] = $value }
    }
    return $declarations
}

function Get-CssRules {
    param([string]$Css)
    $rules = @{}

    # An explicit stack rather than recursion: at-rule nesting is the only reason
    # the Python side recurses, and a stack keeps the two shapes comparable.
    $pending = New-Object System.Collections.Stack
    $pending.Push((Remove-CssComments $Css))

    while ($pending.Count -gt 0) {
        $segment = $pending.Pop()
        $cursor = 0
        while ($true) {
            $opening = $segment.IndexOf([char]123, $cursor)
            if ($opening -lt 0) { break }

            $prelude = $segment.Substring($cursor, $opening - $cursor).Trim()
            $closing = Find-MatchingBrace $segment $opening
            $body = $segment.Substring($opening + 1, $closing - $opening - 1)

            if ($prelude.StartsWith("@")) {
                $pending.Push($body)
            } elseif ($prelude) {
                $declarations = Get-Declarations $body
                foreach ($selector in ($prelude -split ",")) {
                    $normalized = $selector.Trim()
                    if (-not $normalized) { continue }
                    if (-not $rules.ContainsKey($normalized)) { $rules[$normalized] = @{} }
                    foreach ($key in $declarations.Keys) { $rules[$normalized][$key] = $declarations[$key] }
                }
            }

            $cursor = $closing + 1
        }
    }
    return $rules
}

function Get-NormalizedHex {
    param([string]$Value)
    $value = $Value.Trim()
    if (-not $HexColor.IsMatch($value)) {
        throw ("[ui-color-gate:unsupported-color] Only literal hex colors are supported, got: " + $value)
    }
    $digits = $value.Substring(1)
    if ($digits.Length -eq 3) {
        $expanded = ""
        foreach ($char in $digits.ToCharArray()) { $expanded += ([string]$char + [string]$char) }
        $digits = $expanded
    }
    return "#" + $digits.ToLower()
}

function Get-Channel {
    param([int]$Value)
    $normalized = $Value / 255.0
    if ($normalized -le 0.04045) { return $normalized / 12.92 }
    return [Math]::Pow(($normalized + 0.055) / 1.055, 2.4)
}

function Get-Luminance {
    param([string]$Color)
    $color = Get-NormalizedHex $Color
    $red = [Convert]::ToInt32($color.Substring(1, 2), 16)
    $green = [Convert]::ToInt32($color.Substring(3, 2), 16)
    $blue = [Convert]::ToInt32($color.Substring(5, 2), 16)
    return (0.2126 * (Get-Channel $red)) + (0.7152 * (Get-Channel $green)) + (0.0722 * (Get-Channel $blue))
}

function Get-ContrastRatio {
    param([string]$Foreground, [string]$Background)
    $first = Get-Luminance $Foreground
    $second = Get-Luminance $Background
    $lighter = [Math]::Max($first, $second)
    $darker = [Math]::Min($first, $second)
    return ($lighter + 0.05) / ($darker + 0.05)
}

function Get-RequiredProperty {
    # A missing key is a KeyError on the Python side, which is a tool error.
    param([object]$Object, [string]$Name)
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) { throw ("missing required key: '" + $Name + "'") }
    return $property.Value
}

function Resolve-ColorValue {
    param([object]$Reference, [hashtable]$Rules)
    $literal = $null
    $valueProperty = $Reference.PSObject.Properties["value"]
    if ($null -ne $valueProperty) { $literal = $valueProperty.Value }
    # Python treats an empty string and 0 as absent here; `if ($literal)` in
    # PowerShell is the same falsiness.
    if ($literal) { return Get-NormalizedHex ([string]$literal) }

    $selector = [string](Get-RequiredProperty $Reference "selector")
    $propertyName = ([string](Get-RequiredProperty $Reference "property")).ToLower()

    if (-not $Rules.ContainsKey($selector)) {
        throw ("[ui-color-gate:selector-not-found] Selector not found: " + $selector)
    }
    if (-not $Rules[$selector].ContainsKey($propertyName)) {
        throw ("[ui-color-gate:property-not-found] Property '" + $propertyName +
               "' not found for selector '" + $selector + "'.")
    }
    return Get-NormalizedHex $Rules[$selector][$propertyName]
}

# ---------------------------------------------------------------------------
try {
    $cssText = [System.IO.File]::ReadAllText($Css) -replace "`r`n", "`n"
    $rules = Get-CssRules $cssText
    # NOT $config. PowerShell variable names are case-insensitive, so a local
    # `$config` *is* the `[string]$Config` parameter, and assigning the parsed
    # object to it coerces it to the string "@{checks=System.Object[]}". Every
    # property lookup then finds nothing and this reported a missing 'checks' key
    # on a perfectly good config. Same defect as the `$manifest` one recorded in
    # docs/worklogs/powershell-twins.worklog.md; it is easy to make twice.
    $configData = [System.IO.File]::ReadAllText($Config) -replace "`r`n", "`n" | ConvertFrom-Json

    $checks = Get-RequiredProperty $configData "checks"

    $results = @()
    $failureCount = 0

    foreach ($check in $checks) {
        $foreground = Resolve-ColorValue (Get-RequiredProperty $check "foreground") $rules
        $background = Resolve-ColorValue (Get-RequiredProperty $check "background") $rules
        $minimum = 4.5
        $minimumProperty = $check.PSObject.Properties["minimum"]
        if ($null -ne $minimumProperty -and $null -ne $minimumProperty.Value) {
            $minimum = [double]$minimumProperty.Value
        }
        $ratio = Get-ContrastRatio $foreground $background
        if ($ratio -ge $minimum) { $status = "PASS" } else { $status = "FAIL"; $failureCount++ }

        $results += [ordered]@{
            name = [string](Get-RequiredProperty $check "name")
            foreground = $foreground
            background = $background
            ratio = [Math]::Round($ratio, 3)
            minimum = $minimum
            status = $status
        }
    }

    if ($Output) {
        if ($failureCount -gt 0) { $overall = "FAIL" } else { $overall = "PASS" }
        $payload = [ordered]@{
            css = ($Css -replace '\\', '/')
            config = ($Config -replace '\\', '/')
            checks = $results
            status = $overall
        }
        $directory = [System.IO.Path]::GetDirectoryName(
            [System.IO.Path]::GetFullPath([System.IO.Path]::Combine((Get-Location).Path, $Output)))
        if ($directory -and -not (Test-Path -LiteralPath $directory)) {
            # [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
            # -LiteralPath parameter at all (only -Path, which expands wildcards), so a
            # path containing [ ] * ? cannot be created safely through it. The .NET call
            # is literal by definition and creates intermediate directories.
            [void][System.IO.Directory]::CreateDirectory($directory)
        }
        [System.IO.File]::WriteAllText($Output,
            (ConvertTo-Json $payload -Depth 6) + "`n")
    }

    foreach ($result in $results) {
        # The identifier is printed only on the failing line. A passing pair is
        # not a finding, and tagging it would make the identifier unusable for
        # mechanical extraction.
        $tag = ""
        if ($result.status -eq "FAIL") { $tag = "[ui-color-gate:contrast-below-minimum] " }
        Write-Output ("{0,-4} {1,5:F2}:1 >= {2,4:F1}:1 {3}{4} ({5} on {6})" -f
            $result.status, $result.ratio, $result.minimum, $tag,
            $result.name, $result.foreground, $result.background)
    }

    if ($failureCount -gt 0) { exit 2 }
    exit 0
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    exit 1
}
