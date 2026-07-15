param(
    [Parameter(Mandatory=$true)][string]$Target,
    [ValidateSet("full","core")][string]$Mode="full",
    [string]$Stack="_template",
    [switch]$Overwrite
)
$ArgsList = @("$PSScriptRoot/install-kit.py", "--target", $Target, "--mode", $Mode, "--stack", $Stack)
if ($Overwrite) { $ArgsList += "--overwrite" }
python @ArgsList
exit $LASTEXITCODE
