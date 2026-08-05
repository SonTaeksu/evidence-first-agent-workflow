# Stack-Specific Agent Rules — Vue.js

This file extends root `AGENTS.md`. It does not repeat it.

- Read `STACK-READINESS.json` before any stack-dependent implementation.
- A blocking capability with status `unknown` prohibits the dependent pattern.
  Not "proceed carefully" — prohibits.
- Route documentation lookups through `mcp/source-routing.md`. `context7` is
  authoritative for this stack; `microsoft-learn` is not, for the reason stated there.
- Use `references/verified-facts.md` and `references/pitfalls.md` instead of
  recall. Every entry there names where it was verified.
- Record every selected capability in the Project Map and repeat it in Gate
  Analysis.

## Stack prohibitions

- Do not state a version-sensitive fact from memory. Do not answer Vue questions from Microsoft Learn. Do not carry Vue 2 answers into a Vue 3 project or the reverse — the reactivity system differs.
- Do not report a validation as passed without the command and its exit code.
- Do not fill a row of `STACK-INPUTS.md` on the owner's behalf. An unanswered
  input is a blocked stack, which is a correct state.
