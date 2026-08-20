# MCP Source Verification

Which documentation servers the stack profiles route to, how that was established,
and — the part that matters more — what was **not** established.

- **Verified:** 2026-08-05, 22:05:08 – 22:09:30 KST
- **Method:** `@modelcontextprotocol/inspector`, CLI
- **Scope:** remote endpoints, no credentials. Connect, `tools/list`, and a real
  `tools/call`
- **Result:** 16 checks — 15 `PASS`, 1 `PARTIAL`, 0 unreachable, 0 requiring
  authentication

## Why this document exists

A configuration entry naming a server that nobody has connected to is
indistinguishable from an invented one. Both look like knowledge. So every
endpoint the stack profiles reference is listed here with the outcome of a real
call, and the servers that were *named but not tested* are listed separately and
labelled as such.

## What "verified" means, precisely

The checker connected, asked for the tool list, read each tool's `inputSchema`,
built arguments from it, and called a search or question tool with a real query.
`PASS` means that call returned without error.

It does **not** mean the answers were correct. It does not mean the server will
be up tomorrow, and it does not mean the repository's default branch matches any
particular project's installed version. Those are separate claims and none of them
was tested.

## Verified servers

| Server | Endpoint | Verdict | Tools | Stacks routing to it |
|---|---|---:|---:|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | csharp-wpf, csharp-wcf, csharp-asmx |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | **PASS** | 4 | csharp-wpf |
| `wcf-docs` | `https://gitmcp.io/dotnet/docs` | **PASS** | 4 | csharp-wcf |
| `asmx-docs` | `https://gitmcp.io/dotnet/AspNetDocs` | **PASS** | 4 | csharp-asmx |
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | **PASS** | 4 | vue |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | **PARTIAL** | 5 | vue (optional) |
| `nextjs-docs` | `https://gitmcp.io/vercel/next.js` | **PASS** | 4 | nextjs |
| `nodejs-docs` | `https://gitmcp.io/nodejs/node` | **PASS** | 4 | nodejs |
| `go-docs` | `https://gitmcp.io/golang/go` | **PASS** | 4 | go |
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | **PASS** | 4 | go-htmx |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | **PASS** | 3 | go-htmx |
| `rust-book` | `https://gitmcp.io/rust-lang/book` | **PASS** | 4 | rust |
| `rust-reference` | `https://gitmcp.io/rust-lang/reference` | **PASS** | 4 | rust |
| `elixir-docs` | `https://gitmcp.io/elixir-lang/elixir` | **PASS** | 4 | elixir |

`context7` is configured at the kit root and is not part of this run. It predates
it and is required by `check-agent-config`.

### The one PARTIAL

`https://mcp.vue-mcp.org/mcp` connected without credentials and listed five
tools. Calling `vue_docs_search` returned `isError:true`. The failure is inside
the tool, not in transport or authentication, and the summary did not capture the
server-side detail.

It is therefore **optional** for the `vue` stack, and `gitmcp.io/vuejs/docs`
— which passed — is the default. Two further reasons not to depend on it: the
project is licensed **FSL-1.1-ALv2**, which is not OSI-approved, and it is one
maintainer behind a single hosted endpoint.

## Transport: Streamable HTTP, and not by preference

The first run of the same checker used SSE. Every GitMCP endpoint answered:

```text
SSE error: Non-200 status code (405)
```

Switching to Streamable HTTP made all of them pass. Some GitMCP client examples
still show SSE; prefer `http`, and use the `mcp-remote` bridge for a client that
cannot speak it.

## Two findings that came out of checking rather than reading

### GitMCP's landing page is not evidence of anything

`https://gitmcp.io/{owner}/{repo}` serves a confident page — naming the
repository, offering client snippets — **for repositories that do not exist**.
Measured:

```text
https://gitmcp.io/thisorgdoesnotexist99/norepohere99
  -> "GitMCP Documentation Server for thisorgdoesnotexist99/norepohere99"
```

The page is generated from the URL path. Fetching it in a browser establishes
nothing. To check a GitMCP endpoint is meaningful, verify the **repository** on
`github.com` — a real repository returns a page, a missing one returns nothing —
and verify the **server** with the Inspector.

### Two stacks share tool names — and this was first written too strongly

GitMCP derives tool names from the repository name. `dotnet/docs` and `vuejs/docs`
both end in `docs`, so both expose:

```text
fetch_docs_documentation
search_docs_documentation
search_docs_code
```

This was first recorded here as a collision that prohibited registering the two
together. That was wrong, and the correction is worth keeping rather than
quietly editing out.

Most clients qualify a tool by its server. Claude Code presents them as
`mcp__<server>__<tool>`, so `mcp__wcf-docs__search_docs_documentation` and
`mcp__vue-docs__search_docs_documentation` are two distinct identifiers and
nothing collides. Whether a given client flattens names instead is a fact about
that client, and was not tested.

What does survive, in any client, is weaker and still real: a model choosing
between them sees two tools with identical base names whose purpose differs only
by which repository they search. Whether each tool's *description* names its
repository was not captured in the run, so how easily a model distinguishes them
is **unknown**, not fine.

