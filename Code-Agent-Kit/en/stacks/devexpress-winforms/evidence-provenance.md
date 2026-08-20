# Evidence Provenance — DevExpress WinForms

Every fact used in this stack has to be attributable. The order below is by how
much a claim can be trusted.

1. **This project's code, project files and package or lock files.** The resolved
   DevExpress version, not the referenced range.
2. **A command's exit code**, with the command recorded and the machine it ran on
   — and for this stack, *which* machine, because the licence differs between a
   developer box and a build agent.
3. **`dxdocs24_2` (or `dxdocs`) through MCP**, for anything about a DevExpress
   type. Always, including for things that feel obvious.
4. **`microsoft-learn` through MCP**, for the Windows Forms and .NET layer
   underneath — and for nothing DevExpress.
5. **Official DevExpress release notes**, for a behaviour that changed between
   versions.
6. **Model memory** — last, and never for a version-sensitive fact or a member
   name.

## The version the answer came from is part of the answer

A DevExpress fact without a version is not a fact. Record the release the lookup
was pinned to alongside the claim; an answer from the unpinned endpoint on a
pinned project is recorded as such, because that is the case most likely to be
wrong later.

## Recording a fact

An entry in `references/verified-facts.md` states the fact, where it was verified,
and when. An entry with no source is a memory, and is removed rather than kept.

## When sources disagree

Stop and report the disagreement. Do not implement against whichever version the
documentation happened to show, and do not resolve a conflict between two
descriptions of the same server by choosing the more detailed one — see the tool
parameters in `mcp/source-routing.md` for a worked example of that mistake being
declined. Record the unresolved item as `⟨verification required: what and how⟩`.
