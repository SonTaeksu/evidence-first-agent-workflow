# Quickstart

Impatient? This page is all you need. Deeper docs are optional.

## What this is, in one line

A rulebook + auto-checker that keeps an AI coding agent honest: it must read the
project map, work in clear steps, and **prove** the result — or its commit is blocked.

## The 30-second idea

- **Map, not guesswork** — the agent reads `docs/project-map.md` and the feature's `current.md` before touching code.
- **Steps, not vibes** — every task runs the 5-stage Gate (Analysis → Task → Todo → Checklist → Verification).
- **Proof, not promises** — a git commit gate refuses source changes that lack a worklog and state updates.

## Set it up

1. Copy the **contents of this folder** into your project root.
2. Make sure the project is a **git repository**, and that you have **either**:
   - **Python 3.11 or newer** (`python --version`) — this is the supported floor.
     3.11 is where `tomllib` entered the standard library, and one check reads
     Codex's TOML adapter config. No third-party TOML parser is vendored; a tool
     that needs it says so and exits 1 rather than crashing.
   - **or PowerShell** (`pwsh` 7, or Windows PowerShell 5.1) and no Python at all.
     Every check ships a PowerShell twin whose verdict is proven equal to the
     Python original, and the commit hook falls back to it. Four checks cannot be
     twinned and say so instead of pretending — see
     [`docs/core/finding-identifiers.md`](docs/core/finding-identifiers.md).
3. Turn on the commit gate — one line, no script needed:

   ```bash
   git config core.hooksPath tools/enforce-agent-gates
   ```

4. Do the one-time project setup below, then tell your agent: **"Follow AGENTS.md. Add `<your feature>`."**

## First run: point the kit at YOUR project (once)

The kit governs work through your project's **state docs** (`docs/project-map.md`,
`docs/features/<feature>.current.md`). A fresh project has none, so create them once —
otherwise the agent drifts to whatever state docs it can find (e.g. the bundled sample).

1. **Remove the demo if you don't want it.** This kit ships a sample under
   `samples/react-aspnetcore-taskflow/` with its own state docs and a seeded
   "priority field" task. If you keep it, the agent may work on the **sample** instead of
   your app. Delete `samples/` for a real project (the `core` install mode omits it).
2. **Pick your path and run the bootstrap prompt** — tell the agent
   *"Follow AGENTS.md, then run `prompts/<file>`"*:
   - **New / empty project** → [`prompts/2-bootstrap-new-project.md`](prompts/2-bootstrap-new-project.md)
   - **Existing codebase** (already has a `.sln`, `package.json`, source, etc.) → [`prompts/1-analyze-existing-project.md`](prompts/1-analyze-existing-project.md)

   This creates `docs/project-map.md` + a feature `current.md` for **your** code and
   records the **stack decision** explicitly. (Either way you can init the git repo first
   — `git init` — or point the kit at an existing repo; both are fine.)
3. After that, every task just starts with [`prompts/0-sync-and-orient.md`](prompts/0-sync-and-orient.md),
   which the agent runs automatically when you say "Follow AGENTS.md".

> Rule of thumb: **has code already → `1-analyze-existing-project`. empty/scaffold → `2-bootstrap-new-project`.** Both end with state docs pointing at your code, not the sample's.

## Windows first run (verified)

On Windows the `.ps1`/`.sh` installers often fail (PowerShell script signing, or no WSL
`bash`). **Skip them — use the git one-liner in step 3 above.** The hook runs fine through
Git for Windows. A clean first run in PowerShell, from the project root:

```powershell
git init                                             # if not already a repo
git config core.hooksPath tools/enforce-agent-gates  # turn on the gate

# keep IDE/build junk out of git (fixes ".vs permission denied")
@'
bin/
obj/
.vs/
node_modules/
__pycache__/
*.pyc
'@ | Set-Content -Encoding UTF8 .gitignore

git add .
git commit -m "chore: initial import" --no-verify    # first import is not feature work
```

Also set your commit identity so a work email is not published:
`git config --global user.email "you@example.com"` (GitHub users can use their `@users.noreply.github.com` address).

## What verification looks like

"Done" = the deterministic gates passed, cited with **real commands and exit codes** —
never a self-reported "PASS". For the React + ASP.NET Core stack a full run is, e.g.:

```
dotnet test                          # backend
npm run test                         # frontend unit
npm run build                        # frontend build
npm run e2e                          # browser E2E
npm run color:static / e2e:color     # color fidelity vs the reference screenshot
```

Each is recorded in the worklog §5 with its exit code. A PASS with no cited command/exit
is treated as `PENDING`, and the commit gate rejects it. Long-running servers are started
and stopped with `tools/run-managed-service/run_service.py` (never bulk-kill `node`).
Other stacks fill their own commands in `stacks/<stack>/validation/`.

## Skipping the gate (bypass)

The gate is a git pre-commit hook, so git's override applies:

```bash
git commit -m "..." --no-verify
```

`--no-verify` skips the hook for **that one commit**. Use it sparingly: the initial import,
an urgent hotfix you will regularize immediately, or a commit the gate misreads. It is an
explicit, visible choice; if CI is wired, the same checks still run on the pull request. To
turn the gate off entirely (not recommended): `git config --unset core.hooksPath`.

## What you'll see

- A **worklog** in `docs/worklogs/` with the 5 stages and evidence.
- Your **code change** plus updated `current.md` / `history.md`.
- If the agent skipped the work, the commit stops with `result: BLOCKED` and a `FAIL` reason.

## FAQ

- **Do I read all the docs?** No. This page + "Follow AGENTS.md" is enough.
- **Commit got blocked — broken?** No. A step was skipped. Tell the agent "You were blocked by the gate — do the workflow and fix it."
- **Publishing publicly?** Run `python tools/check-sanitization/check_sanitization.py --root .` first.

Using a stack other than React + ASP.NET Core? See [`docs/getting-started/using-another-stack.md`](docs/getting-started/using-another-stack.md).

More: `README.md`, `AGENTS.md`, `prompts/GATE.md`, `docs/persona.md`, `docs/core/command-and-process-safety.md`, `docs/core/enforcement-matrix.md`.
