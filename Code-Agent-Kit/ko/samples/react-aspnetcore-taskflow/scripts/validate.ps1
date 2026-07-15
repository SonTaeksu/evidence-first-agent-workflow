$ErrorActionPreference = "Stop"

$SampleRoot = Split-Path -Parent $PSScriptRoot
$RepoRoot = Resolve-Path (Join-Path $SampleRoot "../..")
$Collector = Join-Path $RepoRoot "tools/collect-validation-evidence/collect.py"
$Evidence = Join-Path $SampleRoot "docs/evidence/generated"

New-Item -ItemType Directory -Force -Path $Evidence | Out-Null

function Invoke-Evidence {
    param(
        [string]$Name,
        [string]$WorkingDirectory,
        [string[]]$Command
    )

    python $Collector `
        --name $Name `
        --cwd $WorkingDirectory `
        --output (Join-Path $Evidence "$Name.md") `
        -- @Command

    if ($LASTEXITCODE -ne 0) {
        throw "Validation failed: $Name"
    }
}

$Frontend = Join-Path $SampleRoot "frontend"
$Backend = Join-Path $SampleRoot "backend"

Invoke-Evidence "frontend-install" $Frontend @("npm", "install")
Invoke-Evidence "stack-readiness" $RepoRoot @(
    "python",
    "tools/check-stack-readiness/check_stack_readiness.py",
    "--stack",
    "stacks/react-aspnetcore"
)
Invoke-Evidence "state-model" $RepoRoot @(
    "python",
    "tools/check-state-model/check_state_model.py",
    "--project-docs",
    "samples/react-aspnetcore-taskflow/docs"
)
Invoke-Evidence "frontend-color-static" $Frontend @("npm", "run", "color:static")
Invoke-Evidence "frontend-lint" $Frontend @("npm", "run", "lint")
Invoke-Evidence "frontend-test" $Frontend @("npm", "run", "test")
Invoke-Evidence "frontend-build" $Frontend @("npm", "run", "build")

Invoke-Evidence "backend-restore" $Backend @(
    "dotnet", "restore", "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj"
)
Invoke-Evidence "backend-build" $Backend @(
    "dotnet", "build", "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj",
    "--no-restore"
)
Invoke-Evidence "backend-test" $Backend @(
    "dotnet", "test", "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj",
    "--no-build"
)

Invoke-Evidence "e2e" $Frontend @("npm", "run", "e2e")
Invoke-Evidence "frontend-color-runtime" $Frontend @("npm", "run", "e2e:color")

Write-Host "All validation gates passed."
