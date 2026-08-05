# Source Routing — Go + HTMX

Every server below was verified by MCP Inspector on **2026-08-05**: connected
without credentials, listed its tools, and answered a real `tools/call`. The
verdicts, the run, and — importantly — what was *not* verified are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | **PASS** | 4 | project repository, documentation and code |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | **PASS** | 3 | repository structure, generated explanation |

Transport is **Streamable HTTP** for all of them. That is not a preference: an
earlier run of the same checker used SSE and every GitMCP endpoint answered
`405`. A client that cannot speak Streamable HTTP needs the `mcp-remote` bridge,
shown at the end of this document.

### `go-htmx-docs` — PASS

Endpoint: `https://gitmcp.io/donseba/go-htmx`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `fetch_go_htmx_documentation`
- `search_go_htmx_documentation`
- `search_go_htmx_code`
- `fetch_generic_url_content`

Use it for: the header-inspection helpers, middleware, component rendering and SSE code — the actual function locations.

### `deepwiki` — PASS

Endpoint: `https://mcp.deepwiki.com/mcp`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `ask_question`
- `read_wiki_contents`
- `read_wiki_structure`

Use it for: how the pieces connect, before looking up where they are.

> **Caveat.** Its answers are model-generated. Never the final citation — confirm against the repository through GitMCP.

## Not this source

Do not answer these questions from single-page-framework documentation. There is no client-side router and no client state store.

Routing a question to the wrong server does not produce an error. It produces a
confident answer about a different technology, which is worse.


## Priority

1. This project's code, manifests and lock files.
2. Deterministic build and test evidence, with exit codes.
3. The servers above, in the order listed.
4. Official release notes, for behaviour that changed between versions.
5. Model memory — never for a version-sensitive fact.

## Calling them at all

Registering a server does not make a model use it. The rule, which belongs in
the project's agent instructions and not only here:

- do not answer an API, version-behaviour or configuration question from
  training knowledge alone;
- call the stack's `search_*` tool first, then `fetch_*` for the passage itself;
- cross-check against `search_*_code` when documentation and implementation
  could disagree;
- never assume the repository's default branch matches this project's installed
  version;
- state the repository, path and version or commit used;
- if the search found nothing, say so. Do not fill the gap from memory.

## Version-sensitive lookups

Always look up rather than recall:

- which version introduced or changed an API;
- the exact spelling of a configuration key;
- a default value, which is the thing most likely to have changed quietly.

## Fallback

When the version in the project disagrees with the version a source describes,
**stop and report the mismatch**. Record it as
`⟨verification required: what and how⟩`.


## Before sending anything outward

These are **public, third-party endpoints**. A call sends the query, the tool
arguments the agent assembled, and whatever context it included. That can carry
private source, customer data, internal hostnames, credentials, unpublished
repository names, or raw operational logs.

On a closed network, do not make these an operational dependency. Mirror the
official repositories internally, pin a commit, index them, and serve an internal
read-only MCP that returns the repository, path, commit and retrieval date with
every answer. Use the public endpoints for public technology research only.

## Connecting

`mcp-profile.json.example` next to this document holds exactly the servers in the
table. Copy it into the adapter configuration your agent reads:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | `.clinerules/` for rules; MCP is configured in the client |

The kit's root configuration deliberately carries only `microsoft-learn` and
`context7`. The per-stack servers are not enabled by default, because copying
them is how an operator says "I accept that these queries leave this machine".

Client field names differ — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. The
two values that matter are the transport and the URL.

For a client that only speaks `stdio`:

```json
{
  "mcpServers": {
    "go-htmx-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/donseba/go-htmx"]
    }
  }
}
```

## Re-checking

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/donseba/go-htmx   --transport http --method tools/list --format json
```

A tool name that has changed is a finding, not a detail: the routing rules above
name specific tools.
