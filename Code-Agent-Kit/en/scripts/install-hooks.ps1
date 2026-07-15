# Wire the Evidence-First commit-layer gate into this repository (Windows).
$ErrorActionPreference = "Stop"
$root = (git rev-parse --show-toplevel).Trim()
New-Item -ItemType Directory -Force -Path "$root/.githooks" | Out-Null
Copy-Item "$root/tools/enforce-agent-gates/pre-commit" "$root/.githooks/pre-commit" -Force
git -C $root config core.hooksPath .githooks
Write-Host "Installed: core.hooksPath=.githooks (pre-commit gate active)."
Write-Host "Bypass a single commit only with an explicit: git commit --no-verify"
