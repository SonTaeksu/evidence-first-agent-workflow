param(
    [Parameter(Mandatory = $true)]
    [string]$Image,

    [string]$Regions,

    [string]$OutputRoot = "reference-assets/evidence"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$ImagePath = Resolve-Path $Image
$Name = [System.IO.Path]::GetFileNameWithoutExtension($ImagePath)
$OutputDirectory = Join-Path (Join-Path $Root $OutputRoot) $Name

New-Item -ItemType Directory -Force -Path $OutputDirectory | Out-Null

$Arguments = @(
    (Join-Path $Root "tools/reference-image-manifest/extract_reference_image.py"),
    $ImagePath,
    "--output",
    (Join-Path $OutputDirectory "manifest.json"),
    "--normalized-png",
    (Join-Path $OutputDirectory "normalized.png")
)

if ($Regions) {
    $Arguments += @("--regions", (Resolve-Path $Regions))
}

python @Arguments
if ($LASTEXITCODE -ne 0) {
    throw "Reference image manifest generation failed."
}

Write-Host "Reference evidence: $OutputDirectory" -ForegroundColor Green
