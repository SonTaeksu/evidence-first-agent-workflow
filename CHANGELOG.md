# Changelog

**English** | [한국어](CHANGELOG.ko.md)


## v0.1.9-alpha — Desktop stack, self-checking kit, and a beginner-first entry point (2026-08-04)

### Added — C# Windows Forms stack (ready)
- `stacks/csharp-winforms/` for .NET Framework 4.7.2 and later: all fourteen required documents, a reference skeleton (`skeletons/MinimalApp/` — SDK-style `net472` project, `App.config` per-monitor v2 DPI, Windows 10 manifest declaration, designer/behaviour separation, single service boundary), and MSBuild/VSTest validation profile. `check_stack_readiness` reports `READY`, exit 0, in both mirrors.
- `references/ui-evidence-contract.md` and `tools/extract_designer_tree.py` + `check_designer_spec.py`: Windows Forms produces no rendered document, so the rendered-output layer reads the designer control tree and compares it against a screen specification written during Gate §1. Comments are blanked length-preservingly before matching and string literals are preserved; fourteen self-test cases, half of which assert that something is *kept*.
- Every version-sensitive fact in `references/verified-facts.md` and `evidence-provenance.md` cites Microsoft Learn with a verification date.

### Added — the kit now checks itself
- `tools/check-kit-selfcheck/`: copies each documented copy source exactly as the kit instructs and runs the kit's own readiness validator on it. A blank seed is *supposed* to report `blocked`, so unresolved inputs are ignored and only structural failures count. Also requires every stack declaring `ready` to validate as ready.
- `tools/check-mirror-parity/`: relative-path set equality between mirrors, byte-identity of non-prose files, and counted claims compared against measurement. A count whose counting rule is not recorded is a WARN, not a FAIL — the claim may be correct under a rule the document never wrote down. Build residue is excluded from measurement and warned.
- Both are registered in `docs/core/enforcement-matrix.md`, `KIT-MANIFEST.json`, and `check_kit_installation.py`.

### Added — gate design principles
- `docs/core/gate-design-principles.md` (en/ko): the conditions a new deterministic check must satisfy before it is allowed to block anything, generalized from the private kit's own enforcement-design principles and its record of twelve observed sessions.
- Grounded in the three observed facts the private kit derives every rule from: a rule written in a document is not followed regardless of model class; context compaction erases rules, so weight must move to the always-resident file and to the hook; and a self-reported "done" cannot be trusted, with rationalized failure as the dangerous form.
- Nine principles: a document cannot enforce, only a machine judgement did; block only what is certain; when uncertain WARN — **but a silent failure must block**, so the most dangerous case does not end up the most weakly guarded; the escape hatch is an explicit marker written by a person, never an implicit circumstance; the rule ID belongs to the tool, not to the model; the basis for judgement lives in a project document; removing a decision raises execution, so the runner takes no arguments for the common case; compile and test passing is not behaviour; your own output fails the same way, so verify artifacts by measurement and generate documents from a diff and a count.
- A closing section requires the honest limits to be published rather than hidden, including the three structural walls no principle removes: a check only fires if something triggers it, without CI there is no way to beat an uncooperative model, and context compaction cannot be fixed with a tool.

### Fixed
- `docs/core/honesty-and-correction.md` (en) was truncated mid-sentence at "Correct code with a wrong d". Restored, using the intact Korean mirror as the reference.
- `templates/stack-profile/` was missing `validation/validation-profile.md`, which its own `STACK-READINESS.json` lists as required. Copying it as `docs/getting-started/using-another-stack.md` instructs therefore failed readiness validation. Added, along with `mcp/source-routing.md` which `SKILL.md` referenced but which did not exist.
- `docs/core/enforcement-matrix.md` cited a tool named `check-portable-kit`; the tool on disk is `check-kit-installation`.
- `KIT-MANIFEST.json` claimed `mirrored_file_count: 270`, which matched no plausible counting rule. Added `mirrored_file_count_rule` and set the value to the measurement. The claim is now machine-checked.

### Changed — documentation entry point
- `README.md` / `README.ko.md` rewritten for a reader who is competent at programming but new to AI coding agents: the problem, a three-step start, what changes, what you get, **what it costs you** (nine numbered items, including that the gate is bypassable and that a false alarm is the real risk), how to add your own stack, and what hardware and models it runs on.
- `OVERVIEW.md` / `OVERVIEW.ko.md` (new) hold the previous README's full reference content, plus an "honest boundaries" section.
- `QUICKSTART`, `CONTRIBUTING`, and `ADOPTION` updated in both languages. `CONTRIBUTING` previously stated that a new stack profile needs four files; it needs fourteen, and following the old text produced a stack that fails validation.
- `ADOPTION` now asks for model, agent tool, GPU and VRAM, RAM, quantization, context window, observed speed, and how far the run got — because the claim that small models suffice needs evidence from machines other than the maintainer's.

### Reported — low-specification run
- Pi Agent with Qwen3.6 35B A3B Compact on a laptop with 6 GB VRAM and 32 GB RAM completed a feature end to end with human intervention. Approximately 45 tokens/second initially, falling to roughly 21 tokens/second as the context grew. This was a light test on the original internal version, not a benchmark and not this public release; the interventions concerned the private stack's server-call convention and a client-side display detail, not the workflow.

### Verified
- 19 gates run, 0 failures: stack readiness (2 stacks × 2 mirrors), kit self-check (2), kit installation (2), mirror parity, five self-tests, and the designer tools in both mirrors.
- `check_sanitization` over 689 files: CLEAN, 0 warnings.
- 64 Python files compile.
- Mirrors measure 327 files each, paths identical, all 68 shared scripts byte-identical.


