param(
    [switch]$SkipDocker
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Sample = Join-Path $Root "samples/react-aspnetcore-taskflow"
$Frontend = Join-Path $Sample "frontend"
$Backend = Join-Path $Sample "backend"
$Evidence = Join-Path $Sample "docs/evidence/generated"
$Collector = Join-Path $Root "tools/collect-validation-evidence/collect.py"

New-Item -ItemType Directory -Force -Path $Evidence | Out-Null

function Invoke-Evidence {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Name,

        [Parameter(Mandatory = $true)]
        [string]$WorkingDirectory,

        [Parameter(Mandatory = $true)]
        [string[]]$Command
    )

    Write-Host ""
    Write-Host "=== $Name ===" -ForegroundColor Cyan

    python $Collector `
        --name $Name `
        --cwd $WorkingDirectory `
        --output (Join-Path $Evidence "$Name.md") `
        -- @Command

    if ($LASTEXITCODE -ne 0) {
        throw "Validation failed: $Name"
    }
}

Invoke-Evidence "agent-config-validation" $Root @(
    "python",
    "tools/check-agent-config/check_agent_config.py",
    "--root",
    "."
)

Invoke-Evidence "python-tools-compile" $Root @(
    "python",
    "-m",
    "compileall",
    "-q",
    "tools"
)

Invoke-Evidence "stack-readiness-self-test" $Root @(
    "python",
    "tools/check-stack-readiness/self_test.py"
)

Invoke-Evidence "react-stack-readiness" $Root @(
    "python",
    "tools/check-stack-readiness/check_stack_readiness.py",
    "--stack",
    "stacks/react-aspnetcore"
)

Invoke-Evidence "state-model-self-test" $Root @(
    "python",
    "tools/check-state-model/self_test.py"
)

Invoke-Evidence "sample-state-model" $Root @(
    "python",
    "tools/check-state-model/check_state_model.py",
    "--project-docs",
    "samples/react-aspnetcore-taskflow/docs"
)

Invoke-Evidence "build-log-self-test" $Root @(
    "python",
    "tools/check-build-log/self_test.py"
)


Invoke-Evidence "reference-image-self-test" $Root @(
    "python",
    "tools/reference-image-manifest/self_test.py"
)

Invoke-Evidence "spa-screen-extractor-self-test" $Root @(
    "python",
    "tools/spa-screen-extractor/self_test.py"
)

Invoke-Evidence "frontend-install" $Frontend @("npm", "ci")
Invoke-Evidence "frontend-color-static" $Frontend @("npm", "run", "color:static")
Invoke-Evidence "frontend-lint" $Frontend @("npm", "run", "lint")
Invoke-Evidence "frontend-test" $Frontend @("npm", "run", "test")
Invoke-Evidence "frontend-build" $Frontend @("npm", "run", "build")

Invoke-Evidence "backend-restore" $Backend @(
    "dotnet",
    "restore",
    "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj"
)
Invoke-Evidence "backend-build" $Backend @(
    "dotnet",
    "build",
    "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj",
    "--no-restore"
)
Invoke-Evidence "backend-test" $Backend @(
    "dotnet",
    "test",
    "TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj",
    "--no-build"
)

Invoke-Evidence "frontend-e2e" $Frontend @("npm", "run", "e2e")
Invoke-Evidence "frontend-color-runtime" $Frontend @("npm", "run", "e2e:color")

if (-not $SkipDocker) {
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
        throw "Docker was not found. Install Docker or rerun with -SkipDocker and record Docker as PENDING."
    }

    Invoke-Evidence "docker-build" $Sample @("docker", "compose", "build")
}

Write-Host ""
Write-Host "All selected pre-commit validation gates passed." -ForegroundColor Green
