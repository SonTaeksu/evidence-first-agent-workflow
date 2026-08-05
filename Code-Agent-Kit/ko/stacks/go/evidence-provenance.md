# Evidence Provenance — Go

Every fact used in this stack has to be attributable. The order below is by how
much a claim can be trusted.

1. **This project's code and manifests.** The lock file, not the version range.
2. **A command's exit code**, with the command recorded and the machine it ran on.
3. **`context7` through MCP**, for anything version-sensitive.
4. **Official release notes**, for a behaviour that changed between versions.
5. **Model memory** — last, and never for a version-sensitive fact.

## Recording a fact

An entry in `references/verified-facts.md` states the fact, where it was
verified, and when. An entry with no source is a memory, and is removed rather
than kept.

## When sources disagree

Stop and report the disagreement. Do not implement against whichever version the
documentation happened to show. Record the unresolved item as
`⟨verification required: what and how⟩`.
