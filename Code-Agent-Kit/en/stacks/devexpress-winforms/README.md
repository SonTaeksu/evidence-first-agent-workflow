# DevExpress WinForms

DevExpress controls on a Windows Forms desktop application, **v24.2 or later**.

## A companion to `csharp-winforms`, not a replacement

Everything in [`../csharp-winforms`](../csharp-winforms/) still holds. A
DevExpress form is a Windows Forms form: the designer owns the layout file,
controls belong to the thread that created them, DPI is configured where that
profile says it is, and the project format still decides the build command. Read
that profile first and keep it open.

This profile adds only what DevExpress changes on top — a control hierarchy where
behaviour and data live on different objects, a command surface that is not the
form's menu strip, a layout container that ignores coordinates, an
application-wide skin layer, a licence file, and a documentation source that
Microsoft Learn does not cover.

## Why v24.2 or later

The DevExpress documentation MCP server supports version pinning through a `?v=`
query parameter no earlier than **v24.2**. On an older release there is no
supported way to point the documentation server at the version the project
actually uses, so every control-API answer would come from whatever release is
current — which is the class of confident, version-shifted answer this kit exists
to prevent. The rules in this profile are still readable on an older project;
the evidence route is not available there.

## State: `blocked`

Not broken — waiting. The owner inputs in `STACK-INPUTS.md` are unanswered, so
`check-stack-readiness` derives `blocked`, and `tools/check-last` deliberately
skips a stack in that state so a placeholder does not produce a false alarm on
every run.

What is already here and useful:

- `mcp/source-routing.md` — the DevExpress documentation server, what is
  documented about it, and what was **not** verified in this environment;
- `references/pitfalls.md` — failures in this stack that produce no error message;
- `references/verified-facts.md` — the documented endpoint facts, with their date;
- `capability-detection.md` — how to tell what this project actually uses.

To reach `ready`, answer `STACK-INPUTS.md` with evidence that exists. Evidence is
measured, not declared:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
