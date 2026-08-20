# Source Routing — DevExpress for ASP.NET Core

Two sources, and the split between them is the whole point of this document.
DevExpress questions go to `dxdocs`. ASP.NET Core, EF Core and .NET questions go
to `microsoft-learn`. Neither answers the other's questions, and neither is a
substitute for memory being switched off.

| Server | Endpoint | Verdict | Tools | Role |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **`tools/list` measured, 2026-08-06 — no call made** | 2 | DevExpress documentation, latest |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **documented, not separately exercised** | 2 | the same server pinned to v24.2 |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | ASP.NET Core, C#, .NET, EF Core |

`microsoft-learn` is one of the endpoints verified by MCP Inspector on
2026-08-05 and recorded in
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md).
The DevExpress rows carry a different and weaker grade. What follows says exactly
what that means.

## Verification status of the DevExpress server

**The endpoint was reached on 2026-08-06.** MCP Inspector, CLI, from a Windows
shell on the owner's machine, against `https://api.devexpress.com/mcp/docs` with
`--transport http --method tools/list --format json`. It connected and returned
without credentials. Two tools, with exactly the names the documentation gives:
`devexpress_docs_search` and `devexpress_docs_get_content`. Their input schemas
are recorded below, from that output rather than from reading.

**That is not a `PASS`, and it must not be written as one.** The fourteen servers
in [`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)
are recorded `PASS` because a real `tools/call` returned without error. No
`tools/call` was run here. What is established is connection, no authentication,
tool names and tool schemas — that the server answers a *query* is still
unmeasured. Borrowing the other servers' grade for this one would be exactly the
substitution this kit exists to stop.

`?v=24.2` was **not separately exercised.** Everything about the pinned row is
still documentation, and the measurement above says nothing about whether the
query parameter is honoured.

The earlier Inspector attempt, in the authoring environment, had failed with:

```json
{"code":"unreachable","cause":"invalid onRequestStart method"}
```

That was read at the time as a fact about the environment rather than about
DevExpress, because two endpoints already recorded **PASS** —
`https://gitmcp.io/vuejs/docs` and `https://mcp.deepwiki.com/mcp` — failed
identically in the same attempt. The 2026-08-06 run on a different machine
confirms that reading.

## `dxdocs` — reached, listed, not yet called

Endpoint: `https://api.devexpress.com/mcp/docs`

- **No authentication.** The documentation does not describe a credential.
- **Streamable HTTP only.** Opening the URL in a browser returns
  `405 Method Not Allowed`, and the documentation states that this is expected
  rather than a fault. Do not treat that response as the server being down, and
  do not treat a browser visit as a check — it establishes nothing either way.
- **Two tools, and only two** — confirmed by the `tools/list` run, with the names
  the documentation gives:
  - `devexpress_docs_search` — semantic search; the documentation says the top
    five matches, and the tool's own description says those matches are snippets
    rather than full content.
  - `devexpress_docs_get_content` — downloads a complete help topic by URL.
- **A predefined prompt exists:** `mcp.dxdocs.devexpress_docs_query_workflow`.

Use it for: every DevExpress question — components, tag helpers, DevExtreme
widgets, Reporting, service registration, and anything with a DevExpress type or
member name in it.

### The measured schemas

From the `tools/list` output of 2026-08-06.

**`devexpress_docs_search`** — "Search DevExpress documentation for a given
technology and a question. If you want to search for multiple technologies, pass
them as a list. This tool returns only snippets/excerpts; full content requires a
follow-up `devexpress_docs_get_content` call on a chosen URL. ALWAYS call
`devexpress_docs_search` before ANY `devexpress_docs_get_content` call in a user
request chain."

Both properties are **required**:

| Property | Type | Constraint |
|---|---|---|
| `technologies` | array | `minItems: 1`; each item is a **closed enum**, listed below |
| `question` | string | "Your specific question or search query. Be descriptive and include relevant keywords about what you're trying to accomplish." |

The enum's own description: "Use specific technology names like 'WindowsForms',
'XtraReports', 'OfficeFileAPI' etc. You must choose from the allowed set." The
allowed set, complete:

```text
Angular            AspNet              AspNetBootstrap    AspNetCore
AspNetMvc          ASPxThemeBuilder    ASPxThemeDeployer  Blazor
CodedUIExtension   CoreLibraries       Dashboard          DesignSystem
DevExtremeAspNetMvc  eud               eXpressAppFramework  GeneralInformation
jQuery             MAUI                OfficeFileAPI      OfficeFileApiJava
React              ReportServer        SkinEditor         VCL
Vue                WindowsForms        WPF                WpfThemeDesigner
XPO                XpoProfiler         XtraReports
```

**`devexpress_docs_get_content`** — "Get full document content by URL from
DevExpress documentation. PREREQUISITE: ALWAYS call `devexpress_docs_search`
before using this tool to get valid URLs. The URL parameter must be obtained from
the results of the `devexpress_docs_search` tool."

Required: `url`, a string — "REQUIRED: This URL must be obtained from a previous
call to `devexpress_docs_search` tool. **Do not construct URLs using your general
knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`"

### A correction, kept rather than edited out

This document previously named the `technologies`/`question` schema and rejected
it, on the grounds that it "describes tools with different names from the
documented ones, so it is not a description of this server". **That was wrong.**
The measured output shows that schema is `devexpress_docs_search`'s own.

What produced the error is worth more than the error: the official documentation
names the two tools but does not publish their input schemas, and the absence of
a published schema was read as the documentation *contradicting* the circulating
one. It did no such thing. **"Not in the documentation" is not "contradicted by
the documentation."** The first is a gap, and a gap is closed by measuring; the
second is a conflict, and a conflict is grounds for rejection. Treating the first
as the second discards a true fact with the same confidence it would discard a
false one.

The original caution was still right about one thing, which is why the schema
above is dated and attributed to a run rather than to a page found elsewhere.

### Which `technologies` value this stack passes

This is the part of the schema that decides whether an answer comes from the
right corpus, and it is the part most easily got wrong — because a wrong-but-valid
value returns results rather than an error.

| The question is about | Pass |
|---|---|
| DevExpress components for ASP.NET Core, tag helpers, service registration | `AspNetCore` |
| DevExpress Reporting — the viewer, the designer, report definitions, storage | `XtraReports` |
| DevExtreme-based MVC wrappers | `DevExtremeAspNetMvc` |
| Classic ASP.NET MVC 5 | `AspNetMvc` |

**Reporting is a separate enum value.** `XtraReports` is not inside `AspNetCore`.
A reporting question routed under `AspNetCore` alone searches the component
corpus and returns component topics — plausible, on-brand, and about something
else. Pass both values when the question is reporting hosted in ASP.NET Core,
which in this stack is most of them.

**Which MVC value applies is a project fact, not a guess.** `DevExtremeAspNetMvc`
and `AspNetMvc` are different corpora for different products, and a project must
establish which it uses before the value can be chosen. That is the
`ui-component-layer` capability in `capability-detection.md`, and it blocks for
this reason among others.

`Blazor` is in the allowed set. It is **out of this stack's scope** — a Blazor
question is a different profile, not this one.

Two more consequences of the enum being closed:

- **Pass the enum value, not a prose platform name.** "ASP.NET Core MVC with
  DevExpress" is not a member of the set; `AspNetCore` is. The tool takes an
  identifier, and the identifier is the routing decision.
- **A value outside the set is a schema error, not an empty result.** `aspnetcore`,
  `ASP.NET Core`, `Reporting` and `DevExpressReporting` do not return nothing —
  the call is rejected against the schema. Read such a failure as a wrong argument
  rather than as the documentation lacking the topic.

A component question:

```json
{
  "technologies": ["AspNetCore"],
  "question": "register the DevExpress GridView tag helper in Startup"
}
```

A reporting question, carrying both values:

```json
{
  "technologies": ["AspNetCore", "XtraReports"],
  "question": "host the Web Document Viewer in an ASP.NET Core application and register its services"
}
```

## `dxdocs24_2` — the pinned server

Endpoint: `https://api.devexpress.com/mcp/docs?v=24.2`

Version pinning uses the `?v=` query parameter, and
`https://api.devexpress.com/mcp/docs?v=24.2` is the documented example. Everything
else about the server — transport, authentication, the two tools — is the same
server; the parameter selects which documentation version it answers from.

**On a v24.2 project, use `dxdocs24_2` rather than the latest endpoint.** The
whole reason pinning exists is that the latest documentation describes a product
this project is not running, and an answer from it looks identical to a correct
one.

> **Caution.** Pinning is supported **no earlier than v24.2**. There is no
> supported way to pin v16.x or any other pre-24.2 release. On such a project the
> only available answer is from current documentation, which is not this
> project's version — record the resulting facts as
> `⟨verification required: what and how⟩` rather than treating them as answers.

Register both servers. The latest endpoint stays useful for reading about a
version the project might move to; the pinned one is what implementation is
written against.

## `microsoft-learn`

Endpoint: `https://learn.microsoft.com/api/mcp`  (Streamable HTTP)

Use it for: ASP.NET Core hosting, routing, MVC and Razor Pages, dependency
injection, configuration, static files, logging, authentication and
authorization, testing, C# and .NET, and Entity Framework Core.

## Not this source

- **Do not answer a DevExpress API question from `microsoft-learn`.** It will
  answer — fluently, about the framework underneath — and the answer will read as
  if it addressed the question. Routing a question to the wrong server does not
  produce an error. It produces a confident answer about a different technology,
  which is worse.
- **Do not answer a DevExpress API question from memory.** Component names,
  property names, tag helper names and registration calls are version-sensitive
  and all of them look plausible when invented.
- Do not answer a plain ASP.NET Core question from `dxdocs`. Its corpus is the
  DevExpress documentation; a framework question there returns whichever
  DevExpress topic mentions the framework.
- Do not carry an answer about the server-side controls into a project using
  DevExtreme's client-side widgets, or the reverse.
- Do not carry a WinForms or WPF reporting answer into this web host. This stack
  covers web hosting of reports only.

## Priority

1. This project's code, project files and resolved package versions.
2. Deterministic build and test evidence, with exit codes.
3. `dxdocs` — pinned, on a v24.2 project — for DevExpress.
4. `microsoft-learn` for ASP.NET Core, EF Core and .NET.
5. Official release notes, for behaviour that changed between versions.
6. Model memory — never for a version-sensitive fact.

## Calling them at all

Registering a server does not make a model use it. The rule, which belongs in
the project's agent instructions and not only here:

- do not answer an API, version-behaviour or configuration question from
  training knowledge alone;
- **always call `devexpress_docs_search` before any `devexpress_docs_get_content`
  call.** This is the server's own rule, stated in both tool descriptions, not a
  preference of this kit: search returns snippets, and full content requires a
  follow-up call on a URL the search chose. Five snippets are a shortlist rather
  than an answer;
- **never construct a documentation URL from memory.** The `url` argument must
  come from a search result — "Do not construct URLs using your general
  knowledge", again the server's wording. An invented `docs.devexpress.com` URL is
  the same failure as an invented property name, with the added property that it
  can resolve to a real page about something else;
- pass the `technologies` enum value the question actually belongs to, and pass
  `XtraReports` alongside `AspNetCore` for anything about reporting;
- state which server answered, and the help topic URL. The URL is what makes the
  claim re-checkable, and it is what a later reader needs;
- never assume the documentation's default version matches this project's
  installed version;
- if the search found nothing, say so. Do not fill the gap from memory.

## Version-sensitive lookups

Always look up rather than recall:

- whether a component or a member exists in this project's version at all;
- the exact spelling of a property, a tag helper or a registration call;
- a default value, which is the thing most likely to have changed quietly;
- which of the two component lines a documented sample belongs to.

## Fallback

When the version in the project disagrees with the version a source describes,
**stop and report the mismatch**. Record it as
`⟨verification required: what and how⟩`.

## Before sending anything outward

These are **public, third-party endpoints**. A call sends the query, the tool
arguments the agent assembled, and whatever context it included. That can carry
private source, customer data, internal hostnames, credentials, unpublished
repository names, or raw operational logs.

This stack has two things worth naming specifically, because they are the ones
most likely to be pasted into a search: a **DevExpress licence key or feed
credential**, and a **report definition**, which commonly carries connection
details and column names from a real schema. Neither belongs in a query.

On a closed network, do not make these an operational dependency. Mirror the
documentation internally, index it, and serve an internal read-only MCP that
returns the topic, version and retrieval date with every answer. Use the public
endpoints for public technology research only.

## Connecting

`mcp-profile.json.example` next to this document holds exactly the servers in the
table. Copy it into the adapter configuration your agent reads:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | `.clinerules/` for rules; MCP is configured in the client |

Client field names differ — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. The
two values that matter are the transport and the URL.

Registering only the stacks a project actually uses reduces tool-routing errors
and unnecessary tool-schema context, so delete the entries for stacks this
project does not use — that is a normal edit, not a downgrade.

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

## What was run, and what is still open

This is the command that was run on 2026-08-06, and it is what the row above
records:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

Two things it did not settle. The pinned server, which has not been exercised at
all:

```bash
npx -y @modelcontextprotocol/inspector --cli "https://api.devexpress.com/mcp/docs?v=24.2" \
  --transport http --method tools/list --format json
```

And a real call, which is what separates `PASS` from "it connected". The
arguments are no longer an unknown — the measured schema fills them in:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/call --tool-name devexpress_docs_search \
  --tool-arg 'technologies=["AspNetCore","XtraReports"]' \
  --tool-arg "question=host the Web Document Viewer in an ASP.NET Core application" \
  --format json
```

Check in this order: exit code, whether the response parsed, the tool count,
whether the two documented tool names are present, then the call's exit code,
then the raw output. A tool name that has changed is a finding, not a detail: the
routing rules above name specific tools. So is a changed enum — the values in
this document are a measurement with a date on it, not a constant.

Record the outcome in `docs/core/mcp-source-verification.md`, in the same shape
as the fourteen endpoints already there — including a failure, which is more
useful than an absence.
