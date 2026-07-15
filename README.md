# Evidence-First Agent Workflow

**English** | [한국어](README.ko.md)

> **New here? Read [QUICKSTART.md](QUICKSTART.md) first — one page, a result in 3 steps.** This README is the full reference.

> A tool-agnostic context-management and development-governance workflow for small models, closed networks, long-lived projects, and stacks that require verified knowledge rather than inference.

## Status

**Alpha.** Public evaluation is encouraged. The repository does not claim fully autonomous development or universal model-independent quality.

## Two-part model

```text
Framework-agnostic governance core
+
Verified stack or organization knowledge pack
```

The core externalizes memory, routes context, forces a five-stage Gate, and delegates judgment to deterministic tools. A stack pack supplies the facts, skeletons, capabilities, contracts, and pitfalls the core cannot invent.

See [Design Concepts Ledger](DESIGN-CONCEPTS.md).

## Portable Code Agent Kit

The operational package is physically separated from repository history and evaluation material.

```text
Code-Agent-Kit/
├─ en/   # independently copyable English mirror
└─ ko/   # independently copyable Korean mirror
```

Both mirrors have identical relative paths and are independently copyable.

Each mirror includes the required `docs/`, `demos/`, prompts, templates, stacks, tools, scripts, reference assets, hidden agent adapters, licenses, and optional sample. Historical design-review and evaluation reports stay outside the portable package.

See [Portable Code Agent Kit Layout](Code-Agent-Kit/en/docs/getting-started/portable-code-agent-kit.md).

## Persistent state and session handoff

```text
Project Map
→ feature current
→ related files and shared dependencies
→ active worklog only when unfinished
→ source
```

- **Feature current** is the persistent verified starting state for every later modification.
- **Feature history** is append-only and indexes commits and PRs.
- **Worklog** is a temporary checkpoint with Gate progress, evidence, and Resume Point.
- A worklog never replaces current state.

See [State and Memory Model](Code-Agent-Kit/en/docs/core/state-and-memory-model.md).

## User input is required for each stack

The generic core can detect files and packages, but it cannot safely invent:

- supported SDK and runtime policy;
- authoritative framework references;
- golden skeleton files;
- feature boundaries;
- internal conventions;
- communication and data contracts;
- capability branch rules;
- validation commands and failure signals;
- confidentiality policy.

A stack is not ready until its required inputs and blocking capabilities are resolved.

```bash
python Code-Agent-Kit/en/tools/check-stack-readiness/check_stack_readiness.py \
  --stack Code-Agent-Kit/en/stacks/react-aspnetcore
```

See [Stack Input Requirements](Code-Agent-Kit/en/docs/getting-started/stack-input-requirements.md).

## Mandatory execution model

```text
1 Analysis
→ 2 Task
→ 3 Todo and Micro-Verify
→ 4 Checklist
→ 5 Verification
```

The five headings are a required output scaffold. A local Todo failure repeats that Todo. A wrong assumption, scope problem, source conflict, or unknown capability returns to Analysis.

See [Mandatory Gate](Code-Agent-Kit/en/prompts/GATE.md).

## Deterministic evidence

The workflow includes:

- stack-readiness validation;
- state-model validation;
- Git-scope and document-sync checks;
- generic build-log scanning;
- rendered SPA extraction;
- grid, form, button, KPI, card, chart, matrix, and panel evidence;
- empty visual-block rejection;
- reference-image hashes, ICC, EXIF, palette, regions, and ΔE00 comparison;
- static and runtime color contrast;
- Playwright E2E and optional visual baselines.

A model saying “PASS” is not evidence. Program exit codes and generated artifacts are.

## Start here

1. [Getting Started](Code-Agent-Kit/en/docs/getting-started/README.md)
2. [Design Concepts Ledger](DESIGN-CONCEPTS.md)
3. [State and Memory Model](Code-Agent-Kit/en/docs/core/state-and-memory-model.md)
4. [Stack Input Requirements](Code-Agent-Kit/en/docs/getting-started/stack-input-requirements.md)
5. [Operational Prompt Router](Code-Agent-Kit/en/prompts/README.md)
6. [React + ASP.NET Core Stack Profile](Code-Agent-Kit/en/stacks/react-aspnetcore/README.md)
7. [TaskFlow Sample](Code-Agent-Kit/en/samples/react-aspnetcore-taskflow/README.md)
8. [Human Developer Guide](Code-Agent-Kit/en/docs/human/developer-guide.md)

## Included structure

- bilingual governance documentation and templates;
- architecture decisions and rejected alternatives;
- feature current/history/worklog templates;
- system and database architecture state templates;
- complete verified-stack template contract;
- ready React + ASP.NET Core sample stack;
- blocked placeholders for Go + HTMX, Rust, and Elixir until owner inputs are supplied;
- Codex, Roo Code, Zoo Code, Cline, and Claude Code adapters;
- project-scoped MCP examples;
- deterministic tools and self-tests;
- React + ASP.NET Core TaskFlow sample.

## Validation layers

```text
Artifact / Compile
≠ Rendered Output
≠ Runtime Behavior
≠ Accessibility / Color
```

A build can pass while the screen is empty or runtime behavior fails. All applicable layers must be recorded separately.

## Source assets

- Image → Reference Image Manifest before multimodal transformation.
- SPA → rendered DOM and Screen Specification.
- Static HTML → preserved original and bounded inspection.
- MCP or search result → compact fact and provenance, not a retained transcript.

## Stack profiles

A complete stack pack includes:

```text
STACK.md
STACK-INPUTS.md
STACK-READINESS.json
AGENTS.stack.md
SKILL.md
capability-detection.md
feature-model.md
artifact-contract.md
communication-contract.md
evidence-provenance.md
references/
skeletons/
validation/
```

Internal library names and organization-specific rules belong in the relevant private stack pack, not in the generic core.

## Supported coding agents

- Codex
- Roo Code
- Zoo Code
- Cline
- Claude Code

Tool adapters point to the same `AGENTS.md`; they do not redefine the workflow.

## Enforcement

Honesty comes first: the agent reports its own mistakes, stops on uncertainty instead of guessing, and treats "done" as "passed verification" (see `AGENTS.md`). Because a model cannot reliably grade itself, the rules are enforced by machine, not by request:

- a **commit-time gate** and **CI job** (`tools/enforce-agent-gates`) block any commit that changes source without the required worklog, the five Gate sections, and state sync;
- a **sanitization gate** (`tools/check-sanitization`) blocks proprietary or organization-identifying strings before a public release.

Turn on the commit gate with `scripts/install-hooks.sh` (Windows: `install-hooks.ps1`). Details in the enforcement matrix; an optional agent stance is in `docs/persona.md`.

## Licensing

The entire project is released under the **MIT License** (see [LICENSE](LICENSE)) — free for commercial and closed-source use; keep the copyright notice. Feedback is welcome but not required.

