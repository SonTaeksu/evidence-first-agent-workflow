#!/usr/bin/env bash
# Wire the Evidence-First commit-layer gate into this repository.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel)"
mkdir -p "$ROOT/.githooks"
cp "$ROOT/tools/enforce-agent-gates/pre-commit" "$ROOT/.githooks/pre-commit"
chmod +x "$ROOT/.githooks/pre-commit"
git -C "$ROOT" config core.hooksPath .githooks
echo "Installed: core.hooksPath=.githooks (pre-commit gate active)."
echo "Bypass a single commit only with an explicit: git commit --no-verify"
