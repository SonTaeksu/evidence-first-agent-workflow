#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SAMPLE="$ROOT/samples/react-aspnetcore-taskflow"
FRONTEND="$SAMPLE/frontend"
BACKEND="$SAMPLE/backend"
EVIDENCE="$SAMPLE/docs/evidence/generated"
COLLECTOR="$ROOT/tools/collect-validation-evidence/collect.py"

mkdir -p "$EVIDENCE"

run_evidence() {
  local name="$1"
  local cwd="$2"
  shift 2

  echo
  echo "=== $name ==="

  python3 "$COLLECTOR" \
    --name "$name" \
    --cwd "$cwd" \
    --output "$EVIDENCE/$name.md" \
    -- "$@"
}

run_evidence agent-config-validation "$ROOT" \
  python3 tools/check-agent-config/check_agent_config.py --root .

run_evidence python-tools-compile "$ROOT" \
  python3 -m compileall -q tools

run_evidence stack-readiness-self-test "$ROOT" \
  python3 tools/check-stack-readiness/self_test.py

run_evidence react-stack-readiness "$ROOT" \
  python3 tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore

run_evidence state-model-self-test "$ROOT" \
  python3 tools/check-state-model/self_test.py

run_evidence sample-state-model "$ROOT" \
  python3 tools/check-state-model/check_state_model.py \
  --project-docs samples/react-aspnetcore-taskflow/docs

run_evidence build-log-self-test "$ROOT" \
  python3 tools/check-build-log/self_test.py

run_evidence reference-image-self-test "$ROOT" \
  python3 tools/reference-image-manifest/self_test.py

run_evidence spa-screen-extractor-self-test "$ROOT" \
  python3 tools/spa-screen-extractor/self_test.py

run_evidence frontend-install "$FRONTEND" npm ci
run_evidence frontend-color-static "$FRONTEND" npm run color:static
run_evidence frontend-lint "$FRONTEND" npm run lint
run_evidence frontend-test "$FRONTEND" npm run test
run_evidence frontend-build "$FRONTEND" npm run build

run_evidence backend-restore "$BACKEND" \
  dotnet restore TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj
run_evidence backend-build "$BACKEND" \
  dotnet build TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj --no-restore
run_evidence backend-test "$BACKEND" \
  dotnet test TaskFlow.Api.Tests/TaskFlow.Api.Tests.csproj --no-build

run_evidence frontend-e2e "$FRONTEND" npm run e2e
run_evidence frontend-color-runtime "$FRONTEND" npm run e2e:color

if [[ "${SKIP_DOCKER:-0}" != "1" ]]; then
  if ! command -v docker >/dev/null 2>&1; then
    echo "Docker was not found." >&2
    echo "Install Docker or rerun with SKIP_DOCKER=1 and record Docker as PENDING." >&2
    exit 1
  fi

  run_evidence docker-build "$SAMPLE" docker compose build
fi

echo
echo "All selected pre-commit validation gates passed."
