# SPDX-License-Identifier: MPL-2.0
"""Validate project instruction and MCP configuration files for supported agents."""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from pathlib import Path
from typing import Any


REQUIRED_SERVERS = {"microsoft-learn", "context7"}


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def check_servers(
    label: str,
    servers: dict[str, Any],
    errors: list[str],
) -> None:
    missing = REQUIRED_SERVERS - set(servers)
    if missing:
        errors.append(f"{label}: missing MCP servers: {sorted(missing)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    root = args.root.resolve()

    errors: list[str] = []
    checks: list[str] = []

    required_files = [
        "AGENTS.md",
        "CLAUDE.md",
        ".mcp.json",
        ".codex/config.toml",
        ".roo/mcp.json",
        ".roo/rules/10-evidence-first.md",
        ".clinerules/10-evidence-first.md",
        "agent-configs/cline/mcp.example.json",
        ".agentignore",
        "prompts/GATE.md",
        "prompts/0-sync-and-orient.md",
        "templates/core/worklog.md",
        "tools/spa-screen-extractor/README.md",
        "DESIGN-CONCEPTS.md",
        "docs/core/state-and-memory-model.md",
        "docs/getting-started/stack-input-requirements.md",
        "tools/check-stack-readiness/check_stack_readiness.py",
        "tools/check-state-model/check_state_model.py",
    ]

    for relative in required_files:
        path = root / relative
        if path.exists() and path.stat().st_size > 0:
            checks.append(f"PASS file: {relative}")
        else:
            errors.append(f"Missing or empty: {relative}")

    root_agents = (root / "AGENTS.md").read_text(encoding="utf-8")
    if len(root_agents.splitlines()) > 90:
        errors.append(
            "AGENTS.md is too long for an always-loaded rule file "
            f"({len(root_agents.splitlines())} lines > 90)."
        )
    worklog_current_markers = [
        "A worklog is a checkpoint. It never replaces current state.",
        "Worklog는 Checkpoint이며 Current State를 대체하지 않습니다.",
        "Worklog는 Current를 대체하지 않습니다.",
    ]
    if not any(marker in root_agents for marker in worklog_current_markers):
        errors.append(
            "AGENTS.md must declare that worklog does not replace current."
        )

    adapters = [
        "CLAUDE.md",
        ".roo/rules/10-evidence-first.md",
        ".clinerules/10-evidence-first.md",
    ]
    for relative in adapters:
        adapter_text = (root / relative).read_text(encoding="utf-8")
        if "AGENTS.md" not in adapter_text:
            errors.append(f"{relative}: must point to AGENTS.md.")
        if len(adapter_text.splitlines()) > 40:
            errors.append(
                f"{relative}: adapter is too long and may duplicate rules."
            )

    try:
        claude = load_json(root / ".mcp.json")
        check_servers(
            "Claude Code .mcp.json",
            claude.get("mcpServers", {}),
            errors,
        )
        microsoft = claude["mcpServers"]["microsoft-learn"]
        if microsoft.get("type") not in {"http", "streamable-http"}:
            errors.append("Claude Code: Microsoft Learn must use HTTP.")
        checks.append("PASS JSON: .mcp.json")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        errors.append(f"Claude Code .mcp.json: {error}")

    try:
        roo = load_json(root / ".roo/mcp.json")
        check_servers("Roo/Zoo .roo/mcp.json", roo.get("mcpServers", {}), errors)
        if (
            roo["mcpServers"]["microsoft-learn"].get("type")
            != "streamable-http"
        ):
            errors.append(
                "Roo/Zoo: Microsoft Learn type must be streamable-http."
            )
        for name, entry in roo.get("mcpServers", {}).items():
            if entry.get("alwaysAllow"):
                errors.append(
                    f"Roo/Zoo: public alpha must not auto-approve {name} tools."
                )
        checks.append("PASS JSON: .roo/mcp.json")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        errors.append(f"Roo/Zoo .roo/mcp.json: {error}")

    try:
        cline = load_json(root / "agent-configs/cline/mcp.example.json")
        check_servers("Cline MCP example", cline.get("mcpServers", {}), errors)
        if (
            cline["mcpServers"]["microsoft-learn"].get("type")
            != "streamableHttp"
        ):
            errors.append(
                "Cline: Microsoft Learn type must be streamableHttp."
            )
        for name, entry in cline.get("mcpServers", {}).items():
            if entry.get("autoApprove"):
                errors.append(
                    f"Cline: public alpha must not auto-approve {name} tools."
                )
        checks.append("PASS JSON: Cline MCP example")
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        errors.append(f"Cline MCP example: {error}")

    try:
        codex = tomllib.loads(
            (root / ".codex/config.toml").read_text(encoding="utf-8")
        )
        servers = codex.get("mcp_servers", {})
        codex_required = {"microsoft_learn", "context7"}
        missing = codex_required - set(servers)
        if missing:
            errors.append(
                f"Codex .codex/config.toml: missing MCP servers: {sorted(missing)}"
            )
        checks.append("PASS TOML: .codex/config.toml")
    except (OSError, TypeError, tomllib.TOMLDecodeError) as error:
        errors.append(f"Codex config: {error}")

    for line in checks:
        print(line)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 2

    print("All supported coding-agent configuration checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
