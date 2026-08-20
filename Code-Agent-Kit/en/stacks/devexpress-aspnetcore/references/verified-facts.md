# Verified Facts — DevExpress for ASP.NET Core

Empty, and that is correct: this stack has not been used against a real project
in this repository yet, so there is nothing that was verified rather than read.

| Fact | Verified against | Date |
|---|---|---|

## One measured fact, which does not belong in the table above

The `dxdocs` endpoint itself was measured on **2026-08-06**: MCP Inspector, CLI,
`tools/list` over Streamable HTTP, no credentials. It connected and returned the
two documented tools with their input schemas, which are recorded in
`mcp/source-routing.md`. The grade is **`tools/list` measured, no `tools/call`
made** — weaker than the `PASS` carried by the servers in
`docs/core/mcp-source-verification.md`, which answered a real call. The pinned
`?v=24.2` endpoint was not exercised.

It is noted here rather than tabled because it is a fact about a shared source,
not about this project, and this table is for facts about this project.

## Rules

- A row needs a source. Without one it is a memory, and memories go in nobody's
  reference file.
- A version-sensitive fact names the version it was verified for. In this stack
  that means the DevExpress version, not only the .NET version — they move
  independently.
- A DevExpress fact names the help topic URL it came from, so a later reader can
  fetch the identical page rather than searching again and landing somewhere else.
- `references/pitfalls.md` holds properties of the technology; this file holds
  facts about *this project*. They are not the same and are not merged.
