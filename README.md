# Evidence-First Agent Workflow

**English** | [한국어](README.ko.md)

> Your AI coding assistant says "Done!". This makes it prove it.

**Alpha.** Free to use, including commercially (MIT). Feedback welcome, never required.

---

## The problem

You ask an AI agent to add a feature. A few minutes later it reports:

> ✅ Done! I've added the user list screen, updated the API, and everything works.

Then you look, and one of these is true:

- it never ran the code;
- the screen it "built" is an empty page;
- it changed eleven files you didn't ask about;
- tomorrow, in a new chat, it has forgotten everything and rewrites what it already did.

The agent isn't lying on purpose. It just has no way to tell "I wrote plausible code" apart from "I verified this works" — and neither do you, without reading everything yourself.

**This project takes that judgement away from the model and gives it to programs that either exit 0 or don't.**

## What this actually is

A folder of Markdown files and small Python scripts that you **copy into your project**. There is nothing to install, no server, no subscription, no account.

Once the files are there, your agent reads them and follows them, because every coding agent already reads a file called `AGENTS.md` in your project root.

```text
your-project/
├─ AGENTS.md          ← the rules your agent reads first
├─ prompts/           ← the procedure it follows
├─ docs/              ← what your project is and what state it's in
├─ tools/             ← programs that check the work
└─ ... your actual code
```

That's it. It works with Codex, Claude Code, Cline, Roo Code, Zoo Code, and anything else that reads `AGENTS.md`.

## Start in three steps

**1. Copy the kit into your project.** Pick your language folder:

```bash
# English
cp -r Code-Agent-Kit/en/* your-project/
# 한국어
cp -r Code-Agent-Kit/ko/* your-project/
```

**2. Turn on the commit check.** One line, in your project (it must be a git repository):

```bash
git config core.hooksPath tools/enforce-agent-gates
```

You need **Python 3.11 or newer**, *or* **PowerShell**. Either one is enough — every
check ships twice, once in each language, and the commit check uses whichever it
finds. If you have neither, the check refuses the commit rather than waving it
through.

**3. Tell your agent:**

> Follow AGENTS.md. Add a user list screen.

That's the whole setup. The longer walkthrough — brand-new project versus existing project, Windows notes, and how to switch the check off when you need to — is in [`Code-Agent-Kit/en/QUICKSTART.md`](Code-Agent-Kit/en/QUICKSTART.md).

## What changes once it's on

Before, the agent goes straight to writing code. Now it has to fill in five headings before it can finish, and it can't rename or skip them:

| Heading | What the agent must write |
|---|---|
| **1. Analysis** | What is this project, what am I about to touch, what don't I know yet |
| **2. Task** | What "finished" means, and which files I expect to change |
| **3. Todo** | Small steps, each with how I'll check it |
| **4. Checklist** | Did I break anything else |
| **5. Verification** | The real command I ran, and its real exit code |

Then, when it tries to commit, a program checks the work:

```text
Evidence-First enforcement gate
  result         : BLOCKED
  FAIL  [enforce-agent-gates:worklog-missing] project source changed but no worklog was produced.
  FAIL  [enforce-agent-gates:current-not-updated] source changed but no feature '*.current.md' was updated.
```

The commit is refused. Not by the model — by a script, which cannot be talked out of it.

The bracketed name is deliberate. It's a permanent label for that one rule, so you
can search for it, and so the rule can be found again next year when the wording
around it has changed.

And this one matters more than it looks:

> A `PASS` written in the log with no command and no exit code beside it is recorded as `PENDING`, never as passed.

That single rule removes most of the fake "Done!".

## What you get

**Your agent stops forgetting.** The project's current state lives in files, not in the chat. Close the window, come back next week, use a different model — it picks up from the files.

**"Done" starts meaning something.** It means a command ran and returned 0. You can check that in a second instead of reading a diff.

**Small and cheap models become usable.** The procedure carries the judgement, so the model doesn't have to be brilliant — it has to follow steps. See [what it runs on](#what-it-runs-on) below.

**Review gets fast.** Every change arrives with why it was made, what was expected to change, and what was run to verify it.

**Nothing is locked in.** Swap the agent, swap the model, swap the tech stack. The rules don't care.

**It works on a closed network.** Nothing is sent anywhere by default, and the
knowledge lives in files you control. There *are* optional documentation servers you
can switch on (see below), and switching them on is a deliberate step precisely
because it sends your questions outside.

## Two things worth knowing before you start

### You don't need Python

Every check is written twice — once in Python, once in PowerShell — and the two are
proven to give the same answer. Not "should give" — a program runs both on the same
input, case by case, and fails if any single case disagrees.

Why bother: plenty of Windows machines have PowerShell and no Python, and on those
machines a Python-only check does nothing at all. Silently. A check that quietly does
nothing is worse than no check, because you think you have one.

