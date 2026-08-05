# Stack Profile — Elixir

Elixir applications, typically Phoenix. Process and supervision structure is part of the design, not an implementation detail.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `mix.exs` — application, Elixir requirement, dependencies, and the release configuration.
- `mix.lock` — the authority on resolved versions.
- `lib/<app>/` and `lib/<app>_web/` — the Phoenix convention separating domain from web.
- `config/*.exs` — compile-time and runtime configuration are different files and differ in what they may read.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- Elixir, OTP, Phoenix and LiveView versions are four separate constraints and are not implied by each other.
- `config/runtime.exs` runs at boot; the other config files run at compile time and cannot read runtime environment.
- LiveView state lives in the socket on the server. Every assign is memory held for the session's lifetime.
- Supervision strategy determines what a crash takes down. It is a design decision with observable behaviour.
- An umbrella project and a single application differ in dependency resolution and release layout.
