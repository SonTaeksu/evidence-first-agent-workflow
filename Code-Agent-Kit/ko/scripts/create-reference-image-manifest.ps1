param(
    [Parameter(Mandatory = $true)]
    [string]$Image,

    [string]$Regions,

    [string]$OutputRoot = "reference-assets/evidence"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$ImagePath = (Resolve-Path -LiteralPath $Image).Path
$Name = [System.IO.Path]::GetFileNameWithoutExtension($ImagePath)
$OutputDirectory = Join-Path (Join-Path $Root $OutputRoot) $Name

# [System.IO.Directory]::CreateDirectory, not New-Item: New-Item has no
# -LiteralPath parameter at all, so the form this line used to have threw
# "A parameter cannot be found that matches parameter name 'LiteralPath'".
# The .NET call is literal by definition and creates intermediate directories.
[void][System.IO.Directory]::CreateDirectory($OutputDirectory)

$Arguments = @(
    (Join-Path $Root "tools/reference-image-manifest/extract_reference_image.py"),
    $ImagePath,
    "--output",
    (Join-Path $OutputDirectory "manifest.json"),
    "--normalized-png",
    (Join-Path $OutputDirectory "normalized.png")
)

if ($Regions) {
    $Arguments += @("--regions", (Resolve-Path -LiteralPath $Regions).Path)
}

python @Arguments
if ($LASTEXITCODE -ne 0) {
    throw "Reference image manifest generation failed."
}

Write-Host "Reference evidence: $OutputDirectory" -ForegroundColor Green
