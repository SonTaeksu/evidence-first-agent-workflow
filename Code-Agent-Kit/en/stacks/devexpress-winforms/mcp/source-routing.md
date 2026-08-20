# Source Routing — DevExpress WinForms

Two documentation sources, and the split between them is the whole point of this
document. DevExpress questions go to `dxdocs`. Windows Forms and .NET questions go
to `microsoft-learn`. Neither answers the other's questions, and a wrong route
here does not produce an error — it produces a confident answer about a different
control library.

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **`tools/list` returned; no `tools/call`** (2026-08-06) | 2 | DevExpress official documentation, latest release |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **documented; the pinned URL was not exercised** | 2 | the same server pinned to v24.2 |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** (2026-08-05) | 3 | Windows Forms, C#, .NET, MSBuild — everything that is not DevExpress |

`microsoft-learn`'s verdict comes from the Inspector run recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).
The two DevExpress rows carry a different, weaker verdict, and the difference is
the next section.

## Verification status — read this before trusting the table

The endpoint has now been reached, and the grade it earned is a specific one. It
is not `PASS`, and reading it as `PASS` would be the mistake this section exists
to prevent.

**What was measured.** On **2026-08-06**, from a Windows shell on the owner's
machine, `@modelcontextprotocol/inspector` was pointed at
`https://api.devexpress.com/mcp/docs` with
`--transport http --method tools/list --format json`. It connected **without
credentials** and returned **two tools**, with exactly the names the
documentation gives. The input schemas in *The two tools* below are that run's
output rather than a reading of the documentation.

**What was not measured, and why the verdict stops where it does.**

- **No `tools/call` was run.** The fourteen servers in
  `docs/core/mcp-source-verification.md` are recorded `PASS` because each one
  answered a real call: arguments built from the server's own `inputSchema`, a
  query sent, a result returned without error. This endpoint has not been taken
  that far. A `tools/list` establishes that the server is there, speaks
  Streamable HTTP, needs no credentials, and declares these two tools with these
  schemas. It establishes nothing about whether a search returns usable topics.
  Do not borrow the `PASS` grade for it, and do not add it to
  `docs/core/mcp-source-verification.md` until a call has returned.
- **`?v=24.2` was not exercised separately.** The pinned URL was not run. Its row
  in the table still rests on the documentation alone, and the fact that the
  unpinned URL answers is not evidence that the pinned one does.

An earlier attempt failed inside the authoring environment, where two endpoints
already recorded `PASS` — `https://gitmcp.io/vuejs/docs` and
`https://mcp.deepwiki.com/mcp` — failed identically with
`{"code":"unreachable","cause":"invalid onRequestStart method"}`. That reading —
a fact about the environment, not about the endpoint — is now confirmed: the same
endpoint answered on the first try from a machine with outbound access.

Everything in *What the documentation says* still comes from the official
DevExpress documentation, retrieved **2026-06-16**, except where the 2026-08-06
run has since confirmed it. Documentation remains a weaker class of evidence than
a call that returned.

### Settling the rest

Two things are still open. Both are one command each, from a machine with
outbound network access.

A real `tools/call`, which is what would make this endpoint `PASS` on the same
terms as the other fourteen:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/call --tool-name devexpress_docs_search \
  --tool-arg 'technologies=["WindowsForms"]' \
  --tool-arg 'question=How do I hide a GridView column at runtime?' \
  --format json
```

And the pinned endpoint, which has still not answered anything:

```bash
npx -y @modelcontextprotocol/inspector --cli "https://api.devexpress.com/mcp/docs?v=24.2" \
  --transport http --method tools/list --format json
```

Record either result in `references/verified-facts.md` with its date. A tool name
or schema that differs from the one below is a finding rather than a detail — the
routing rules in this document name specific tools and pass specific arguments.

## What the documentation says

- **No authentication.** The endpoint takes no credentials. *Confirmed by the
  2026-08-06 run, which connected without any.*
- **Streamable HTTP only.** There is no SSE transport and no plain GET interface.
  Opening the URL in a browser returns `405 Method Not Allowed`, and the
  documentation states that this is the expected response rather than a fault. Do
  not read a browser `405` as an outage, and do not use it as a health check — it
  is what a working server returns to the wrong verb.
- **Version pinning uses `?v=`,** and is supported **no earlier than v24.2**.
  `https://api.devexpress.com/mcp/docs?v=24.2` is the documented example. There is
  no supported way to pin an older release, so on a pre-24.2 project the
  documentation server cannot be aligned to the code and every control-API answer
  must be treated as unpinned.