## v0.1.8-alpha — Enforced honesty, process safety, and stack on-ramp (2026-07-15)

### Added — honesty and evidence rules (AGENTS.md, always loaded)
- "Honesty over completion" promoted to the top of `AGENTS.md` and `docs/core/honesty-and-correction.md`: report your own mistakes, stop on uncertainty instead of guessing.
- Completion-word discipline: reserve "done/complete/끝/완료" for a passing GATE §5; intermediate steps are "step N done".
- Evidence, not claims: a verification step must cite the real command and exit code, report each GATE stage before the next, and a `PASS` with no cited command/exit is treated as `PENDING`.
- Completion is anchored to a commit: no `complete` until the verification commit exists and its hash is recorded; before that, status is `verified, pending commit`.
- Stack / capability decision must be recorded explicitly in Analysis.

### Added — machine enforcement
- Commit-time gate + CI job (`tools/enforce-agent-gates/`): blocks a commit that stages project source without a worklog, the five GATE sections, and state sync; and rejects a worklog `PASS` with no cited command/exit.
- Public-release sanitization gate (`tools/check-sanitization/`): blocks organization/proprietary strings; exit 2.

### Added — command and process safety
- `docs/core/command-and-process-safety.md`: never bulk-kill by image name (`Get-Process node | Stop-Process`, `killall node`, `pkill -f npx`) — it kills the agent's own MCP servers.
- Managed service runner `tools/run-managed-service/run_service.py`: start/stop a dev server by tracked PID + port and verify the port is free. Wired into AGENTS and the stack template.

### Added — color/theme fidelity (react-aspnetcore)
- `stacks/react-aspnetcore/references/color-contract.md`: reference screenshot is the source of truth → extract palette → bind to CSS variable tokens → verify with ΔE; promoted `extract_palette` to a first-class reference-image tool.

### Added — docs and on-ramp
- Optional agent stance `docs/persona.md`.
- `QUICKSTART.md` overhaul (en/ko): first-time project setup (new vs existing, bootstrap prompts), verified Windows first-run (git one-liner, `.gitignore`, initial import `--no-verify`), what verification looks like, and gate bypass.
- New guide `docs/getting-started/using-another-stack.md` (en/ko): stack-agnostic core + swappable pack; who-does-what; how to designate md vs MCP sources with real examples; filling a stack with AI.
- `CLAUDE.md` now imports `@AGENTS.md`; Cline/Roo/Codex adapters strengthened to carry the non-negotiables.

### Changed
- Repository root restructured to intro/reference docs + independently copyable `Code-Agent-Kit/en` and `ko` mirrors.
- Relicensed the entire project to the **MIT License** (© Taeksu.Son and HUENSYSTEM Co., Ltd.).
- `ROADMAP` updated to reflect actual progress (done / next / candidate stacks).

## v0.1.6-alpha — Portable language-mirrored Code Agent Kit

### Added

- independently copyable `Code-Agent-Kit/en` and `Code-Agent-Kit/ko` distributions;
- identical relative paths;
- self-contained agent docs, human docs, demos, tools, scripts, stacks, reference assets, adapters, licenses, and sample;
- full/core installer modes;
- portable-kit mirror and link validator;
- inactive CI template instead of automatically activated workflows.

### Packaging decision

Historical design-review/evaluation reports and generated evidence remain in the repository but outside the portable kit.

## v0.1.5-alpha — Restore state model and verified-stack inputs

- Added the Design Concepts Ledger and architecture decisions.
- Restored feature-current-first routing and append-only history.
- Added stack owner inputs, readiness manifests, and deterministic readiness validation.
- Added shared reverse dependencies, Git state linkage, and architecture state.
- Added visual-block empty detection and generic output/build validator contracts.
- Slimmed agent adapters to pointers.

## v0.1.4-alpha — Code Agent Kit operational integration

- Implemented the previously deferred rendered-SPA input branch.
- Added screen completeness checks, prompt routing, worklogs, and human-guide boundaries.
- Upgraded Git scope validation.
- Preserved the existing image manifest as primary and added the Kit palette tools as backup.
- Added generic skill routing and demo isolation.

## v0.1.3-alpha — Reference image evidence before multimodal transformation

- Added exact original-file and decoded-pixel hashes.
- Added ICC, EXIF, palette, pixel-grid, and named-region evidence.
- Added a normalized lossless PNG.
- Added ΔE00 comparison with runtime computed colors.
- Added self-tests and command wrappers.
- Reserved SPA HTML ingestion until the prepared representative package is available.

## v0.1.2-alpha — Multi-agent configuration and UI color gates

- Added Codex, Roo Code, Zoo Code, Cline, and Claude Code setup.
- Added shared MCP configurations and validation.
- Added static and runtime UI color gates.
- Added one-command pre-commit validation scripts and a truthful partial-validation report.
- Added smaller-model computed-color evidence.
- Fixed two contrast failures found by the new gate.
- Recorded validation boundaries without claiming unavailable backend/browser results.

## v0.1.1-alpha — Full Korean documentation

- Added Korean companions for all human-readable public Markdown documents.
- Added bidirectional language navigation.
- Added a complete Korean documentation index.
- Added Korean summaries for immutable validation evidence.
- Added Korean license explanations while retaining official English license texts.
- Made GitHub Issue forms bilingual.
- Added translation policy and automated language-coverage checks.
- Kept English as the default GitHub entry language.

## v0.1.0-alpha

- Published the initial core workflow.
- Added the React + ASP.NET Core TaskFlow sample.
- Added Microsoft Learn MCP and Context7 routing.
- Added deterministic validation helper tools.
- Added the bilingual AI Workflow Design Review.
