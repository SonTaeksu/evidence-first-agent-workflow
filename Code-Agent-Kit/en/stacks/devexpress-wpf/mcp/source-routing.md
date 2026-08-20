# Source Routing — DevExpress WPF (v24.2+)

This stack routes to two different kinds of source, and the split is the whole
point: **DevExpress documents its own controls and Microsoft does not.** A
question answered by the wrong one of these comes back confident and wrong.

Two of the servers below were verified by MCP Inspector on **2026-08-05** —
connected without credentials, listed their tools, and answered a real
`tools/call`. Those verdicts are recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).

The DevExpress endpoint was reached separately, on **2026-08-06**. It connected
without credentials and returned its `tools/list`, so the two tool names and
their input schemas below are now **measured** rather than read. It was not taken
as far as the fourteen servers in that document: **no real `tools/call` was run
against it.** Their `PASS` is a stronger grade than this endpoint has earned, and
this document does not borrow it. Read "What the 2026-08-06 run established, and
what it did not" below before treating the two as equivalent.

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **TOOLS LISTED, NOT CALLED** (2026-08-06) | 2 measured | official DevExpress documentation, latest |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **NOT SEPARATELY EXERCISED** | 2 documented | the same, pinned to v24.2 |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | official Microsoft documentation — plain WPF, XAML, .NET |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | **PASS** | 4 | WPF conceptual docs at source |

Transport is **Streamable HTTP** for all of them. For the DevExpress endpoint
that is not a preference but the only supported transport: opening the URL in a
browser returns `405 Method Not Allowed`, and the DevExpress documentation states
that this response is expected rather than a fault. A `405` from a browser is
therefore not a reason to conclude the server is down. A client that cannot speak
Streamable HTTP needs the `mcp-remote` bridge, shown at the end of this document.

## The DevExpress server

The endpoint, the transport, the `?v=` pinning and the prompt name below are
taken from the official DevExpress documentation, read on **2026-06-16**. The
tool names and input schemas under "### Tools" are of a different kind: they were
read off the `tools/list` response of a real MCP Inspector run on **2026-08-06**
and are observed, not documented.

Endpoint: `https://api.devexpress.com/mcp/docs`  (Streamable HTTP, **no
authentication**)

### Version pinning

A version is selected with the `?v=` query parameter. The documented example is:

```
https://api.devexpress.com/mcp/docs?v=24.2
```

**Pinning is supported no earlier than v24.2**; there is no supported way to pin
v16.x or any other pre-24.2 release, which is why this stack profile is scoped to
v24.2 and later rather than to DevExpress WPF in general.

### Tools

Two, and only two. Both schemas below are transcribed from the 2026-08-06
`tools/list` response.

#### `devexpress_docs_search`

Semantic search over the documentation. Its own description states the shape of
the workflow it belongs to:

> Search DevExpress documentation for a given technology and a question. If you
> want to search for multiple technologies, pass them as a list. This tool
> returns only snippets/excerpts; full content requires a follow-up
> `devexpress_docs_get_content` call on a chosen URL. ALWAYS call
> `devexpress_docs_search` before ANY `devexpress_docs_get_content` call in a
> user request chain.

Both properties are **required**:

| Property | Type | Notes |
|---|---|---|
| `technologies` | array, `minItems: 1` | items are a **closed enum** — see below |
| `question` | string | "Your specific question or search query. Be descriptive and include relevant keywords about what you're trying to accomplish." |

`technologies` is not free text. The schema's own description says: "Use specific
technology names like 'WindowsForms', 'XtraReports', 'OfficeFileAPI' etc. You
must choose from the allowed set." The allowed set, complete:

