# Capability Detection — Rust

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| edition-and-msrv | `edition` and `rust-version` in `Cargo.toml`, plus `rustc --version` | answer within them | confirm with the owner | block edition-sensitive constructs |
| async-runtime | the runtime crate in `Cargo.toml` and its attribute macros in the code | use it exclusively | confirm with the owner | block async work entirely |
| web-framework | a framework crate and its router wiring | use it | confirm with the owner | block introducing a framework |
| error-model | an error crate and the crate's public error type | follow it | confirm with the owner | block mixing error models |
| data-access | a driver or ORM crate and its migrations | use it | confirm with the owner | block data access invention |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
