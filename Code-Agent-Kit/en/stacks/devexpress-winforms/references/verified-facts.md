# Verified Facts — DevExpress WinForms

This file holds facts confirmed against a named source on a named date. Nothing
about *this project* is here yet, because this stack has not been used against a
real project in this repository — that is correct, not an omission.

What is here is the documentation-source layer, because it is version-sensitive
and because the whole stack routes through it.

| Fact | Scope | Verified against | Date |
|---|---|---|---|
| The DevExpress documentation MCP endpoint is `https://api.devexpress.com/mcp/docs` and requires no authentication | the endpoint | official DevExpress documentation | 2026-06-16 |
| Transport is Streamable HTTP only; a browser GET returns `405 Method Not Allowed`, and the documentation states that this is expected rather than a fault | the endpoint | official DevExpress documentation | 2026-06-16 |
| Version pinning uses the `?v=` query parameter and is supported no earlier than v24.2; `?v=24.2` is the documented example | v24.2 and later | official DevExpress documentation | 2026-06-16 |
| The server exposes exactly two tools: `devexpress_docs_search` (semantic search, returns the top five matches) and `devexpress_docs_get_content` (downloads a complete help topic by URL) | the endpoint | official DevExpress documentation | 2026-06-16 |
| A predefined prompt exists: `mcp.dxdocs.devexpress_docs_query_workflow` | the endpoint | official DevExpress documentation | 2026-06-16 |
| The documented server names are `dxdocs` for the latest release and `dxdocs24_2` for the pinned one | the endpoint | official DevExpress documentation | 2026-06-16 |
| `https://learn.microsoft.com/api/mcp` connects without credentials and exposes 3 tools | the endpoint | MCP Inspector run, `docs/core/mcp-source-verification.md` | 2026-08-05 |
| `https://api.devexpress.com/mcp/docs` connects without credentials and its `tools/list` returns exactly the two documented tools | the endpoint | MCP Inspector `tools/list`, `--transport http`, owner's machine | 2026-08-06 |
| `devexpress_docs_search` takes `technologies` (array, `minItems: 1`, closed enum, **required**) and `question` (string, **required**) | the endpoint | the same `tools/list` output | 2026-08-06 |
| The `technologies` enum is closed and its members are `Angular`, `AspNet`, `AspNetBootstrap`, `AspNetCore`, `AspNetMvc`, `ASPxThemeBuilder`, `ASPxThemeDeployer`, `Blazor`, `CodedUIExtension`, `CoreLibraries`, `Dashboard`, `DesignSystem`, `DevExtremeAspNetMvc`, `eud`, `eXpressAppFramework`, `GeneralInformation`, `jQuery`, `MAUI`, `OfficeFileAPI`, `OfficeFileApiJava`, `React`, `ReportServer`, `SkinEditor`, `VCL`, `Vue`, `WindowsForms`, `WPF`, `WpfThemeDesigner`, `XPO`, `XpoProfiler`, `XtraReports` — this stack's value is `WindowsForms` | the endpoint | the same `tools/list` output | 2026-08-06 |
| `devexpress_docs_get_content` takes `url` (string, **required**), and its own description forbids constructing the URL from general knowledge — it must come from a `devexpress_docs_search` result | the endpoint | the same `tools/list` output | 2026-08-06 |
| The server's own tool descriptions require `devexpress_docs_search` before any `devexpress_docs_get_content`, because search returns snippets only | the endpoint | the same `tools/list` output | 2026-08-06 |

**The grade of the 2026-08-06 run, precisely.** It connected and listed tools. It
did **not** run a `tools/call`. The fourteen servers in
`docs/core/mcp-source-verification.md` are `PASS` because each answered a real
call; this endpoint has not been taken that far and is not recorded as `PASS`.
`https://api.devexpress.com/mcp/docs?v=24.2` was not exercised at all.

## Recorded as unverified

| Claim | Why it is not in the table above |
|---|---|
| That `api.devexpress.com/mcp/docs` answers a real `tools/call` | `⟨verification required: MCP Inspector tools/call against devexpress_docs_search, arguments built from the schema above — the 2026-08-06 run stopped at tools/list⟩` |
| That the pinned `api.devexpress.com/mcp/docs?v=24.2` answers anything | `⟨verification required: MCP Inspector tools/list against the pinned URL — the 2026-08-06 run used the unpinned URL only, and the unpinned one answering is not evidence for the pinned one⟩` |

## Rules

- A row needs a source. Without one it is a memory, and memories go in nobody's
  reference file.
- A version-sensitive fact names the version it was verified for.
- `references/pitfalls.md` holds properties of the technology; this file holds
  facts confirmed against a source. They are not the same and are not merged.
- Documentation is a weaker class of evidence than a call that returned. A row
  sourced to documentation stays sourced to documentation when somebody later runs
  the call — the run adds a row, it does not upgrade this one.