```text
Angular              AspNet               AspNetBootstrap      AspNetCore
AspNetMvc            ASPxThemeBuilder     ASPxThemeDeployer    Blazor
CodedUIExtension     CoreLibraries        Dashboard            DesignSystem
DevExtremeAspNetMvc  eud                  eXpressAppFramework  GeneralInformation
jQuery               MAUI                 OfficeFileAPI        OfficeFileApiJava
React                ReportServer         SkinEditor           VCL
Vue                  WindowsForms         WPF                  WpfThemeDesigner
XPO                  XpoProfiler          XtraReports
```

Thirty-one values, and nothing else is accepted. Which of them this stack uses is
in "Routing rules" below.

#### `devexpress_docs_get_content`

Downloads a complete help topic by URL. Its description:

> Get full document content by URL from DevExpress documentation. PREREQUISITE:
> ALWAYS call `devexpress_docs_search` before using this tool to get valid URLs.
> The URL parameter must be obtained from the results of the
> `devexpress_docs_search` tool.

One required property:

| Property | Type | Notes |
|---|---|---|
| `url` | string | "REQUIRED: This URL must be obtained from a previous call to `devexpress_docs_search` tool. **Do not construct URLs using your general knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`" |

### A correction, recorded

An earlier revision of this document said that a schema circulating elsewhere —
a `technologies` array plus a required `question` — **contradicted** the
documented tool names, and recorded it as unverified rather than as a schema.

That was wrong, and the measurement says so plainly: that is exactly the input
schema of `devexpress_docs_search`. The circulating claim was right, and the
reasoning that dismissed it was not.

The mistake was one step of inference, not one of fact. The official DevExpress
documentation publishes the tool names and does not publish their input schemas.
Absence from the documentation was read as conflict with the documentation, and
those are different things. **"Not in the documentation" is not "contradicted by
the documentation."** The correct label for an unpublished schema is *unknown*,
which invites a measurement; *contradicted* is a verdict, and it was one this
document had no evidence to issue.

The original caution still stands on its own terms — writing a plausible schema
for a tool nobody has called is the class of invention this kit exists to
prevent, and a wrong schema fails at call time in a way that reads like the
server being broken. Declining to copy an unverified schema was right. Declaring
it false was not. This correction stays here rather than being edited away,
because the deleted version of a mistake teaches nobody anything.

### Predefined prompt

The server publishes a prompt: `mcp.dxdocs.devexpress_docs_query_workflow`.

### What the 2026-08-06 run established, and what it did not

The command, run from a Windows shell on the owner's machine:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

It returned successfully. **Established:**

- the endpoint answers over Streamable HTTP, from an ordinary developer machine;
- it requires **no credentials** — none were supplied, and none were demanded;
- it exposes exactly two tools, with the names the documentation gives;
- their full input schemas, transcribed above, including the closed
  `technologies` enum.

**Not established, and not to be implied:**

- **No real `tools/call` was run.** A `tools/list` proves transport, reachability
  and shape. It does not prove that a search returns a usable result, or any
  result. The fourteen servers recorded `PASS` in
  `docs/core/mcp-source-verification.md` were graded on a real call with real
  arguments; this endpoint has not been taken that far, so it does not carry
  their verdict. The grade here is **tools listed, not called**, and it should be
  written that way wherever it is written.
- **`?v=24.2` was not separately exercised.** The run addressed the unpinned URL
  only. Version pinning remains *documented* — the distinction the whole first
  half of this section rests on — and `dxdocs24_2` keeps a weaker verdict than
  `dxdocs` for that reason alone.
- Nothing about answer quality, uptime, or whether the default version matches
  any particular project's installed one. Those were never in scope.

An earlier attempt from the authoring environment had failed, and that failure
was correctly read as environmental rather than as evidence about DevExpress: two
endpoints already holding a `PASS` from the 2026-08-05 run —
`https://gitmcp.io/vuejs/docs` and `https://mcp.deepwiki.com/mcp` — failed
identically in the same session with

```json
{"code":"unreachable","cause":"invalid onRequestStart method"}
```

