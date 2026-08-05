# Overview — full reference

**English** | [한국어](OVERVIEW.ko.md)

> New here? Read [README.md](README.md) first, then [QUICKSTART.md](QUICKSTART.md). This page is the complete reference and assumes you already know what the project is for.

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

Both mirrors have identical relative paths and are independently copyable. `tools/check-mirror-parity` enforces that: an orphan path, a shared script that drifted between mirrors, or a counted claim contradicted by measurement fails with exit 2.

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
- Playwright E2E and optional visual baselines;
- Windows Forms designer control-tree extraction and screen-specification comparison, for a UI framework that produces no rendered document.

A model saying “PASS” is not evidence. Program exit codes and generated artifacts are.

## Start here

1. [Getting Started](Code-Agent-Kit/en/docs/getting-started/README.md)
2. [Design Concepts Ledger](DESIGN-CONCEPTS.md)
3. [State and Memory Model](Code-Agent-Kit/en/docs/core/state-and-memory-model.md)
4. [Stack Input Requirements](Code-Agent-Kit/en/docs/getting-started/stack-input-requirements.md)
5. [Operational Prompt Router](Code-Agent-Kit/en/prompts/README.md)
6. [React + ASP.NET Core Stack Profile](Code-Agent-Kit/en/stacks/react-aspnetcore/README.md)
7. [C# Windows Forms Stack Profile](Code-Agent-Kit/en/stacks/csharp-winforms/README.md)
8. [TaskFlow Sample](Code-Agent-Kit/en/samples/react-aspnetcore-taskflow/README.md)
9. [Gate Design Principles](Code-Agent-Kit/en/docs/core/gate-design-principles.md)
10. [Human Developer Guide](Code-Agent-Kit/en/docs/human/developer-guide.md)

## Included structure

- bilingual governance documentation and templates;
- architecture decisions and rejected alternatives;
- feature current/history/worklog templates;
- system and database architecture state templates;
- complete verified-stack template contract;
- ready React + ASP.NET Core sample stack;
- ready C# Windows Forms stack for .NET Framework 4.7.2 and later, with a reference skeleton and designer-tree evidence;
- ten stack profiles that stay blocked until owner inputs arrive — WPF, WCF, ASMX, Vue.js, Next.js, Node.js, Go, Go + HTMX, Rust and Elixir — each already carrying that technology's constraints, silent-failure pitfalls, capability-detection rules and documentation routing;
- Codex, Roo Code, Zoo Code, Cline, and Claude Code adapters;
- project-scoped MCP examples, and per-stack profiles pointing at fourteen public documentation servers that were verified by connecting and issuing a real call (`docs/core/mcp-source-verification.md`);
- deterministic tools, each shipped as a Python + PowerShell pair whose verdicts are proven identical, plus a self-test per tool;
- React + ASP.NET Core TaskFlow sample.

## Validation layers

```text
Artifact / Compile
≠ Rendered Output
≠ Runtime Behavior
≠ Accessibility / Color
```

A build can pass while the screen is empty or runtime behavior fails. All applicable layers must be recorded separately. A layer that cannot run is recorded as `PENDING` with a reason, never as `PASS`.

## Source assets

- Image → Reference Image Manifest before multimodal transformation.
- SPA → rendered DOM and Screen Specification.
- Static HTML → preserved original and bounded inspection.
- Desktop UI with no rendered document → designer control tree and screen specification.
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
mcp-profile.json.example
mcp/source-routing.md
references/
skeletons/
validation/
```

`mcp/source-routing.md` names the documentation server that is authoritative for the
stack, the server that is **not**, and the tool names each one actually exposed when
it was tested. The example profile is not enabled by default: copying it is how an
operator accepts that these queries leave the machine.

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
- a **sanitization gate** (`tools/check-sanitization`) blocks proprietary or organization-identifying strings before a public release;
- a **mirror-parity check** (`tools/check-mirror-parity`) blocks an orphan path, a shared script that drifted between the language mirrors, and a counted claim contradicted by measurement;
- a **kit self-check** (`tools/check-kit-selfcheck`) runs the templates the kit tells you to copy through the kit's own validation, so a scaffold cannot ship in a state where the only exit is `--no-verify`;
- a **twin-parity check** (`tools/check-script-parity`) compares every tool's Python and PowerShell implementations case by case (154 at the time of writing; `--status` prints the current count) — the exit code **and** the finding identifiers must match, and each case also pins the exit code the convention requires, so two implementations cannot agree on a wrong answer and pass;
- **measured stack readiness** (`tools/check-stack-readiness`) resolves every cited evidence path against the tree, so a manifest that names files which do not exist derives `blocked` instead of `ready`.

Turn on the commit gate with `scripts/install-hooks.sh` (Windows: `install-hooks.ps1`), or with one line: `git config core.hooksPath tools/enforce-agent-gates`.

The hook needs **Python 3.11 or newer, or PowerShell** — it picks whichever is present, and refuses the commit when neither is. Python 3.11 is the floor because one check reads Codex's TOML configuration and `tomllib` arrives in the standard library there; on an older interpreter that check exits 1 with the requirement stated rather than crashing.

Details in the [enforcement matrix](Code-Agent-Kit/en/docs/core/enforcement-matrix.md). The conditions a new check must satisfy before it earns a place there are in [Gate Design Principles](Code-Agent-Kit/en/docs/core/gate-design-principles.md). An optional agent stance is in `docs/persona.md`.

## Honest boundaries

- Cognitive rules — "did you read first", "did you avoid guessing", "did you honor the authority order" — cannot be verified from commit artifacts. What is enforced is the artifact each rule must produce, so skipping leaves a detectable trace.
- Write-time blocking (refusing an edit as it happens) requires a platform write-hook API that does not exist here. Commit-time and CI blocking are the substitute.
- A false positive is treated as more damaging than a missed defect, because one false alarm teaches the operator to bypass the gate permanently.

## Licensing

The entire project is released under the **MIT License** (see [LICENSE](LICENSE)) — free for commercial and closed-source use; keep the copyright notice. Feedback is welcome but not required.
