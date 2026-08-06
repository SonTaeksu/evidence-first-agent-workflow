# Using another stack

React + ASP.NET Core is just the example that's already filled in. You don't have to use
it. The kit keeps one shared rulebook (the core) and swaps only the **stack pack** per
technology.

## Stacks you have now

| Stack | State | Meaning |
|---|---|---|
| `react-aspnetcore` | ready | fully filled in → use as-is |
| `csharp-winforms` | ready | fully filled in → use as-is (desktop, .NET Framework 4.7.2+) |
| ten more: `csharp-wpf`, `csharp-wcf`, `csharp-asmx`, `vue`, `nextjs`, `nodejs`, `go`, `go-htmx`, `rust`, `elixir` | blocked | half filled in → the technology's constraints, traps, capability detection and documentation routing are already there; your project's specifics are not |
| `_template` | — | the blank form you copy to make a new stack |

`csharp-winforms` is worth reading even if you don't use it: Windows Forms has no rendered
document, so it shows how a stack supplies the rendered-output layer when the usual route
doesn't exist — see its `references/ui-evidence-contract.md`.

Check a stack's state:

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

## Who does what (this is the key part)

**What you do**
1. Pick the stack you want.
2. If that stack is `blocked` (empty), fill in the info it needs — versions, run/build/test
   commands, conventions: the **decisions only you (or your team) know**.
3. When you start work, tell the agent once: **"use the `<stack>` stack (e.g. go-htmx)."**

**What the agent does automatically**
- Records your chosen stack in `docs/project-map.md` → **you don't edit that by hand.**
- Routes to that stack's `SKILL.md`, references, and validation profile from then on.
- If the stack is `blocked`, the gate stops it from building on an unready stack.

> So "telling the agent the stack" is not your homework — you just name it once.

## Where knowledge comes from (md file vs MCP)

Stack knowledge has two kinds of source, and **both count as "evidence"** — the only
question is when to use each.

- **Bundled md references** (`references/verified-facts.md`, `pitfalls.md`) — stable,
  in-house, version-pinned, or niche facts. Curated once; works offline / on a closed
  network; zero call cost. **First choice for stack-specific knowledge.**
- **MCP** (Context7, Microsoft Learn) — official-library facts that change. Query at work
  time, then keep only the **needed fact + its source** in a reference or the worklog
  (discard the full dump).
- **Model memory** — never for version/niche facts (last resort).

Whatever the source, **record where it came from** (claim, source, version, date —
`../../stacks/<stack>/evidence-provenance.md`). Which MCP to use for which topic lives in
the stack's `mcp/source-routing.md`; everything general — routing, fallback,
compacting results, connecting — is one page at `../mcp.md`.

Rule of thumb: **bake the stable, only-we-know facts into md; confirm changing official
facts via MCP at the moment, then summarize and keep the source.**

### How to designate a source (real examples)

**Designate an MCP — 2 steps.**
1. Register the MCP server in the project-root `.mcp.json` (Codex/Roo use `.codex/config.toml`, `.roo/mcp.json` too):

```json
{
  "mcpServers": {
    "microsoft-learn": { "type": "http", "url": "https://learn.microsoft.com/api/mcp" },
    "context7": { "type": "stdio", "command": "npx", "args": ["-y", "@upstash/context7-mcp"] }
  }
}
```

2. Say **which MCP for which topic** in the stack's `mcp/source-routing.md`:

```markdown
## ASP.NET Core · C# · .NET   -> use Microsoft Learn MCP
## React · JS libraries        -> use Context7 (pin core library: /facebook/react)
## Priority: code/validation > official MCP > official repos > model memory
```

**Designate an md source — write it in the files.**
Facts go in `references/verified-facts.md` as a **table** (with source, version, date):

```markdown
| Fact | Scope | Evidence | Last Verified |
|---|---|---|---|
| Sample uses React 19.2.7 | sample only | `package.json` | 2026-07-14 |
```

Pitfalls go in `references/pitfalls.md` (✗ common mistake -> ✓ this stack's way); screen/code skeletons go in `skeletons/`.

> So: **MCP = `.mcp.json` (connect) + `source-routing.md` (where to use it)**, **md = write directly under `references/`**. The agent reads both and picks the right one.

## The easy way: let the agent interview you

```text
Follow prompts/8-fill-stack.md. Fill in the vue stack.
```

The agent reads your manifests and lock files to detect what it can, asks you only
what it cannot read, writes **both** `STACK-INPUTS.md` and `STACK-READINESS.json`
together, then runs the checker and reports what it said. Editing the two files by
hand works too, and the rest of this page describes that — but they are compared
now, and a disagreement makes the stack fail, so keeping them in step by hand is
the part worth delegating.

## Filling a stack by hand (only when it's blocked or brand-new)

- **Existing half-filled stack** → fill the blank cells in that folder. Ten of them are waiting.
- **Brand-new stack (e.g. desktop or in-house UI)** → copy the form:
  `cp -r stacks/_template stacks/<your-stack>`

What to fill (you provide the decisions; you may have the agent draft from sources — but
only mark something "verified" when it's confirmed from evidence):
- `STACK-INPUTS.md` — versions, framework, run/build/test commands, conventions
- `references/`, `skeletons/` — from official docs and real code (not from memory)
- `validation/validation-profile.md` — verification commands (+ `run_service.py` for dev servers)

Then fill until `check-stack-readiness` reports **ready**, and that stack works just like
React + ASP.NET Core.

> Confirm the blank form itself still passes: `python tools/check-kit-selfcheck/check_kit_selfcheck.py --root .`
> A template that cannot pass the kit's own checks leaves you no exit but `--no-verify`.

## Filling it with AI (you don't hand-write everything)

You don't have to write an empty stack by hand. Let the agent draft it — **you give the
decisions, the agent drafts the content.** The kit's honesty rules still apply, so the
agent **cannot fill from memory** and must cite a source for each fact.

Who does what:
- **You provide** — the decisions only you know (versions to pin, in-house conventions,
  run/build/test commands, auth choice) + **point it at trustworthy sources** (official-doc
  MCP, the installed SDK path, existing working code, a reference repo).
- **The agent drafts** — `verified-facts` (with source, version, date), `pitfalls`
  (official docs + known gotchas), `skeletons` (**copied from real files**, not invented),
  `validation-profile` commands, `capability-detection`.
- **You confirm** — that each fact's source is real (not model memory), then run
  `check-stack-readiness` until it reports ready.

Example prompts (paste as-is):

```text
Fill stacks/<stack>/references/verified-facts.md.
For each fact, confirm it via Microsoft Learn / Context7 MCP, the installed SDK, or this
repo's code, and record Evidence + version + date in the table. Mark anything you cannot
confirm as ⟨verification required⟩ — do not guess.
```

```text
Create stacks/<stack>/skeletons/ by copying a minimal example from <real file path>. Do not write from memory.
```

```text
Fill stacks/<stack>/validation/validation-profile.md with this stack's real run/build/test
commands and their pass criteria (exit codes). Use run_service.py for long-running servers.
```

**Why this is safe** — `verified-facts` cannot have an empty Evidence cell (so it can't be
filled from memory), unconfirmed items become `⟨verification required⟩`, and skeletons are
copied from real files. So even AI-filled packs keep only sourced facts. A human confirms
with `check-stack-readiness` at the end.

Details: `stack-input-requirements.md`, `../core/stack-extension.md`.
