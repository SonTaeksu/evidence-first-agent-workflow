#!/usr/bin/env bash
set -euo pipefail

SAMPLE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPO_ROOT="$(cd "$SAMPLE_ROOT/../.." && pwd)"
COLLECTOR="$REPO_ROOT/tools/collect-validation-evidence/collect.py"
EVIDENCE="$SAMPLE_ROOT/docs/evidence/generated"

mkdir -p "$EVIDENCE"

run_evidence() {
  local name="$1"
  local cwd="$2"
  shift 2

  python3 "$COLLECTOR" \
    --name "$name" \
    --cwd "$cwd" \
    --output "$EVIDENCE/$name.md" \
    -- "$@"
}

run_evidence stack-readiness "$REPO_ROOT" \
  python3 tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
run_evidence state-model "$REPO_ROOT" \
  python3 tools/check-state-model/check_state_model.py \
  --project-docs samples/react-aspnetcore-taskflow/docs

run_evidence frontend-install "$SAMPLE_ROOT/frontend" npm install
run_evidence frontend-color-static "$SAMPLE_ROOT/frontend" npm run color:static
run_evidence frontend-lint "$SAMPLE_ROOT/frontend" npm run lint
run_evidence frontend-test "$SAMPLE_ROOT/frontend" npm run test
run_evidence frontend-build "$SAMPLE_ROOT/frontend" npm run build

run_evidence backend-restore "$SAMPLE_ROOT/backend" \
  dotnet restore TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj
run_evidence backend-build "$SAMPLE_ROOT/backend" \
  dotnet build TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj --no-restore
run_evidence backend-test "$SAMPLE_ROOT/backend" \
  dotnet test TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj --no-build

run_evidence e2e "$SAMPLE_ROOT/frontend" npm run e2e
run_evidence frontend-color-runtime "$SAMPLE_ROOT/frontend" npm run e2e:color

echo "All validation gates passed."
