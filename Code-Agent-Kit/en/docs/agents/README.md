# Coding-agent setup

| Tool | Project instructions | Project MCP |
|---|---|---|
| Codex | `AGENTS.md` | `.codex/config.toml` |
| Roo Code | `AGENTS.md`, `.roo/rules/` | `.roo/mcp.json` |
| Zoo Code | `AGENTS.md`, `.roo/rules/` | `.roo/mcp.json` |
| Cline | `AGENTS.md`, `.clinerules/` | import `agent-configs/cline/mcp.example.json` |
| Claude Code | `CLAUDE.md`, `AGENTS.md` | `.mcp.json` |

All tools must use the same state and validation rules. Tool-specific files only adapt discovery and MCP configuration.
