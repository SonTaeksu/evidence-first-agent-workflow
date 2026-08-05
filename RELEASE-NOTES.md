# Alpha Release Notes

**English** | [한국어](RELEASE-NOTES.ko.md)

## v0.1.9-alpha — Desktop stack, self-checking kit, and a beginner-first entry point (2026-08-04)

### Headline

Three things, and one of them is uncomfortable.

**A second ready stack.** C# Windows Forms on .NET Framework 4.7.2+, complete with a reference skeleton and a validation profile. It exists partly as a teaching case: Windows Forms produces no rendered document, so the usual "did the screen actually render" check has nothing to look at. Rather than quietly dropping that layer, the pack reads the form's designer file and compares the declared controls against a specification written before the code existed.

**The kit now checks itself.** `check-kit-selfcheck` copies the templates the kit tells you to copy and runs the kit's own validator on them. `check-mirror-parity` compares the two language mirrors and compares the numbers documents claim against measurement.

**The uncomfortable part: the self-check found a real defect on its first run.** `templates/stack-profile/` — the folder `using-another-stack.md` tells you to copy — was missing a file its own manifest lists as required. Anyone following the documented path got a readiness failure they did not cause. That defect had been shipping. It is fixed, and the check that would have caught it now runs.

### ⚠️ Behaviour change

Nothing blocks that did not block before, but two claims are now machine-checked:

| Change | Direction | What newly fails |
|---|---|---|
| `mirrored_file_count` verified against measurement | stricter | a manifest whose count is wrong, once `mirrored_file_count_rule` is present |
| Every stack declaring `ready` must validate as ready | stricter | a stack pack shipped in a state it cannot reach |
| Seed templates must have no missing required document | stricter | a scaffold that cannot pass the kit's own checks |

If you maintain a fork, run `check-mirror-parity` and `check-kit-selfcheck` before upgrading rather than after.

### Added
- `stacks/csharp-winforms/` — ready, both mirrors, `check_stack_readiness` exit 0.
- `tools/check-kit-selfcheck/`, `tools/check-mirror-parity/` — with self-tests.
- `docs/core/gate-design-principles.md` — the conditions a new check must satisfy before it may block anything.
- `OVERVIEW.md` / `OVERVIEW.ko.md` — the full reference, moved out of README.

### Fixed
- `docs/core/honesty-and-correction.md` (en) was truncated mid-sentence.
- `templates/stack-profile/` was missing two files, one of which its own manifest requires.
- `enforcement-matrix.md` named a tool that does not exist.
- `KIT-MANIFEST.json` carried a file count that matched no counting rule.

### Changed
- `README` rewritten for a reader new to AI coding agents, with an explicit nine-item cost-and-risk section.
- `CONTRIBUTING` corrected: a new stack profile needs fourteen documents, not four.
- `ADOPTION` now asks for model, GPU, VRAM, RAM, context window, and observed speed.

### Reported — running on 6 GB of VRAM

Pi Agent with Qwen3.6 35B A3B Compact, laptop, 6 GB VRAM, 32 GB RAM: a feature completed end to end with human intervention, at roughly 45 tokens/second falling to about 21 as the context grew.

Caveats, because they matter: it was a light test rather than a benchmark, it ran on the original internal version rather than this public release, a human had to step in on the private stack's server-call convention and a client-side display detail, and 21 tokens/second on a long context is slow enough that you will feel it.

### Verification

19 gates, 0 failures. `check_sanitization` clean over 689 files. 64 Python files compile. Both mirrors measure 327 files with identical paths and 68 byte-identical shared scripts.

Not claimed: application-level gates that need a browser, a .NET SDK, or Docker remain `PENDING` in the generation environment, as before. See `PRE-COMMIT-VALIDATION.md`.

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

## v0.1.5-alpha — State, design intent, and stack-input correction

### Added

- public Design Concepts Ledger;
- architecture decisions preserving rejected alternatives;
- feature current, append-only history, and corrected worklog templates;
- system and database architecture current/history;
- Project Map feature routing, capabilities, and Shared File Reverse Index;
- Stack Input Requirements and complete verified-stack template contract;
- stack-readiness validator and self-test;
- state-model validator and self-test;
- generic build-log scanner and self-test;
- honesty/correction, validation-layer, MCP compaction, Git workflow, and output-adapter documents;
- KPI, card, chart, matrix, panel, and empty visual-block extraction;
- visual-block completeness failure gate;
- ready React + ASP.NET Core stack manifest;
- blocked input manifests for planned Go + HTMX, Rust, and Elixir stacks.

### Corrected

- Worklog no longer appears to replace feature current.
- Resume order is now worklog header → Git → Project Map → feature current → full worklog.
- Root AGENTS is thin and tool adapters point to it.
- Stack-specific internal names are removed from the generic core.
- Artifact, rendered output, runtime behavior, and color are separate validation layers.
- Project and feature state are separated in the sample.

### Validation completed in the generation environment

- agent configuration and thin-adapter validation: PASS;
- React + ASP.NET Core stack readiness: PASS;
- stack-readiness pass/fail self-test: PASS;
- sample state-model validation: PASS;
- state-model pass/fail self-test: PASS;
- build-log pass/fail self-test: PASS;
- SPA grid and visual-block extraction: PASS;
- missing-column and empty-visual-block failure paths: PASS, exit code 2;
- Reference Image Manifest and ΔE comparison: PASS;
- Python compilation and JavaScript syntax: PASS.

### Still required locally or in CI

- fresh frontend npm install, type check, tests, and build;
- ASP.NET Core restore, build, and tests;
- browser runtime E2E and axe color gate;
- Docker build and smoke test.

No unavailable result is reported as PASS.
