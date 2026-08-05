# Source Routing — Vue.js

Every server below was verified by MCP Inspector on **2026-08-05**: connected
without credentials, listed its tools, and answered a real `tools/call`. The
verdicts, the run, and — importantly — what was *not* verified are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | **PASS** | 4 | official documentation repository |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | **PARTIAL** | 5 | ecosystem search, optional |

Transport is **Streamable HTTP** for all of them. That is not a preference: an
earlier run of the same checker used SSE and every GitMCP endpoint answered
`405`. A client that cannot speak Streamable HTTP needs the `mcp-remote` bridge,
shown at the end of this document.

### `vue-docs` — PASS

Endpoint: `https://gitmcp.io/vuejs/docs`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `fetch_docs_documentation`
- `search_docs_documentation`
- `search_docs_code`
- `fetch_generic_url_content`

Use it for: the Vue documentation at source, and the version-specific pages that decide every Vue 2 versus Vue 3 answer.

### `vue-docs-specialized` — PARTIAL

Endpoint: `https://mcp.vue-mcp.org/mcp`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `vue_docs_search`
- `vue_api_lookup`
- `vue_get_related`
- `set_framework_preferences`
- `ecosystem_search`

Use it for: broader ecosystem coverage (Router, Pinia, Vite, Vitest, Nuxt) if and when its search tool works.

> **Caveat.** Connection and tools/list succeeded; `vue_docs_search` returned isError:true on a real call. Not a default dependency. The project is also FSL-1.1-ALv2, which is not an OSI-approved licence, and is maintained by one person behind a single hosted endpoint.

## Not this source

Do not answer Vue questions from Microsoft Learn. Do not carry Vue 2 answers into a Vue 3 project or the reverse — the reactivity system differs.

Routing a question to the wrong server does not produce an error. It produces a
confident answer about a different technology, which is worse.

## Shares tool names with `dotnet/docs`

GitMCP derives tool names from the repository name, and this stack's repository
and `dotnet/docs` end in the same segment. Both expose:

- `fetch_docs_documentation`
- `search_docs_documentation`
- `search_docs_code`

**This is a caution, not a prohibition, and the distinction matters.** Most
clients qualify a tool by its server — Claude Code presents them as
`mcp__<server>__<tool>` — so registering both gives two distinctly addressable
tools and nothing collides. Whether a particular client flattens names instead is
a fact about that client and was not tested here.

What remains, in any client, is that a model choosing between them sees two tools
whose base names are identical and whose purpose differs only by which repository
they search. Whether each tool's *description* names its repository was not
captured in the verification run, so how easily a model tells them apart is
unknown rather than fine.

Two cheap consequences. Keep the server names distinct and descriptive — the
`vue-docs` above rather than a bare `docs` — because in a namespacing client
that name is the only thing distinguishing the two tools. And when both are
registered, say which server to use in the request rather than leaving the choice
to inference.

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
    "vue-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/vuejs/docs"]
    }
  }
}
```

## Re-checking

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/vuejs/docs   --transport http --method tools/list --format json
```

A tool name that has changed is a finding, not a detail: the routing rules above
name specific tools.
