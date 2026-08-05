# Stack Profile — Vue.js

Single-page or embedded UI on Vue. The major version is a hard boundary.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `src/main.*` — application entry and plugin registration.
- `src/components/*.vue` — single-file components: template, script, style.
- `src/router`, `src/stores` — present only if the corresponding capability is present.
- `vite.config.*` or the configured bundler's config — the build contract.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- Vue 2 and Vue 3 differ in reactivity implementation, component API and template rules. The major version governs every answer.
- Vue 3 reactivity is Proxy-based, so it tracks property access on the proxy object; a value pulled out of the proxy is no longer reactive.
- `<script setup>` compiles differently from `setup()` — bindings are exposed automatically and the file has different top-level rules.
- Scoped styles are compiled to attribute selectors; they do not isolate child component internals.
