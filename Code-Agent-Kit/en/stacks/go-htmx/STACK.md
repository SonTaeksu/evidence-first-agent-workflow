# Stack Profile — Go + HTMX

Server-rendered HTML in Go with HTMX for partial updates. Everything in the Go profile applies; this adds the fragment contract.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- Templates — a full-page set and a fragment set. Which one a handler returns is the core decision.
- Handlers — one route may return either a page or a fragment depending on the request.
- Static assets — the HTMX script itself, with a pinned version.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- Everything in the Go stack profile applies unchanged, including the `go` directive rule.
- A handler must decide page versus fragment. The `HX-Request` header is how HTMX identifies itself.
- The swap target is named by the client. A target that does not match anything results in **no change and no error**.
- `html/template` escapes by context; escaping is not optional and changes what a fragment may contain.