An endpoint that passed before and fails now, alongside a new endpoint failing
the same way, is a broken client or a blocked network. Withholding a verdict
then was right; the 2026-08-06 run on a working client is what supplies one now,
and it confirms the earlier failure said nothing about this server.

## Routing rules

- A question about a DevExpress control, its views, its themes, its MVVM
  framework or its docking goes to **`dxdocs`**.
- A question about WPF, XAML, binding, dependency properties, the Dispatcher,
  resources, or anything in .NET goes to **`microsoft-learn`** or **`wpf-docs`**,
  per `../../csharp-wpf/mcp/source-routing.md`.
- **Never answer a DevExpress API question from `microsoft-learn`, from
  `wpf-docs`, or from memory.** Microsoft does not document these controls, so
  the first two produce an answer about a different technology, and memory
  produces a member name that usually still exists — which means it compiles, and
  the mistake reaches production instead of the build log.
- On a v24.2 project, use **`dxdocs24_2`** rather than the latest endpoint. The
  latest documentation describes the latest release, and this stack's whole
  version discipline is defeated by reading it for a pinned project.
- A question that mixes the two — a DevExpress control bound with plain
  `Binding`, say — is two lookups, not one.

### Two rules the server states itself

Both of these come out of the tool descriptions returned by `tools/list`. They
are the server's own rules, not this kit's preference, and an agent that ignores
them is arguing with the tool it is calling:

- **Always call `devexpress_docs_search` before any `devexpress_docs_get_content`
  call in a request chain.** Search returns snippets only; the full topic needs
  the second call. There is no supported path that starts at
  `devexpress_docs_get_content`.
- **Never construct a documentation URL from memory.** The `url` argument must be
  one a previous search returned — *"Do not construct URLs using your general
  knowledge."* A guessed URL has two ways to fail and only one of them is safe:
  it 404s, or it resolves to a real topic that is not the one being asked about.
  The second reads exactly like a successful lookup.

### The `technologies` value for this stack

`technologies` is a closed enum. An agent passes the **enum value**, not the
prose name of the platform: `WPF`, never `"DevExpress WPF"`, `"wpf"` or
`".NET WPF"`. A value outside the allowed set is a **schema validation error** —
the call is rejected, it does not come back empty — so a near-miss does not
degrade into a thin answer that someone might use. It fails, loudly, which for
once is the good case.

| Question about | value |
|---|---|
| a DevExpress WPF control, view, theme, MVVM framework or docking | `WPF` |
| the WPF theme designer tooling | `WpfThemeDesigner` |
| a base type shared across DevExpress platforms | `CoreLibraries` |

The property is an array with `minItems: 1`, so more than one may be passed; a
WPF question that reaches into a shared base type is reasonably
`["WPF", "CoreLibraries"]`.

The required two-step chain, concretely:

```json
{
  "name": "devexpress_docs_search",
  "arguments": {
    "technologies": ["WPF"],
    "question": "How do I persist and restore a DockLayoutManager layout per user?"
  }
}
```

then, and only on a URL that search returned:

```json
{
  "name": "devexpress_docs_get_content",
  "arguments": {
    "url": "<copied verbatim from a result of the search above>"
  }
}
```

No URL is written out here on purpose. One written in this document is one an
agent can copy without searching, which is the rule above defeated by its own
example.

## Not this source

Do not route DevExpress questions to a package-documentation server, to Microsoft
Learn, or to a general web search. Do not route plain WPF questions to `dxdocs`
either: it documents DevExpress, and a framework question answered from a vendor's
documentation comes back describing the vendor's replacement for the framework.

Routing a question to the wrong server does not produce an error. It produces a
confident answer about a different technology, which is worse.

## Priority

1. This project's code, manifests and restore output.
2. Deterministic build and test evidence, with exit codes.
3. The servers above, in the order listed — `dxdocs` for DevExpress,
   `microsoft-learn` and `wpf-docs` for the framework.
