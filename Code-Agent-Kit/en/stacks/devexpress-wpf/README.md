# DevExpress WPF (v24.2+)

DevExpress WPF controls inside a WPF application, v24.2 or later.

**This profile is a companion to [`../csharp-wpf`](../csharp-wpf), not a
replacement for it.** Everything in that profile still holds: XAML compiles to
BAML, a failed binding throws nothing, the UI thread must be STA, and a
collection changed off the Dispatcher is a race rather than an exception. This
profile adds only what DevExpress changes on top of plain WPF and MVVM. Read
both. Where the two appear to disagree about a plain-WPF fact, `csharp-wpf` is
the one that is right — this document has no authority over the framework.

**Scope is v24.2 or later, and that boundary is not arbitrary.** The DevExpress
documentation MCP server supports version pinning no earlier than v24.2, so
below that line there is no documented way to make a lookup answer for the
version a project actually runs. A profile that cannot pin its own documentation
is a profile that answers from memory, which is the thing this kit exists to
stop.

**State: `blocked`.** Not broken — waiting. The owner inputs in
`STACK-INPUTS.md` are unanswered, so `check-stack-readiness` derives `blocked`,
and `tools/check-last` deliberately skips a stack in that state so a
placeholder does not produce a false alarm on every run.

What is already here and useful:

- `references/pitfalls.md` — failures in this stack that produce no error message;
- `capability-detection.md` — how to tell what this project actually uses;
- `mcp/source-routing.md` — which documentation source is authoritative, which
  must not be consulted, and what about the DevExpress server was *not* verified.

To reach `ready`, answer `STACK-INPUTS.md` with evidence that exists. Evidence is
measured, not declared:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
