# Claude Code Adapter

@AGENTS.md

The `AGENTS.md` content imported above is the **binding ruleset**; this adapter adds
nothing and does not redefine it. In particular: honesty over completion (report your
own mistakes, stop on uncertainty instead of guessing, "done" means verification passed),
and run every file-changing task through `prompts/GATE.md`.

A commit-time gate enforces this: a commit that changes project source without a worklog,
the five Gate sections, and state sync is **blocked** (see `docs/core/enforcement-matrix.md`).
Skipping the workflow is caught; it does not save time.

Routing: `prompts/0-sync-and-orient.md` → the matching situation prompt → the nearest
stack `SKILL.md` → project `.mcp.json`. Optional stance: `docs/persona.md`.
