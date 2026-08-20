# Evidence Provenance — DevExpress for ASP.NET Core

Every fact used in this stack has to be attributable. The order below is by how
much a claim can be trusted.

1. **This project's code, project files and restore output.** The resolved
   package version, not the range in the project file.
2. **A command's exit code**, with the command recorded and the machine it ran on.
3. **`dxdocs` through MCP**, for anything about DevExpress components or
   reporting. On a v24.2 project use the pinned server rather than the latest
   endpoint; `mcp/source-routing.md` says why.
4. **`microsoft-learn` through MCP**, for ASP.NET Core, EF Core and .NET — and
   for nothing DevExpress.
5. **Official release notes**, for a behaviour that changed between versions.
6. **Model memory** — last, and never for a version-sensitive fact.

The split between 3 and 4 is not a preference. A DevExpress question answered
from Microsoft Learn produces a fluent answer about the framework underneath,
which reads as if it addressed the question and does not.

## Recording a fact

An entry in `references/verified-facts.md` states the fact, where it was
verified, and when. An entry with no source is a memory, and is removed rather
than kept.

For a DevExpress fact, the source is the help topic — record the URL, since
`devexpress_docs_get_content` takes one and a later reader can re-fetch the
identical page. Record the version the topic described, because that is the
thing most likely to differ from this project.

## When sources disagree

Stop and report the disagreement. Do not implement against whichever version the
documentation happened to show. Record the unresolved item as
`⟨verification required: what and how⟩`.

The specific disagreement to expect here is between the documentation's current
version and this project's pinned version. The endpoint can be pinned, but only
for v24.2 and later — so on an older project there is no pinned source to
compare against, and every version-sensitive answer stays unresolved rather than
becoming approximate.
