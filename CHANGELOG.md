# Changelog

**English** | [한국어](CHANGELOG.ko.md)


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
