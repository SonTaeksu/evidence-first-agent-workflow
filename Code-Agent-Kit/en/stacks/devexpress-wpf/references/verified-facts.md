# Verified Facts — DevExpress WPF (v24.2+)

Empty, and that is correct: this stack has not been used against a real project
in this repository yet, so there is nothing that was verified rather than read.

| Fact | Verified against | Date |
|---|---|---|

## Rules

- A row needs a source. Without one it is a memory, and memories go in nobody's
  reference file.
- A version-sensitive fact names the version it was verified for. In this stack
  that means the DevExpress version, which is the axis these facts move along —
  the .NET target alone does not identify the behaviour.
- `references/pitfalls.md` holds properties of the technology; this file holds
  facts about *this project*. They are not the same and are not merged.
- Facts about the DevExpress documentation server itself belong in
  `../mcp/source-routing.md`, not here, and that file records exactly what the
  measurement covered and what it left open. In short: on **2026-08-06** an MCP
  Inspector
  `tools/list` against `https://api.devexpress.com/mcp/docs` succeeded without
  credentials and returned two tools with their full input schemas, which are
  transcribed there. The grade is **tools listed, not called** — no real
  `tools/call` was run, so it does **not** hold the `PASS` that the fourteen
  servers in `../../../docs/core/mcp-source-verification.md` earned by answering
  one, and `?v=24.2` was not separately exercised.
