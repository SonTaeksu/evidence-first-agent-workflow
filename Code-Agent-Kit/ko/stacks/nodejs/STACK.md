# Stack Profile — Node.js

Server-side or CLI JavaScript on Node. The module system is the first thing to establish and it changes the answer to most questions.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `package.json` — `type`, `engines`, `exports` and `scripts` are all contracts.
- `src/` or the `main`/`exports` entry — the module graph root.
- Lock file — the only authority on installed versions.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- `"type": "module"` switches the whole package to ESM. Without it, `.js` is CommonJS and `import` syntax is a parse error.
- `__dirname` and `__filename` do not exist in ESM; `import.meta.url` replaces them.
- Top-level `await` is available in ESM only.
- The `exports` field, once present, makes deep imports fail even when the file exists on disk.
- Behaviour on an unhandled promise rejection, and which APIs are stable, both depend on the major version. The `engines` field states an intent, not a fact.