4. Official release notes, for behaviour that changed between versions.
5. Model memory — never for a version-sensitive fact, and never at all for a
   DevExpress one.

## Calling them at all

Registering a server does not make a model use it. The rule, which belongs in
the project's agent instructions and not only here:

- do not answer an API, version-behaviour or configuration question from
  training knowledge alone;
- search first, then fetch the passage itself — on `dxdocs` that is
  `devexpress_docs_search` followed by `devexpress_docs_get_content` on the URL
  the search returned, in that order, because the server requires it;
- `devexpress_docs_search` returns the top five matches (documented on
  2026-06-16; the tool description measured on 2026-08-06 says only that it
  returns snippets and states no count). Five is not a survey. If none of them is
  on the exact control and version in question, say so rather than answering from
  the nearest one;
- never assume the endpoint's default version matches this project's installed
  version — that is what `?v=` is for;
- state the topic URL and the version used;
- if the search found nothing, say so. Do not fill the gap from memory.

## Version-sensitive lookups

Always look up rather than recall:

- which version introduced or changed a control member;
- the exact spelling of a property, and which type it lives on — in this stack
  most often the grid's view rather than the grid;
- a default value, which is the thing most likely to have changed quietly.

## Fallback

When the version in the project disagrees with the version a source describes,
**stop and report the mismatch**. Record it as
`⟨verification required: what and how⟩`.

A project below v24.2 hits this immediately and has no documented way out: `?v=`
does not reach back that far. Record the situation rather than approximating it
from the latest documentation.

## Before sending anything outward

These are **public, third-party endpoints**. A call sends the query, the tool
arguments the agent assembled, and whatever context it included. That can carry
private source, customer data, internal hostnames, credentials, unpublished
repository names, or raw operational logs.

`dxdocs` takes no authentication, which makes it easy to enable and does not make
it private. It is a vendor endpoint, and the queries an agent sends it describe
what is being built.

On a closed network, do not make these an operational dependency. Mirror the
official documentation internally, pin a version, index it, and serve an internal
read-only MCP that returns the topic URL, version and retrieval date with every
answer. Use the public endpoints for public technology research only.

## Connecting

`mcp-profile.json.example` next to this document holds exactly the servers in the
table. Copy it into the adapter configuration your agent reads:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | `.clinerules/` for rules; MCP is configured in the client |

Both DevExpress entries are registered on purpose. `dxdocs` and `dxdocs24_2` are
the server names DevExpress documents, and having both present makes the pinned
one addressable by name rather than by remembering to append a query parameter.
Delete the entries for stacks this project does not use — that is a normal edit,
not a downgrade — and read the section above before leaving any of them enabled
on a closed network, where the right answer is an internal mirror.

Client field names differ — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. The
two values that matter are the transport and the URL.

For a client that only speaks `stdio`:

```json
{
  "mcpServers": {
    "dxdocs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.devexpress.com/mcp/docs"]
    }
  }
}
```

## Re-checking

The command that produced the schemas above, for anyone who wants to repeat it or
who suspects the tools have changed:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

Expect two tools, named `devexpress_docs_search` and
`devexpress_docs_get_content`, with the input schemas transcribed above. A tool
name, a required property or an enum member that has changed is a finding, not a
detail: the routing rules above name specific tools and pass a specific enum
value, and both break silently at call time if the server has moved on.

What remains open is a rung further up: a real `tools/call` against this
endpoint, and the same two checks against `?v=24.2`. Whoever runs them should
record the outcome here with its date, and upgrade the verdict in the table above
only as far as what was actually run.

Run the same command against a known-good endpoint in the same session before
believing a failure:

```bash
npx -y @modelcontextprotocol/inspector --cli https://learn.microsoft.com/api/mcp \
  --transport http --method tools/list --format json
```

If both fail, the client or the network is the problem — which is exactly what
happened in the authoring environment, and why this endpoint went unverified
until 2026-08-06.
