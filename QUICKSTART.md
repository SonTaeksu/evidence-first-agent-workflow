# Quickstart

**English** | [한국어](QUICKSTART.ko.md)

> Not sure what this project is yet? Read [README.md](README.md) first — it takes two minutes.

## Pick a folder

The kit ships as **two independent folders**. Pick your language and use that one. Everything is inside it: the rules, the procedure, the checks, the sample. You never need the other folder.

| Language | Folder | Detailed walkthrough |
|---|---|---|
| English | [`Code-Agent-Kit/en/`](Code-Agent-Kit/en/) | [`Code-Agent-Kit/en/QUICKSTART.md`](Code-Agent-Kit/en/QUICKSTART.md) |
| 한국어 | [`Code-Agent-Kit/ko/`](Code-Agent-Kit/ko/) | [`Code-Agent-Kit/ko/QUICKSTART.md`](Code-Agent-Kit/ko/QUICKSTART.md) |

## Three steps

**1. Copy the folder contents into your project.**

```bash
cp -r Code-Agent-Kit/en/* your-project/
```

**2. Turn on the commit check.** Your project must be a git repository.

```bash
cd your-project
git config core.hooksPath tools/enforce-agent-gates
```

You need **Python 3.11 or newer**, *or* **PowerShell** — either one. Every check
exists in both languages and the hook uses whichever it finds. With neither, it
refuses the commit instead of letting it through.

**3. Tell your agent what to do.**

> Follow AGENTS.md. Add a user list screen.

## Then what?

The agent writes a plan before it writes code, works in small steps, and records the command it ran to verify each one. When it tries to commit without that record, the commit is refused.

Seeing that refusal once is worth the five minutes — it's how you start trusting it. Follow [gate-test-guide.md](gate-test-guide.md).

## Two things that will come up

**"The check is blocking my first commit."** Expected, when you import an existing codebase. There is no work log for code that already existed. Use `git commit --no-verify` for that one import, then leave the check on.

**"How do I add my own tech stack?"** Twelve stacks already ship — check
`stacks/` first, because yours may be half done already. Otherwise copy
`stacks/_template`, fill it in, and ask the kit whether it's ready. The [README section on stacks](README.md) covers it; [Using another stack](Code-Agent-Kit/en/docs/getting-started/using-another-stack.md) is the full guide with copy-paste prompts.

## The longer walkthrough

Each folder's own `QUICKSTART.md` covers what this page doesn't: setting up a brand-new project versus an existing one, the Windows first run, what a verification record actually looks like, and when bypassing the check is the right call.

For the big picture see [README.md](README.md), for the full reference [OVERVIEW.md](OVERVIEW.md), and for why it is built this way [DESIGN-CONCEPTS.md](DESIGN-CONCEPTS.md).
