param(
    [Parameter(Mandatory = $true)]
    [string]$Source,

    [string]$OutputRoot = "reference-assets/evidence",

    [int]$Wait = 2000,

    [string]$BrowserBin,

    [switch]$FromRenderedFile,

    [ValidateSet("en", "ko")]
    [string]$Language = "ko"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$SourcePath = Resolve-Path $Source
$Name = [System.IO.Path]::GetFileNameWithoutExtension($SourcePath)
$Output = Join-Path (Join-Path $Root $OutputRoot) $Name

New-Item -ItemType Directory -Force -Path $Output | Out-Null

$Arguments = @(
    (Join-Path $Root "tools/spa-screen-extractor/extract_spa.py"),
    "--wait",
    "$Wait",
    "--language",
    $Language,
    "--json",
    (Join-Path $Output "screen-spec.json"),
    "--out",
    (Join-Path $Output "screen-spec.md")
)

if ($FromRenderedFile) {
    $Arguments += @("--from-file", "$SourcePath")
}
else {
    $Arguments += @(
        "--browser",
        "$SourcePath",
        "--save-dom",
        (Join-Path $Output "rendered.html")
    )
}

if ($BrowserBin) {
    $Arguments += @("--browser-bin", $BrowserBin)
}

python @Arguments

if ($LASTEXITCODE -ne 0) {
    throw "SPA screen specification extraction failed."
}

Write-Host "SPA evidence: $Output" -ForegroundColor Green
