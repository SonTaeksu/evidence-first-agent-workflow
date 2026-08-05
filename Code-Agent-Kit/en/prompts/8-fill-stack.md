# Fill in a stack — interview

Use this when a stack is `blocked` and you want to unblock it, or when you are
adding a new one. You answer questions; the agent does the reading, the writing and
the checking.

Ten stacks ship half-filled. They already contain that technology's constraints, its
silent-failure traps, how to detect what a project uses, and which documentation
server to ask. What is missing is only what nobody but you knows.

## Say this

> Follow `prompts/8-fill-stack.md`. Fill in the `vue` stack.

Substitute the directory name under `stacks/`.

---

## Rules for the agent

These are the point of the prompt. Everything else is procedure.

1. **Detect before asking.** Most answers are already in the repository. Read them.
   Every value you write must name the file you read it from, and that file must
   exist — `check-stack-readiness` resolves evidence paths, so an invented path is
   worse than a blank.
2. **Never fill a row from memory.** Not the version, not the command, not the
   framework. If you cannot read it and the user has not said it, the row stays
   `unknown`. A blocked stack is a correct state; a stack that claims `ready` on a
   guess is a lie the tooling will now catch.
3. **Ask in small batches.** Three or four questions, then write what you learned,
   then ask again. Do not produce a thirty-question form.
4. **Write both files together.** `STACK-INPUTS.md` is what a person reads;
   `STACK-READINESS.json` is what the checker reads. They are compared and a
   disagreement makes the stack fail. Never update one alone.
5. **Report the checker's verdict; never state it yourself.** Run it, paste what it
   said, and if it is still `blocked` say which rows are outstanding.

---

## Step 1 — read the stack, and say what is already known

```bash
cat stacks/<name>/STACK.md
cat stacks/<name>/STACK-INPUTS.md
cat stacks/<name>/capability-detection.md
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

`capability-detection.md` is the important one: it tells you *how* to detect each
capability from the repository. Follow it rather than guessing.

Report back:

- which rows are `unknown`;
- which of them you think you can detect, and from which file;
- which ones only the user can answer.

## Step 2 — detect what you can

Read the project. What to look at, by stack family:

| Stack | Read |
|---|---|
| WPF, WCF, ASMX | `*.csproj` (`TargetFramework` / `TargetFrameworkVersion`), `App.config` / `Web.config`, `packages.config` or `PackageReference` |
| Vue, Next.js, Node.js | `package.json` **and the lock file** — the lock file is the authority; `package.json` may name a range |
| Go, Go + HTMX | `go.mod` (module path and the `go` directive), and `go version` on the machine that will run validation |
| Rust | `Cargo.toml` (`edition`, `rust-version`), `Cargo.lock`, and `rustc --version` |
| Elixir | `mix.exs`, `mix.lock`, and `elixir --version` plus the OTP release |

Also look for: a test directory or test script, a lint configuration, a CI
workflow — those usually answer the validation questions without asking.

For each thing you found, record the **file path you read it from**. That path
becomes the evidence, and it has to exist.

## Step 3 — ask only what is left

Typically these, and they are genuinely yours to answer:

- **What counts as one feature here?** What may a single feature touch, and what is
  shared?
- **The exact build and test commands**, and what failure looks like. A command
  nobody has run is not a validation profile.
- **Data access and authentication** — which library, which pattern, or none.
- **Deployment** — what the build has to produce and where it goes.
- **Confidentiality** — may this stack's material appear in a public repository?

Ask three or four at a time. If the user says "I don't know", the row stays
`unknown` and the stack stays blocked. That is a correct outcome, not a failure of
the interview.

## Step 4 — write both files

In `STACK-INPUTS.md`, fill the `Value or Path`, `Evidence` and `Status` cells. Leave
the `Key` column alone — it is what joins this table to the manifest.

In `STACK-READINESS.json`, set the matching `status` and `evidence` for the same key:

```json
{
  "key": "runtime-sdk-versions",
  "required": true,
  "source": "auto",
  "status": "detected",
  "evidence": ["frontend/package.json", "frontend/package-lock.json"],
  "notes": "Read from the lock file, not the range in package.json."
}
```

Status values, and there are only these:

| Value | Means |
|---|---|
| `detected` | read from a file, and the file is named in `evidence` |
| `confirmed` | the user stated it, and `evidence` names where it is written down |
| `not-applicable` | genuinely does not apply here — say why in `notes` |
| `unknown` | not established. The honest default |

For capabilities, `present` and `absent` both need `evidence` **and** a
`selected_path`. Proving something *absent* does not need prose: record the search
in `capability-detection.md` and cite that file.

Do not touch `declared_state` yet.

## Step 5 — let the checker decide the state

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

It prints `READY`, `PROVISIONAL` or `BLOCKED`. Set `declared_state` to **what it
printed**, then run it once more — it also checks that the declaration matches what
it derives, so a wrong guess here fails immediately.

Paste the output into the reply. If it is blocked, list the outstanding rows and
stop. Do not adjust anything to make the verdict nicer.

## Step 6 — record it

- add the stack to `docs/project-map.md` under the environment section;
- if this was part of a feature, name the stack in the worklog's Analysis section
  along with each capability decision you took.

---

## What the checker will tell you off for

| Finding | What happened |
|---|---|
| `input-unresolved` | a required row is still `unknown` |
| `input-without-evidence` | a status says resolved but `evidence` is empty |
| `evidence-not-found` | none of the cited paths exist. This is the forgery guard |
| `inputs-document-drift` | the table and the manifest disagree. Update whichever is behind |
| `declared-state-mismatch` | `declared_state` is not what the tool derives |
| `capability-without-path` | a capability is `present` with no `selected_path` |

Every one of them names the row. None of them requires guessing what went wrong.

## Where the documentation lookups go

`stacks/<name>/mcp/source-routing.md` names the server that is authoritative for
this stack and the one that is not, with the tool names each actually exposed when
it was tested. Those servers are **off by default** — see
[`docs/core/mcp-source-verification.md`](../docs/core/mcp-source-verification.md)
before switching any on, especially on a closed network.