- **Two tools, and only two.** *Confirmed by the 2026-08-06 `tools/list`, which
  returned these two names and no others.*
- **A predefined prompt exists:** `mcp.dxdocs.devexpress_docs_query_workflow`.
- **Documented server names:** `dxdocs` for the latest release and `dxdocs24_2`
  for the pinned one. Both are registered in `mcp-profile.json.example`, because a
  project needs the pinned one and the kit should not make anyone guess the naming
  convention for the other.

## The two tools

The schemas below are the `tools/list` output of the 2026-08-06 run, not a
paraphrase of the documentation.

| Tool | What it does | Parameters |
|---|---|---|
| `devexpress_docs_search` | semantic search across the documentation; returns the top five matches, and **only snippets** — the full topic needs a second call | `technologies` — array, `minItems: 1`, **required**; each item a value from the closed enum below. `question` — string, **required** |
| `devexpress_docs_get_content` | downloads a complete help topic by its URL | `url` — string, **required**; must have come from a `devexpress_docs_search` result |

`technologies` — the server's own description: *"Use specific technology names
like 'WindowsForms', 'XtraReports', 'OfficeFileAPI' etc. You must choose from the
allowed set."* The allowed set is closed, and complete:

```
Angular, AspNet, AspNetBootstrap, AspNetCore, AspNetMvc, ASPxThemeBuilder,
ASPxThemeDeployer, Blazor, CodedUIExtension, CoreLibraries, Dashboard,
DesignSystem, DevExtremeAspNetMvc, eud, eXpressAppFramework, GeneralInformation,
jQuery, MAUI, OfficeFileAPI, OfficeFileApiJava, React, ReportServer, SkinEditor,
VCL, Vue, WindowsForms, WPF, WpfThemeDesigner, XPO, XpoProfiler, XtraReports
```

`question` — *"Your specific question or search query. Be descriptive and include
relevant keywords about what you're trying to accomplish."*

`url` — *"REQUIRED: This URL must be obtained from a previous call to
`devexpress_docs_search` tool. **Do not construct URLs using your general
knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`"*

### A recorded correction

This section previously said the parameter columns were *deliberately empty*, on
the reasoning that a `technologies`/`question` schema circulating elsewhere
"describes tools whose names do not match the two documented above", and that two
contradicting descriptions of the same server were a reason to record neither.

**That reasoning was wrong, and the measurement is what shows it.** The
`technologies`/`question` schema is `devexpress_docs_search`'s own input schema,
returned by the server under exactly that tool name. Nothing contradicted
anything. The official documentation simply does not publish input schemas, and
the absence of a schema in the documentation was read as the documentation
disagreeing with the schema.

The lesson is kept here rather than deleted: **"not in the documentation" is not
the same as "contradicted by the documentation."** The first is a gap and is
settled by measuring; the second is a conflict and needs adjudicating. Treating
the first as the second withheld a schema that was available all along, and left a
`⟨verification required⟩` where an agent needed argument names.

## Routing rules

- A DevExpress control, property, event, service or namespace question goes to
  `dxdocs`. Always. There is no exception for "obvious" ones — a control library
  this large is where recall is least reliable.
- A Windows Forms, C#, .NET, MSBuild or configuration-schema question goes to
  `microsoft-learn`.
- **Never answer a DevExpress API question from `microsoft-learn`.** Microsoft
  Learn does not document a third-party control library. Asked about `GridControl`
  it will find `DataGridView` and answer about that, which is a different type
  with different members and no error message to say so.
- **Never answer a DevExpress API question from memory.** Not the property name,
  not the enumeration member, not the namespace, not which release introduced it.
- **On a v24.2 project, use `dxdocs24_2`.** The unpinned `dxdocs` answers from the
  latest release, and a member added after v24.2 will be described as though it
  were available. That failure is silent until compile time at best and until
  runtime at worst.
- Do not route DevExpress questions to a general package-documentation server
  either. The documentation is the product's own; a repository mirror is not it.

### The server's own two rules

These are not this kit's preferences. Both are stated in the tool descriptions the
server returns, which makes them the server's own contract:

- **Always call `devexpress_docs_search` before any `devexpress_docs_get_content`.**
  The search description says so in as many words, and the reason is in the
  schema: search returns snippets and excerpts only, so the full topic always
  costs a second call. A `get_content` that was not preceded by a search in the
  same request chain is out of contract.
- **Never construct a documentation URL from memory.** The `url` parameter's own
  description says *do not construct URLs using your general knowledge* — the
  value must be one that a `devexpress_docs_search` result returned. A plausible
  `https://docs.devexpress.com/WindowsForms/…` assembled from recall is exactly
  the failure this rule names, and a wrong-but-well-formed URL fails as a fetch
  rather than as a routing error.

