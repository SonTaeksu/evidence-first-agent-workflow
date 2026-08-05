# Stack Profile — Go

Services and command-line tools in Go, using the standard toolchain.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `go.mod` — module path and the `go` directive. Both are contracts.
- `cmd/*` — one directory per binary, by convention.
- `internal/*` — importable only within this module; the compiler enforces it.
- `*_test.go` — the standard test tooling; no runner needs to be chosen.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- The `go` directive in `go.mod` selects language semantics, and one of those semantics changed observably at 1.22 (loop variable scope).
- `internal/` is a compiler-enforced boundary, not a convention.
- Build tags and `GOOS`/`GOARCH` produce different compilation units; a file can be excluded from the build and never checked.
- An interface value holding a nil pointer is not nil. This is a language rule, not a bug.
