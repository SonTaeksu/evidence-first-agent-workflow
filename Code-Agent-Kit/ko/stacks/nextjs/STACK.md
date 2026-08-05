# Stack Profile — Next.js

React application on Next.js. The router mode and the server/client boundary govern almost every answer.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `app/` or `pages/` — which one exists decides the routing and data model. Both can exist; then per-route behaviour differs.
- `app/**/layout.*`, `page.*`, `route.*` — App Router segment files, each with distinct rules.
- `next.config.*` — output mode, redirects, image and bundler configuration.
- `middleware.*` — runs in a restricted runtime with a smaller API surface than Node.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- Server components are the default in the App Router; `'use client'` marks a boundary, and everything below it is client code.
- Props crossing a server-to-client boundary must be serializable. A function or a class instance fails at render.
- Caching and revalidation defaults have changed across major versions. The installed version is the authority; do not recall them.
- Only `NEXT_PUBLIC_`-prefixed environment variables reach the browser. Others are undefined there, not empty.
- `output: 'export'` removes server features entirely; code that works in development fails at export.
