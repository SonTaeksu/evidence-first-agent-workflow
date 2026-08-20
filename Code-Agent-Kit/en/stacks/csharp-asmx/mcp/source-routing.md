# Source Routing — ASMX Web Service 2.0 (.NET Framework 4+)

Every server below was verified by MCP Inspector on **2026-08-05**: connected
without credentials, listed its tools, and answered a real `tools/call`. The
verdicts, the run, and — importantly — what was *not* verified are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | official Microsoft documentation |
| `asmx-docs` | `https://gitmcp.io/dotnet/AspNetDocs` | **PASS** | 4 | legacy documentation repository |

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

Use it for: System.Web.Services, WebMethod, SoapHeader, XML serialization, SOAP 1.1 and 1.2, WSDL, IIS hosting.

### `asmx-docs` — PASS

Endpoint: `https://gitmcp.io/dotnet/AspNetDocs`  (Streamable HTTP)

Tools actually exposed, as observed rather than as documented:

- `fetch_AspNetDocs_documentation`
- `search_AspNetDocs_documentation`
- `search_AspNetDocs_code`
- `fetch_generic_url_content`

Use it for: ASP.NET 4.x pages specifically, which is how ASMX answers are kept apart from ASP.NET Core ones.

## Not this source

Do not answer ASMX questions from WCF or ASP.NET Core documentation. The serializer, the attribute model and the hosting pipeline are all different.

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
