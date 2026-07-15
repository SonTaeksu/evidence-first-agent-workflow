# Codex MCP configuration

## Binding rules

Codex reads the project-root `AGENTS.md` by convention — that is the binding ruleset: honesty over completion, the five-stage `prompts/GATE.md`, and a commit-time gate that blocks source changes lacking a worklog/state sync (`docs/core/enforcement-matrix.md`). The MCP setup below is separate.


Codex can use project-scoped `.codex/config.toml` for trusted projects.

Configured servers:

- `microsoft_learn`: official Microsoft Learn documentation through Streamable HTTP
- `context7`: current React and JavaScript-library documentation through a local STDIO process

After opening the project in Codex:

1. Trust the project.
2. Restart Codex after MCP configuration changes.
3. Run `/mcp` or `codex mcp list`.
4. Confirm both servers are connected.

Context7 can run without an API key with lower limits. Add an API key in your user-level configuration when higher limits are needed. Do not commit API keys.
