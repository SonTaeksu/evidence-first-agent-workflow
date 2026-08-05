# Roadmap

**English** | [한국어](ROADMAP.ko.md)

## Done

- Governance core: five-stage Gate, externalized state (current / append-only history / worklog), deterministic validators.
- Machine enforcement: commit + CI gate and a public-release sanitization gate.
- Independently copyable `Code-Agent-Kit/en` and `ko` mirrors.
- One-page QUICKSTART and an optional agent stance.
- React + ASP.NET Core sample stack.
- C# Windows Forms stack for .NET Framework 4.7.2+, including a rendered-output route for a UI framework that produces no rendered document.
- The kit checks itself: `check-kit-selfcheck` runs the documented copy sources through the kit's own validator, and `check-mirror-parity` compares the language mirrors and the numbers documents claim against measurement.
- `docs/core/gate-design-principles.md` — the conditions a new check must satisfy before it may block anything.
- Beginner-first README with an explicit cost-and-risk section, and the full reference moved to `OVERVIEW.md`.
- Every check ships as a Python + PowerShell pair, and the pair is *proven* equal: `check-script-parity` compares them case by case on verdict **and** finding identifier, and fails if any one disagrees. The commit hook falls back to PowerShell, so a machine with no Python is still gated.
- Stack readiness is **measured, not declared**: `check-stack-readiness` resolves every cited evidence path against the tree. A manifest naming files that do not exist used to validate as `ready`.
- Twelve stack profiles: two ready, ten carrying the technology's own constraints, pitfalls, capability-detection rules and documentation routing while waiting on owner inputs.
- Documentation sources are verified rather than listed. Fourteen public MCP endpoints were checked by connecting and issuing a real call; `docs/core/mcp-source-verification.md` records the run, the one partial result, the one candidate rejected on inspection, and what the check does *not* prove.
- This repository has its own CI. It previously had none, which is why a failing self-test survived three releases.

## Next

- Fill in the ten blocked stacks as owners supply versions, commands and conventions; the profiles are written and waiting.
- Port the prewrite-token preflight so "edit source only after a passing token" becomes a hard tool gate rather than advice.
- Stack-specific artifact / binding validators and Artifact / Rendered / Runtime result aggregation.
- A worked run of the public release on a small local model, to replace the maintainer's internal-version report with a reproducible one.
- Adoption reports from machines other than the maintainer's — this is the gap that limits every claim in the README.

## Stacks waiting on owner inputs

Each already contains the technology's constraints, its silent-failure pitfalls,
how to detect what a project uses, and which documentation server to ask. What is
missing is versions, build and test commands, data access, authentication and
deployment — the things the kit refuses to guess.

- WPF (.NET Framework 4.7.2+) — ships a skeleton, not yet compiled anywhere
- WCF (.NET Framework 4.7.2+)
- ASMX / ASP.NET XML Web Services (.NET Framework 4+)
- Vue.js
- Next.js
- Node.js
- Go
- Go + HTMX
- Rust
- Elixir
