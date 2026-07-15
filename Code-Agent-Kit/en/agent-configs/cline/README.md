# Cline setup

Cline automatically loads:

- root `AGENTS.md`;
- workspace rules under `.clinerules/`;
- `.clineignore`.

Cline IDE MCP settings are managed from the MCP Servers configuration UI rather than a portable repository-level file. Import or copy the entries from `mcp.example.json`.

For Cline CLI, the user-level MCP file is `~/.cline/mcp.json`.

After setup, confirm:

- Microsoft Learn MCP is connected;
- Context7 MCP is connected;
- no tools are auto-approved during initial evaluation;
- `npm run e2e:color` is used for UI color changes.