So: Python 3.11+ **or** PowerShell. Either. With neither, the commit is refused
rather than passed.

### The agent can look things up instead of guessing

The most common way an AI gets a technical answer wrong is confidently remembering
the wrong version. So each stack says which documentation server to ask — Microsoft's
own for .NET, the project's own repository for Vue, Next.js, Node, Go, Rust, Elixir.
These are real, public, free, and no account is needed.

Fourteen of them were tested by actually connecting and asking a real question. What
that test did and did not prove is written down in
[`mcp-source-verification.md`](Code-Agent-Kit/en/docs/core/mcp-source-verification.md),
including the one that half worked and the one we decided not to recommend.

**They are off by default.** Each stack has an example config file; copying it is how
you say "I'm fine with these questions leaving my machine". On a closed network,
don't — mirror the documentation inside instead. That document explains how.

## What it costs you — read this part

This is a **slow, deliberate, paperwork-heavy** way to work. If that doesn't suit the job, don't use it.

**1. It is genuinely slower.** The agent reads state, writes a plan, works in small steps, and verifies before it can say it's finished. Reported on GPT-5.4 Mini: about 20 minutes for one user-management screen. If you want a throwaway prototype by lunchtime, this is the wrong tool.

**2. It uses more tokens.** Roughly 45K for one feature; a large screen used about 143K of a 258K context window. That is real money on a paid API.

**3. You will maintain documents.** Feature state files, work logs, a project map. They pay for themselves on a long project and are pure overhead on a two-day one.

**4. The check can be bypassed, and that's the real risk.** `git commit --no-verify` skips everything. It exists on purpose — you need it for the initial import and for emergencies. But if the check ever blocks something that was actually fine, people learn to type `--no-verify`, and then nothing is enforced at all. This is why the project treats a false alarm as more damaging than a missed defect, and why new checks must satisfy [Gate Design Principles](Code-Agent-Kit/en/docs/core/gate-design-principles.md) before they're allowed to block anything.

**5. A lot still cannot be checked by machine — and the docs say so.** "Did you actually read the state file first?" "Did you avoid guessing?" No program can tell. What's enforced is the *artifact* each rule should leave behind, so skipping leaves a trace. The [enforcement matrix](Code-Agent-Kit/en/docs/core/enforcement-matrix.md) lists honestly which rules are enforced and which are only advice.

**6. A green build still proves very little.** A project can compile perfectly and render a blank screen. The kit separates compile / rendered output / runtime behaviour / colour and accessibility, and makes you record each one separately. Expect to see `PENDING` a lot. `PENDING` is the honest answer, not a failure.

**7. There is a learning curve for you, not just the agent.** You need to understand roughly what the five headings are for. One read-through, but it isn't zero.

**8. Adding your own tech stack is real work.** See the next section. The kit deliberately refuses to guess your versions, conventions, and commands.

**9. It's alpha.** Twelve tech stacks ship, but only two are ready to use as-is.
The other ten come with the technology's own facts and traps written down, and wait
for your project's specifics. Expect rough edges and please report them.

## Adding your own tech stack

The rules in the middle are generic. What the kit **cannot** invent is your specifics: which framework version, which build command, which internal convention, which mistakes your team keeps making. Guessing those is exactly how an agent produces confident nonsense.

So a "stack pack" is a folder you fill in, and until it's filled in, the kit **blocks** work that depends on it.

### What ships now

| Stack | State | Meaning |
|---|---|---|
| React + ASP.NET Core | ready | filled in, use as-is |
| C# Windows Forms (.NET Framework 4.7.2+) | ready | filled in, use as-is |
| WPF, WCF, ASMX (.NET Framework) | blocked | half filled in — see below |
| Vue.js, Next.js, Node.js | blocked | half filled in |
| Go, Go + HTMX, Rust, Elixir | blocked | half filled in |

**"Blocked" is not "empty".** Each of those ten already contains the parts nobody
should have to write twice:

- the traps that bite everyone in that technology — the ones where nothing errors and
  you just get a wrong answer. WPF bindings fail silently. A `-Filter` typo in WCF
  quietly uses a different binding. Go before 1.22 captures loop variables in a way
  that changed;
- how to tell what your project actually uses, instead of guessing;
- which documentation server to ask, and which one to keep away from that question.

What's missing is only what nobody but you knows: your versions, your build command,
your database, your authentication. Until you answer those, the kit blocks work on
that stack — which is the point, not a bug.

### How to fill one in — ask the agent

You do not have to edit files by hand. Ten stacks are half done; tell the agent
which one:

```text
Follow prompts/8-fill-stack.md. Fill in the vue stack.
```

It reads your manifests and lock files to work out what it can, asks you only what
it cannot read, writes both of the stack's files, then runs the checker and shows
you what it said. It is not allowed to fill anything in from memory — if it can't
read it and you haven't said it, the row stays blank and the stack stays blocked.
That is the correct outcome, not a failure.

