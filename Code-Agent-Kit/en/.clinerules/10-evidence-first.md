# Cline Adapter — binding rules

Cline auto-loads this file. The full, binding ruleset is `AGENTS.md` in the project root — read it and follow it; this adapter does not replace it. Non-negotiables, always in effect:

- Honesty over completion: report your own mistakes, stop on uncertainty instead of guessing, treat "done" as "passed verification".
- Run every file-changing task through the five-stage Gate in `prompts/GATE.md`; start from `prompts/0-sync-and-orient.md`.
- A commit-time gate blocks source changes lacking a worklog, the Gate sections, and state sync (`docs/core/enforcement-matrix.md`). Skipping the workflow is caught, not saved time.

Use `prompts/`, the active feature `current.md`/worklog, and the nearest stack `SKILL.md`.
