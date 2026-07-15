# MCP Setup

## Codex project configuration

The repository includes `.codex/config.toml`.

```toml
[mcp_servers.microsoft_learn]
url = "https://learn.microsoft.com/api/mcp"
enabled = true

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
enabled = true
```

Codex loads project-scoped configuration only for trusted projects.

Check:

```bash
codex mcp list
```

## Generic client example

See `mcp.json.example`.

## Optional Context7 API key

Context7 can run without a key with lower limits. Keep any API key in user-level configuration or environment variables. Do not commit it.