### Doing it by hand

```bash
# 1. copy the blank form
cp -r stacks/_template stacks/my-stack

# 2. fill it in (you can have the agent draft most of it)

# 3. ask the kit if it's ready
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/my-stack
```

That last command answers with one of three words:

- **ready** — everything required is filled in and has evidence behind it;
- **provisional** — usable, but something optional is still unknown;
- **blocked** — something required is missing, so dependent work is refused.

**Two files, and they must agree.** A stack has a table you read
(`STACK-INPUTS.md`) and a manifest the checker reads (`STACK-READINESS.json`). They
are compared. If you fill in one and forget the other, the stack fails and the
message tells you which is behind — that is deliberate, because the old behaviour
was to keep saying `blocked` without ever saying why. The interview prompt keeps
them in step for you.

**"Evidence" means a file that exists.** When you write down what proves a fact, the
checker goes and looks for it. A path that isn't there doesn't count. This used to be
otherwise, and a stack could claim `ready` while pointing at files that had never
existed — so the claim was worth nothing. Now it's checked.

You supply the decisions only you know: versions, build and test commands, naming rules, whether there's a database, whether there's authentication. The agent can draft the rest — but it must cite a source for each fact, and anything it can't confirm gets marked `⟨verification required⟩` instead of guessed.

Step-by-step guide with copy-paste prompts: [Using another stack](Code-Agent-Kit/en/docs/getting-started/using-another-stack.md).

### A worked example worth reading

The **C# Windows Forms** pack exists partly as a teaching case. Windows Forms has no web page to inspect, so the usual "did the screen actually render" check has nothing to look at. Rather than quietly drop that check, the pack reads the form's designer file and compares the controls it declares against a specification written *before* the code existed. If your stack also has no inspectable output, [read how that was solved](Code-Agent-Kit/en/stacks/csharp-winforms/references/ui-evidence-contract.md).

## What it runs on

Model-agnostic by design. Reported by the maintainer:

| Where | Models used |
|---|---|
| Public release (React + ASP.NET Core sample) | Claude Haiku, GPT-5.4 mini |
| Original internal version | Claude Opus 4.8, Claude Sonnet 5, Claude Haiku, GLM 5.2, Qwen3.6 35B-A3B |

### Running on a small local machine

The whole point of the procedure is that the *process* carries the judgement, so the model doesn't have to be large. That was tested, lightly:

| | |
|---|---|
| Agent | Pi Agent |
| Model | Qwen3.6 35B A3B Compact (local) |
| Machine | Laptop, **6 GB VRAM**, 32 GB RAM |
| Result | Completed a feature end to end, with human intervention |
| Speed | Started around **45 tokens/second**, dropped to roughly **21 tokens/second** as the context grew |

**Read the caveats, they matter:**

- This was a **light test**, not a benchmark. Nothing was measured under controlled conditions.
- It ran on the **original internal version**, not this public release. The public kit has not been tested at this configuration yet.
- **A human had to step in.** The interventions were about the private stack's server-call convention and a client-side display detail — not about the workflow itself. The feature was implemented.
- **It is slow.** 21 tokens/second on a long context is slow enough that you will feel it. That is the honest trade for running on 6 GB of VRAM.

If you try it on modest hardware, please [tell us how it went](ADOPTION.md) — including if it went badly. Failed reports are more useful than successful ones.

## Where to go next

| If you want to | Read |
|---|---|
| Just start | [QUICKSTART.md](QUICKSTART.md) |
| See the full feature list and structure | [OVERVIEW.md](OVERVIEW.md) |
| Understand *why* it's built this way | [DESIGN-CONCEPTS.md](DESIGN-CONCEPTS.md) |
| Check the commit gate really blocks | [gate-test-guide.md](gate-test-guide.md) |
| Add your own stack | [Using another stack](Code-Agent-Kit/en/docs/getting-started/using-another-stack.md) |
| See what's enforced and what isn't | [Enforcement matrix](Code-Agent-Kit/en/docs/core/enforcement-matrix.md) |
| Know which documentation servers are trusted, and why | [MCP source verification](Code-Agent-Kit/en/docs/core/mcp-source-verification.md) |
| Write a new check without breaking the others | [Gate design principles](Code-Agent-Kit/en/docs/core/gate-design-principles.md) |
| Read it as a human, not as an agent | [Developer guide](Code-Agent-Kit/en/docs/human/developer-guide.md) |
| Report how it went | [ADOPTION.md](ADOPTION.md) |
| Contribute | [CONTRIBUTING.md](CONTRIBUTING.md) |

## Status and licence

**Alpha.** Public evaluation is encouraged. This project does **not** claim fully autonomous development, and does not claim the same quality from every model.

Released under the **MIT License** ([LICENSE](LICENSE)) — free for commercial and closed-source use, keep the copyright notice. Feedback is welcome but is not a licence condition.
