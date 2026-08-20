# MCP — one page

Everything you need to point an agent at real documentation instead of its own
memory. This replaces the two files that used to live in `docs/core/`
(`mcp-knowledge-routing.md`, `mcp-result-compaction.md`).

Two things are deliberately **not** here:

- **The evidence.** What was actually connected to, what it exposed, and what was
  only named, is in [`core/mcp-source-verification.md`](core/mcp-source-verification.md).
  A server nobody has connected to reads exactly like an invented one, so that
  distinction is kept in writing rather than in memory.
- **Per-stack routing.** `stacks/<name>/mcp/source-routing.md` stays inside its
  stack, because `install-kit.py` installs one stack at a time. Moving it here
  would hand installed projects half a stack.

## What ships, and it is all switched on

The kit's configurations carry seventeen servers, all enabled. Fourteen of them
answered MCP Inspector on **2026-08-05**: connected without credentials, listed
their tools, and returned a real `tools/call`. `context7` is stdio and predates
that run. The two DevExpress entries are graded lower — see the note under the
table.

| Server | Endpoint | For |
|---|---|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | .NET, C#, ASP.NET Core, EF Core |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | WPF |
| `wcf-docs` | `https://gitmcp.io/dotnet/docs` | WCF |
| `asmx-docs` | `https://gitmcp.io/dotnet/AspNetDocs` | ASMX / ASP.NET web services |
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | Vue |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | Vue ecosystem — **PARTIAL**, see below |
| `nextjs-docs` | `https://gitmcp.io/vercel/next.js` | Next.js |
| `nodejs-docs` | `https://gitmcp.io/nodejs/node` | Node.js |
| `go-docs` | `https://gitmcp.io/golang/go` | Go |
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | Go + HTMX |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | any public repository, narrative form |
| `rust-book` | `https://gitmcp.io/rust-lang/book` | Rust, the book |
| `rust-reference` | `https://gitmcp.io/rust-lang/reference` | Rust, the reference |
| `elixir-docs` | `https://gitmcp.io/elixir-lang/elixir` | Elixir |
| `context7` | stdio, `npx -y @upstash/context7-mcp` | React, Vite, Vitest, Playwright |
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | DevExpress components — **listed, not called**, see below |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | the same, pinned to v24.2 |

Transport for every remote server is **Streamable HTTP**. That is not a
preference: an earlier run used SSE and every GitMCP endpoint answered `405`.

### Two caveats worth reading before you rely on this

**`vue-docs-specialized` is PARTIAL.** It connected and listed five tools, but a
real `vue_docs_search` call returned `isError:true`. Prefer `vue-docs`. It is
shipped enabled so you can retry it yourself, not because it works.

**The two DevExpress entries are not the same grade as the rest.** On
**2026-08-06** the endpoint connected without credentials and returned
`tools/list` with two tools, `devexpress_docs_search` and
`devexpress_docs_get_content`. No real `tools/call` was run, and the pinned URL
was not separately exercised, so neither is recorded as `PASS`.

Two rules come from the server's own tool descriptions rather than from this kit.
`devexpress_docs_search` must be called before any `devexpress_docs_get_content`,
because search returns excerpts only. And a URL passed to `get_content` must come
from a search result — the schema says in as many words not to construct one from
general knowledge. `devexpress_docs_search` also requires a `technologies` array
drawn from a closed enum (`WindowsForms`, `WPF`, `AspNetCore`, `XtraReports`,
`Blazor`, `VCL`, `XPO` and others), so a prose platform name is a schema error
rather than an empty result. Version pinning with `?v=` is supported no earlier
than **v24.2**; there is no supported way to pin an older release.

**Shipping all seventeen has a price.** The verification guide's own advice is the
opposite: register only the stacks a project actually uses, because that
"reduces tool-routing errors and unnecessary tool-schema context". Every server
costs schema context at every start, and several expose similarly named
`search_*` and `fetch_*` tools that a model must choose between. **Deleting the
entries for stacks you do not use is a normal edit, not a downgrade.**

## Source priority

1. This project's code, manifests, lock files and generated artifacts.
2. Deterministic build, test and runtime evidence, with exit codes.
3. Official documentation retrieved through MCP.
4. Official repositories and release notes.
5. Model memory — never for a version-sensitive fact.

## Routing by technology

| Ask about | Use |
|---|---|
| .NET, C#, ASP.NET Core, DI, configuration, logging, auth, EF Core | `microsoft-learn` |
| React core | `context7`, pinned to `/facebook/react` |
| Vite, Vitest, React Testing Library, Playwright, React Router | `context7` — resolve the library ID first |
| Anything with a stack profile | that stack's `mcp/source-routing.md` |

Routing a question to the wrong server does not produce an error. It produces a
confident answer about a different technology, which is worse.

## Registering a server does not make a model use it

This belongs in the project's agent instructions, not only here:

- do not answer an API, version-behaviour or configuration question from
  training knowledge alone;
- call `search_*` first, then `fetch_*` for the passage itself;
- cross-check `search_*_code` when documentation and implementation could
  disagree;
- never assume a repository's default branch matches this project's installed
  version;
- state the repository, path and version or commit used;
- if the search found nothing, say so. Do not fill the gap from memory.

Always look up rather than recall: which version introduced or changed an API,
the exact spelling of a configuration key, and any default value — the last
being the thing most likely to have changed quietly.

## When MCP is unavailable

1. Inspect local project code and lock files.
2. Use an official source only.
3. Stop and report `knowledge unavailable` for version-sensitive behaviour that
   cannot be verified.
4. Do not silently replace an official-source lookup with model memory.

When the version in the project disagrees with the version a source describes,
**stop and report the mismatch** as `⟨verification required: what and how⟩`.

## Compacting what comes back

MCP reduces search effort. It does not remove context limits.

1. Extract only the fact the task needs.
2. Record source, version and verification method.
3. Put the compact fact in the worklog or the stack's `evidence-provenance.md`.
4. Keep a link or identifier where permitted.
5. Do not copy the full retrieval result into current state.
6. Do not re-inject the full result in a later session.

Current state records verified decisions, not retrieval transcripts.

## Connecting

The kit already ships these configured. The files, by agent:

| Agent | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo / Zoo | `.roo/mcp.json` |
| Cline | `agent-configs/cline/mcp.example.json`, copied into the client |

Field names differ between clients — `mcpServers`, `servers`, `serverUrl`,
`httpUrl`. The two values that matter are the transport and the URL.

`.codex/config.toml` uses underscores in its keys (`vue_docs`) because that is
what the file already used, so the server name Codex shows may differ from the
hyphenated name (`vue-docs`) used everywhere else. ⟨verification required:
whether Codex accepts hyphenated keys — it was not tested.⟩

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

## Before sending anything outward

These are **public, third-party endpoints**. A call sends the query, the tool
arguments the agent assembled, and whatever context it included — which can
carry private source, customer data, internal hostnames, credentials,
unpublished repository names or raw operational logs.

On a closed network, do not make these an operational dependency. Mirror the
official repositories internally, pin a commit, index them, and serve an
internal read-only MCP that returns repository, path, commit and retrieval date
with every answer. Use the public endpoints for public technology research only.

## Re-checking

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/vuejs/docs \
  --transport http --method tools/list --format json
```

A tool name that has changed is a finding, not a detail: the routing rules above
name specific tools.
