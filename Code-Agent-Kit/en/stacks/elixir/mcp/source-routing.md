# Source Routing — Elixir

Every server below was verified by MCP Inspector on **2026-08-05**: connected
without credentials, listed its tools, and answered a real `tools/call`. The
verdicts, the run, and — importantly — what was *not* verified are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `elixir-docs` | `https://gitmcp.io/elixir-lang/elixir` | **PASS** | 4 | official language repository |

Transport is **Streamable HTTP** for all of them. That is not a preference: an
earlier run of the same checker used SSE and every GitMCP endpoint answered
`405`. A client that cannot speak Streamable HTTP needs the `mcp-remote` bridge,
shown at the end of this document.

### `elixir-docs` — PASS

Endpoint: `https://gitmcp.io/elixir-lang/elixir`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `fetch_elixir_documentation`
- `search_elixir_documentation`
- `search_elixir_code`
- `fetch_generic_url_content`

Use it for: the language and its standard library. Phoenix, LiveView and Ecto are separate projects and are not covered here.

## Not this source

Do not answer from a shared-mutable-state framework's documentation. Do not mix LiveView major-version guidance; the lifecycle changed.

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

## Named but not verified

These are local `stdio` servers. They were **not** part of the verified run, so
nothing here says they work. They are named so that nobody has to rediscover
them, and marked so that nobody mistakes a name for a test.

**`hexdocs-mcp`** — `npx -y hexdocs-mcp@0.5.0`

Semantic search over Hex package docs. Not in the verified run, needs Node 22, Elixir, OTP and Ollama locally, and its own documentation describes v0.6.0 while the stable release is v0.5.0.

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

The kit's root configuration carries every server in this document, enabled.
This is the public kit; it is meant to work without anyone hunting down
endpoints first. The cost is not hidden. The verification guide's own advice is
the opposite of shipping them all: registering only the stacks a project
actually uses "reduces tool-routing errors and unnecessary tool-schema
context". So delete the entries for stacks this project does not use — that is
a normal edit, not a downgrade. And read the section above before leaving any
of them enabled on a closed network, where the right answer is an internal
mirror rather than these endpoints.

Client field names differ — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. The
two values that matter are the transport and the URL.

For a client that only speaks `stdio`:

```json
{
  "mcpServers": {
    "elixir-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/elixir-lang/elixir"]
    }
  }
}
```

## Re-checking

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/elixir-lang/elixir   --transport http --method tools/list --format json
```

A tool name that has changed is a finding, not a detail: the routing rules above
name specific tools.
