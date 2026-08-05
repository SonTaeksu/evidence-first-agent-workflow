# Stack Profile — Rust

Services and tools in Rust with Cargo. The async runtime and the error model are load-bearing choices that pervade the code.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `Cargo.toml` — edition, `rust-version` (MSRV), features and workspace members.
- `Cargo.lock` — the only authority on resolved versions for a binary.
- `src/lib.rs` / `src/main.rs` — the crate roots.
- `tests/` — integration tests, compiled as separate crates.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- The edition changes language rules; `rust-version` states the minimum compiler. Both are contracts and neither is the installed toolchain.
- The async runtime is not an implementation detail: spawning, timers and IO types come from it, and two runtimes cannot generally be mixed.
- Cargo unifies features across a workspace, so enabling a feature in one member can change what another member compiles.
- `Send`/`Sync` bounds propagate through the call graph; one non-`Send` value can make a whole spawn impossible.