### The `technologies` value for this stack

`technologies` is a closed enum, and an agent must pass the enum value rather than
a prose platform name. `"DevExpress WinForms"`, `"WinForms"` and
`"Windows Forms"` are not members of the set; passing one is a **schema
validation error**, not an empty result set. It fails loudly at the call rather
than quietly at the answer — which is the good case, provided nobody retries with
another invented spelling.

- DevExpress WinForms questions — `WindowsForms`.
- Where this stack's material touches reporting — `XtraReports`.
- Shared base types, common enumerations and cross-product infrastructure —
  `CoreLibraries`.

More than one may be passed; the parameter is an array with `minItems: 1`. A grid
question that ends in a print or export path is reasonably
`["WindowsForms", "XtraReports"]`.

A concrete call:

```json
{
  "name": "devexpress_docs_search",
  "arguments": {
    "technologies": ["WindowsForms"],
    "question": "How do I hide a GridView column at runtime without removing it from the columns collection?"
  }
}
```

and only then, with a URL taken from that result:

```json
{
  "name": "devexpress_docs_get_content",
  "arguments": { "url": "https://docs.devexpress.com/CoreLibraries/405204" }
}
```

## Priority

1. This project's code, project files and package or lock files.
2. Deterministic build and test evidence, with exit codes.
3. `dxdocs24_2` — or `dxdocs`, when the project really is on the latest release.
4. `microsoft-learn`, for the Windows Forms and .NET layer underneath.
5. Official DevExpress release notes, for behaviour that changed between versions.
6. Model memory — never for a version-sensitive fact, and never for a DevExpress
   member name.

## Calling them at all

Registering a server does not make a model use it. The rule, which belongs in the
project's agent instructions and not only here:

- do not answer an API, version-behaviour or configuration question from training
  knowledge alone;
- search first, then fetch the topic itself — `devexpress_docs_search` returns the
  top five matches as snippets, which is a shortlist rather than an answer, and
  `devexpress_docs_get_content` is what retrieves the passage. The server states
  this ordering itself; see *The server's own two rules* above;
- read the returned topic rather than its title. A search hit is a candidate;
- state the topic URL and the version the answer came from;
- if the search found nothing, say so. Do not fill the gap from memory.

## Version-sensitive lookups

Always look up rather than recall:

- which release introduced or changed a member;
- the exact spelling of a property, an enumeration member or a namespace;
- whether a setting belongs to the control or to its view;
- a default value, which is the thing most likely to have changed quietly.

## Fallback

When the DevExpress version in the project disagrees with the version a source
describes, **stop and report the mismatch**. Do not implement against whichever
version the documentation happened to show. Record the unresolved item as
`⟨verification required: what and how⟩`.

## Before sending anything outward

`api.devexpress.com` and `learn.microsoft.com` are **public, third-party
endpoints**. A call sends the query, the tool arguments the agent assembled, and
whatever context it included. That can carry private source, customer data,
internal hostnames, credentials, unpublished repository names, or raw operational
logs. A question phrased as "why does *our* order grid on the settlement screen
throw" carries more than a question about a grid.

On a closed network, do not make these an operational dependency. Mirror the
documentation internally, pin the release, index it, and serve an internal
read-only MCP that returns the topic, version and retrieval date with every
answer. Use the public endpoints for public technology research only.

## Connecting

`mcp-profile.json.example` next to this document holds exactly the servers in the
table above. Copy it into the adapter configuration your agent reads:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | `.clinerules/` for rules; MCP is configured in the client |

Client field names differ — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. The
two values that matter are the transport and the URL, and the transport here is
not optional: **Streamable HTTP**. A client configured for SSE will not connect.

Delete the endpoints this project does not need — registering fewer servers
reduces tool-routing errors and unnecessary tool-schema context, and a project on
v24.2 needs `dxdocs24_2` rather than both DevExpress entries. And read the section
above before leaving any of them enabled on a closed network, where the right
answer is an internal mirror rather than these endpoints.

For a client that only speaks `stdio`:

```json
{
  "mcpServers": {
    "dxdocs24_2": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.devexpress.com/mcp/docs?v=24.2"]
    }
  }
}
```

`⟨verification required: that the mcp-remote bridge reaches this endpoint — it
was not tried here, for the same reason the Inspector was not⟩`

## Re-checking

Re-run the `tools/list` command above when a DevExpress release changes, when the
project moves to a different version, and whenever the server starts answering
differently. A tool name that has changed is a finding, not a detail: the routing
rules above name specific tools.
