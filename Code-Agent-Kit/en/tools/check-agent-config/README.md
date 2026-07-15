# check-agent-config

Validates the checked-in instruction and MCP configuration for:

- Codex
- Roo Code
- Zoo Code
- Cline
- Claude Code

It checks required files, JSON/TOML syntax, server names, transport spelling, and that public-alpha MCP tools are not auto-approved.

```bash
python tools/check-agent-config/check_agent_config.py --root .
```
