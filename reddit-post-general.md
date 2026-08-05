<!-- Revision 2 — 2026-08-04, aligned with v0.1.9-alpha. Previous revision: v0.1.8-alpha. -->

TITLE (pick one):
1) Can we actually trust an AI coding agent? Here's a workflow I built to try (MIT, alpha)
2) I got tired of agents faking "done" — so I built a workflow that makes them work like a careful engineer (MIT, alpha)

---
[IMAGE 1 — HERO] TaskFlow public sample screenshot (the license-free React + ASP.NET Core sample UI).
Caption: "The public TaskFlow sample — built by GPT-5.4 mini running under this workflow."
---

*Updated 2026-08-04 for v0.1.9-alpha (previous version of this post covered v0.1.8-alpha): there are two filled-in stacks now, the kit started checking itself and immediately caught itself, and there's a run on a 6 GB VRAM laptop below.*

We've all seen it: you hand a task to an AI, and it skips the process, jumps straight to code, says "done" without ever running anything, and then "cleans up" by killing every process in sight. So I tried to build something that makes an AI behave more like a careful engineer. It's called **Evidence-First Agent Workflow**, and it's open source (MIT).

**The idea (it's simpler than it sounds).** It's less a tool and more a set of *working habits* you give the agent:

- **Read first, then touch.** Understand the project's state before editing anything.
- **Evidence, not claims.** Not "it works" — "I ran this command and here's the result."
- **Honesty over looking-done.** Stopping to ask beats wrapping something up plausibly.
- **Keep a memory.** Work logs and current state live in docs, so context survives even when a session ends.

There are automatic guards (a commit-time check and so on) that keep these habits from slipping, but those just play a supporting role — the real point is the way of working itself.

**What's nice about it**
1. **Great for long-lived projects** — it doesn't lose context across sessions, so you don't re-explain "what were we doing yesterday" every time.
2. **Works even on small / cheap LLMs** — the process carries the judgment, so you get usable results without a top-tier model. Saves money too.
3. **It self-evolves** — the more you use it, the more the accumulated logs sharpen the project's own rules.
4. **You can trust "done"** — faked completion gets blocked, so you spend less time re-checking its work.
5. **No lock-in** — not tied to one agent (Codex, Claude, Cline, Roo) or one tech stack. Swap freely.
6. **Easy to review and hand off** — every change comes with "why, what, and how it was verified."
7. **Consistent quality no matter who runs it** — same procedure whether it's a person or a model.
8. **Recoverable** — if the order gets tangled, there's a recovery path so work isn't lost.

**The downsides (being honest)** — this is definitely a *slow, hands-on* approach.
1. **Slow and heavy.** Following the whole procedure takes time. On ChatGPT 5.4 Mini, a user-management screen took ~20 min, and the TaskFlow sample ~18 min. Not for rapid prototyping.
2. **Token-hungry.** ~45K for one feature; a big screen (TaskFlow) used ~143K of a 258K window.
3. **Setup is a bit of a chore.** Hooks, folder structure, state docs — it's not "install and go."
4. **Adding a new stack is work.** You fill in verification commands yourself; there's a learning curve.
5. **You have to learn the concepts once.** The rules and terms need a read-through to run smoothly.
6. **The check is bypassable, and honestly that's the real risk.** `git commit --no-verify` skips the whole thing. That escape hatch is deliberate — you need it for the initial import and for emergencies. But the moment the check blocks something that was actually fine, people learn to type `--no-verify`, and after that nothing is enforced at all. Which is why the project treats a **false alarm as worse than a missed defect**: a check that cries wolf doesn't just fail once, it kills every check after it.
7. **A lot still can't be machine-checked, and the docs say which parts.** "Did you actually read the state file first?" "Did you stop instead of guessing?" No program can tell. What's enforced is the *artifact* each rule should leave behind, so skipping leaves a trace — but that's not the same thing. The enforcement matrix lists rule by rule what's enforced and what's only advice.
8. **Still alpha.** The public sample stack especially hasn't had much mileage, so expect bugs.

**Public vs. original (being upfront).** The core of this has actually been used on a real internal project — an enterprise web front-end stack. But that stack's UI framework and its communication layer **require commercial licenses**, so it can't be used as a public test stack. That's why the public release ships a **license-free React + ASP.NET Core sample** instead. "How can you open-source something you used at work?" — I **got permission from our CEO** and built a **separate public release** with all internal/proprietary bits stripped out. So the *method* is battle-tested; the *public sample stack* is new.

**Two filled-in stacks now — and the second one is the interesting part.** What ships ready to use is **React + ASP.NET Core** and **C# Windows Forms on .NET Framework 4.7.2+**. The Windows Forms pack exists partly as a teaching case. This workflow has a validation layer that asks "did the screen actually render" — on the web you open the rendered document and look. Windows Forms has no rendered document to look at. So the choice was to quietly drop that check for this stack, or replace it with something. Dropping it would have meant silently shipping a stack with a hole in it, so instead the pack **parses the form's designer file and compares the controls it declares against a screen specification written before the code existed**. The thing being inspected changed; the question — "did you build what you said you would" — didn't. If your stack also has no inspectable output, that's the pattern to steal.

**We wrote a check about ourselves and it immediately caught us.** New this release: the kit takes the templates its own docs tell you to copy, copies them exactly as instructed, and runs its own validator over the result. On the very first run that check found a real defect — the template folder the docs point you at was **missing a file its own manifest lists as required**. So anyone who followed the documented path hit a readiness failure they hadn't caused. It had been shipping broken. I'd rather not dress this up as a win; the accurate sentence is that we wrote a check about ourselves and got caught by it on day one. It's fixed, and the check that should have caught it now runs every time.

Worth saying plainly alongside that: of the four defects fixed this release, **two were found by a person reading, not by any program** — and those two still aren't machine-checkable. More automated checks didn't remove the need to read.

**Tested with**
- Public release (sample stack): Claude Haiku, GPT-5.4 mini, among others.
- Original internal version: Claude Opus 4.8, Sonnet 5, Haiku, GLM 5.2, Qwen3.6 35B-A3B.

Everything except Claude ran on **my own personal budget**, so Qwen3.6 27B eventually **got paused when I ran out of money.** I'm just a broke dad, honestly — barely keeping up with diaper money. 😅

**One low-spec run, since "small models are enough" is a claim that needs evidence.**
- **Agent:** Pi Agent. **Model:** Qwen3.6 35B A3B Compact, running locally.
- **Machine:** laptop, **6 GB VRAM**, 32 GB RAM.
- **Result:** completed a feature end to end, with human intervention.
- **Speed:** about **45 tokens/second** initially, dropping to roughly **21 tokens/second** as the context grew.

The caveats are the important half:
- It was a **light test, not a benchmark**. Nothing was measured under controlled conditions.
- It ran on the **original internal version, not the public release**. The public kit has not been tested at this configuration.
- **A human had to step in.** The interventions were about the private stack's server-call convention and a client-side display detail — not about the workflow itself. The feature was implemented.
- **It is slow.** 21 tokens/second on a long context is slow enough that you will feel it. That's the honest trade for 6 GB of VRAM.

---
[IMAGE 2 — OPTIONAL] Console screenshot of the gate rejecting a commit ("result: BLOCKED / FAIL [gate] ... no worklog").
Caption: "The automatic check blocking a change that skipped the workflow."
---

**To try it — what you need, and how**

Requirements depend a bit on the stack:
- **Git** — required (version control + the automatic checks hook in here).
- **Python** — to run the kit's check tools.
- **Node.js** — if you use the React (frontend) side.
- **.NET SDK** — if you use the ASP.NET Core (backend) side.

The flow is simple:
1. Clone the repo from GitHub.
2. Run the install script to drop the kit onto your project (`install-kit` — Windows / macOS / Linux versions included).
3. Open your coding agent (Codex, Claude, etc.) and give it the start prompt.
4. The workflow guides the rest — orient → plan → work → verify → record.

And you **don't have to use React and ASP.NET Core together** — the frontend (React) alone or the backend (ASP.NET Core) alone is fine. You only need the matching requirements.

**A couple of asks**
- **If you build a stack, please share it.** The filled-in public examples right now are React + ASP.NET Core and C# Windows Forms. I plan to add more (FastAPI, Express, plain static, etc.), and stacks you share via issues/PRs help everyone. **Duplicates of the same stack are very welcome too** — collecting overlapping ones lets us cross-check for consistency and makes the knowledge base sturdier.
- **If you have spare AI resources, a test environment would mean a lot.** As mentioned, my wallet can't run many models. If you can share compute or an environment for other models/agents, I'd be hugely grateful — and results/reports from other setups are always welcome.

What I'd love most: **failure reports** — "this didn't work for my stack/agent" — and honest pushback on the design.

Repo: https://github.com/SonTaeksu/evidence-first-agent-workflow
Start here: the one-page QUICKSTART in `Code-Agent-Kit/en` (or `ko`).

One heads-up: starting tomorrow I'm heading out to the countryside to spend time with my baby and my parents, so I'll be slow to respond for a while. I might get to things from next week, or check in from my phone here and there — my English isn't great, so I'll be leaning on a translator. Between the baby and work I might not manage to reply to everything, so thanks in advance for your patience. 🙏

(Self-promo: I'm the author. MIT-licensed, feedback-driven, still alpha.)
