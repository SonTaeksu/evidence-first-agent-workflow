# Quickstart

This repository ships the kit as **two independent, copyable folders**. Pick your
language and use that folder — everything (rules, prompts, tools, gate, sample) is inside it.

| Language | Folder | Start file |
|---|---|---|
| English | [`Code-Agent-Kit/en/`](Code-Agent-Kit/en/) | [`Code-Agent-Kit/en/QUICKSTART.md`](Code-Agent-Kit/en/QUICKSTART.md) |
| 한국어 | [`Code-Agent-Kit/ko/`](Code-Agent-Kit/ko/) | [`Code-Agent-Kit/ko/QUICKSTART.md`](Code-Agent-Kit/ko/QUICKSTART.md) |

## In short

1. Copy the contents of `Code-Agent-Kit/en` (or `ko`) into your project.
2. In your project (a git repo), turn on the commit gate — one line, no script:
   `git config core.hooksPath tools/enforce-agent-gates`
3. Tell your AI agent: **"Follow AGENTS.md. Add `<your feature>`."**

The full walkthrough — **first-time project setup (new vs. existing project)**, **Windows first run**, what verification looks like, and **how to bypass the gate** (`git commit --no-verify`) — is in each folder's own `QUICKSTART.md`.
For the big picture, see [README.md](README.md) and [DESIGN-CONCEPTS.md](DESIGN-CONCEPTS.md).
