# Source Routing — WCF (.NET Framework 4.7.2+)

Every server below was verified by MCP Inspector on **2026-08-05**: connected
without credentials, listed its tools, and answered a real `tools/call`. The
verdicts, the run, and — importantly — what was *not* verified are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | official Microsoft documentation |
| `wcf-docs` | `https://gitmcp.io/dotnet/docs` | **PASS** | 4 | documentation repository, searched as source |

Transport is **Streamable HTTP** for all of them. That is not a preference: an
earlier run of the same checker used SSE and every GitMCP endpoint answered
`405`. A client that cannot speak Streamable HTTP needs the `mcp-remote` bridge,
shown at the end of this document.

### `microsoft-learn` — PASS

Endpoint: `https://learn.microsoft.com/api/mcp`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `microsoft_docs_search`
- `microsoft_code_sample_search`
- `microsoft_docs_fetch`

Use it for: System.ServiceModel, bindings, hosting, message and transport security, certificates, SOAP and WSDL, faults, channel model.

### `wcf-docs` — PASS

Endpoint: `https://gitmcp.io/dotnet/docs`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `fetch_docs_documentation`
- `search_docs_documentation`
- `search_docs_code`
- `fetch_generic_url_content`

Use it for: the .NET conceptual docs at source.

## Not this source

Do not route WCF questions to a package-documentation server, and do not answer them from ASP.NET Core or gRPC documentation — the configuration model is unrelated.

Routing a question to the wrong server does not produce an error. It produces a
confident answer about a different technology, which is worse.

## Shares tool names with `vuejs/docs`

GitMCP derives tool names from the repository name, and this stack's repository
and `vuejs/docs` end in the same segment. Both expose:

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
`wcf-docs` above rather than a bare `docs` — because in a namespacing client
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
    "microsoft-learn": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://learn.microsoft.com/api/mcp"]
    }
  }
}
```

## Re-checking

```bash
npx -y @modelcontextprotocol/inspector --cli https://learn.microsoft.com/api/mcp   --transport http --method tools/list --format json
```

A tool name that has changed is a finding, not a detail: the routing rules above
name specific tools.
