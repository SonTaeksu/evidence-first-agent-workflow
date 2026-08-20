# Evidence Provenance — DevExpress WPF (v24.2+)

Every fact used in this stack has to be attributable. The order below is by how
much a claim can be trusted.

1. **This project's code and manifests.** The resolved DevExpress version from the
   restore, not a version range and not what is installed on the machine.
2. **A command's exit code**, with the command recorded and the machine it ran on.
3. **`dxdocs` through MCP**, for anything DevExpress — pinned to the project's
   version where the project is on a pinnable release.
4. **`microsoft-learn` or `wpf-docs` through MCP**, for anything that is plain
   WPF, XAML or .NET. Never for a DevExpress control.
5. **Official release notes**, for a behaviour that changed between versions.
6. **Model memory** — last, and never for a DevExpress fact of any kind.

The demotion of memory is stricter here than in `../csharp-wpf`, and the reason is
specific: a recalled DevExpress member name usually still exists, so the code
compiles and the mistake survives review. A recalled WPF fact tends to fail
loudly. Compiling is not evidence.

## Recording a fact

An entry in `references/verified-facts.md` states the fact, where it was
verified, and when. A DevExpress entry also names the version it was verified
for, because that is the axis along which these facts change. An entry with no
source is a memory, and is removed rather than kept.

## When sources disagree

Stop and report the disagreement. Do not implement against whichever version the
documentation happened to show. Record the unresolved item as
`⟨verification required: what and how⟩`.