So: a caution with two cheap consequences, not a prohibition. Keep server names
distinct and descriptive — `wcf-docs` and `vue-docs`, never a bare `docs` — since
in a namespacing client that name is the only thing separating the two tools. And
when both are registered, name the server in the request rather than leaving the
choice to inference.

## DevExpress, on a different date and to a different depth

Added **2026-08-06**, after the fourteen above, and deliberately not folded into
their table because it was not taken as far.

| Server | Endpoint | What was established | Tools |
|---|---|---|---:|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | connected without credentials; `tools/list` returned | 2 |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | nothing — documented, not exercised | — |

**No `tools/call` was made.** The fourteen servers above hold `PASS` because a
real call returned; this endpoint has not been taken that far, so it is not
written as `PASS`. The pinned URL was not contacted at all.

Both tools carry input schemas, and they are a machine contract worth recording:

- `devexpress_docs_search` requires `technologies` — an array, `minItems: 1`,
  whose items come from a **closed enum** of 31 values (`WindowsForms`, `WPF`,
  `AspNetCore`, `XtraReports`, `Blazor`, `VCL`, `XPO`, `eXpressAppFramework`,
  `Dashboard`, `DevExtremeAspNetMvc` among them) — and `question`, a string.
  A prose platform name is a schema error, not an empty result.
- `devexpress_docs_get_content` requires `url`, and its own description says the
  URL must come from a search result rather than be constructed from general
  knowledge.
- The search tool's description states that it must be called before any
  `get_content` call, because it returns excerpts only.

### A correction worth keeping

Before the run, a schema circulating outside the official documentation —
`technologies` plus a required `question` — was written up here as *contradicted*,
on the reasoning that it described tools whose names did not match the documented
ones. That was wrong. The names matched all along; DevExpress simply does not
publish input schemas, and absence of documentation was read as conflict with it.
**"Not in the documentation" is not "contradicted by the documentation."** The
first is a gap a measurement closes; the second is a verdict, and there was no
evidence for it.

### Version pinning has a floor

`?v=` is supported no earlier than **v24.2**. There is no supported way to pin
v16.x or any other pre-24.2 release, so on such a project the documentation
server cannot be aligned to the code and every control-API answer is unpinned.

## Named but not verified

Local `stdio` servers, outside the remote run. Named so nobody rediscovers them;
labelled so nobody mistakes a name for a test.

| Server | Stack | Why it is here, and what is unknown |
|---|---|---|
| `next-devtools` | nextjs | Vercel's own; diagnoses a *running* project rather than reading documentation. Untested here. |
| `gopls mcp` | go | Go's official language server, experimental MCP mode, analyses the *current* project. Needs gopls ≥ v0.20. Untested here. |
| `hexdocs-mcp` | elixir | Semantic search over Hex docs. Needs Node 22, Elixir, OTP and Ollama locally. Its own documentation describes v0.6.0 while the stable release is v0.5.0. Untested here. |
| `nodejs-api-docs` | nodejs | **Not recommended.** Untested here, and the repository reads as abandoned: 9 stars, 36 commits, no releases, 42 open pull requests against 0 open issues — dependency bots accumulating on a repository nobody merges. `snyk-labs` is an experiments organisation, not a supported product line. |

## What none of this covers

- **Answer correctness.** A `PASS` is a call that returned, not a call that was right.
- **Availability over time.** Fourteen third-party endpoints are fourteen things
  that can go away. Re-run the checker rather than assuming.
- **Branch versus installed version.** Every GitMCP endpoint searches a default
  branch. That is not this project's version, and treating it as one is the
  mistake these profiles exist to prevent.

## Sending anything outward

Every endpoint above is public and third-party. A call transmits the query, the
arguments the agent assembled, and whatever context it attached — which can
include private source, customer data, internal hostnames, credentials,
unpublished repository names and raw logs.

The kit's root configuration nevertheless carries all fourteen, enabled. That
is a decision about *this* kit rather than a general recommendation: it is the
public release, and an endpoint nobody can find is not a source. The private
lineage this kit came from does treat copying a profile as the act of consent,
and on a closed network that is still the right shape — see below.

Two things follow, and they are the operator's to weigh rather than ours to
decide. Registering all fourteen costs tool-schema context on every start and
gives the model more similarly-named `search_*` tools to choose between; the
verification guide recommends keeping only the stacks in use. And every enabled
server is an egress path, so the paragraph above is not boilerplate.

On a closed network, do not make them an operational dependency. Mirror the
official repositories internally, pin a commit, index them, and serve an internal
read-only MCP that returns repository, path, commit and retrieval date with every
answer.

## Re-verifying

```bash
npx -y @modelcontextprotocol/inspector --cli <endpoint> \
  --transport http --method tools/list --format json

npx -y @modelcontextprotocol/inspector --cli <endpoint> \
  --transport http --method tools/call \
  --tool-name <search tool> --tool-arg "query=..." --format json
```

Check in this order: exit code, whether the response parsed, tool count, whether
the expected tool names are present, then the call's exit code, then the raw
output. A tool name that has changed is a finding — the per-stack routing
documents name specific tools, and a rename silently breaks them.

Re-run when a branch or release changes, and whenever an endpoint starts
answering differently.
