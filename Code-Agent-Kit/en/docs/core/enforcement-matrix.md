# Enforcement Matrix — machine-enforcing the Markdown rules (maximum reached)

This lists each rule written in prose in `AGENTS.md`, `prompts/GATE.md`, and
`docs/core/*`, and states honestly how far it is **machine-enforced**.

Enforcement levels:

- **BLOCK** — deterministically checkable. A violation is refused at commit (pre-commit) and merge (CI). Owned by `enforce_gates.py`.
- **EVIDENCE** — the rule is cognitive and cannot be checked directly, so the **artifact it must produce** (worklog sections, state docs) is enforced instead. Skipping the step leaves the artifact empty and is caught as a BLOCK. (indirect)
- **TOOL** — an existing kit tool already checks this deterministically; invoked from CI / hook.
- **ADVISORY** — not verifiable from commit artifacts alone. The residue that cannot be enforced (reason given).

---

## AGENTS.md

| Rule | Level | Mechanism |
|---|---|---|
| No plaintext password/secret/key in source or config | **BLOCK** | `gate_secret_scan` — scans staged source/config diff for credential patterns; exit 2 |
| Source work must leave a worklog (checkpoint) | **EVIDENCE** | `gate_worklog_and_gate_sections` — a `docs/worklogs/*.md` is required on source change |
| Completion: current/history/Project Map sync | **BLOCK / WARN** | `gate_state_sync` — current + history required (BLOCK); project-map is "impact review" so its absence is a WARN |
| Completion: final Git diff review, honest PENDING report | ADVISORY | diff facts are checked, but "did you review / were you honest" is cognitive; partly nudged by requiring §5 Verification |
| Start order: read Project Map → current → related first | ADVISORY / EVIDENCE | "did you read" is unobservable; nudged by requiring routing fields in worklog §1 Analysis |
| Unknown → `⟨verification required⟩`, no guessing | ADVISORY | guessing is not detectable; optional placeholder-token check can partly block |
| Follow procedure without exception; press the user for omitted inputs | ADVISORY / EVIDENCE | pressing the user is behavioral; the missing input surfaces as a failed gate downstream |

## prompts/GATE.md

| Rule | Level | Mechanism |
|---|---|---|
| Keep the 5 headers (1 Analysis → 5 Verification), no renaming/omitting | **BLOCK** | `gate_worklog_and_gate_sections` — checks the 5 section headers exist; exit 2 |
| Expected Files has ≥1 concrete entry | **BLOCK** | checks a `- [ ] path` entry exists under Expected Files |
| Staged source must be declared in Expected Files | **BLOCK (opt)** | `gate_unexpected_files` — `--strict-scope` blocks undeclared source; WARN by default |
| Prewrite boundary (edit only after token) | ADVISORY → TOOL | no token tool in v0.1.6; promote to TOOL by porting the newer `check-workflow-preflight` |
| Do not implement during Analysis | ADVISORY | cognitive ordering; not checkable |

## docs/core/state-and-memory-model.md

| Rule | Level | Mechanism |
|---|---|---|
| current/history/worklog roles separated; worklog never replaces current | **TOOL** | existing `check-state-model` self-test / check (run in CI) |
| history is append-only | ADVISORY | partially checkable via diff; not fully enforced |

## docs/core (others) and stacks

| Rule | Level | Mechanism |
|---|---|---|
| Git scope: no unrelated changes | **TOOL** | existing `check-git-scope` (CI / hook) |
| Adapter config integrity (.mcp.json etc.) | **TOOL** | existing `check-agent-config` (needs Python ≥3.11) |
| Build/test exit code preserved; self-report is not a gate | **TOOL** | existing `check-build-log` self-test |
| UI color contrast / empty visual block | **TOOL** | existing `ui-color-gate`, `spa-screen-extractor` |
| Portable kit path/link parity (en=ko) | **TOOL** | existing `check-portable-kit` |
| Stack readiness (no use before capability confirmed) | **TOOL (partial)** | existing `check-stack-readiness`; actual API-use blocking remains ADVISORY |
| No proprietary/org-identifying strings in the public tree | **BLOCK** | `check-sanitization` (CI + pre-release); exit 2 on match |

---

## Maximum reached, and the honest boundary

**Enforced (BLOCK/EVIDENCE/TOOL):** secret exposure, worklog + 5 sections, state sync,
Expected Files, sanitization, and the existing tools (state-model, git-scope, build-log,
color, portable parity) invoked from CI/hook. These run automatically at commit and CI, so
a violation cannot land in the repository.

**Not enforceable (ADVISORY):** cognitive/judgment rules — "did you read first", "did you
avoid guessing", "did you honor the authority order". These cannot be verified from commit
artifacts. Instead the artifact each rule must produce (worklog sections, state docs) is
enforced, so skipping leaves a detectable trace. That is the maximum current tech allows.

**Write-time blocking (level A):** stopping the agent from editing a file without procedure
requires a platform write-hook/permission API. Commit blocking (B) + CI blocking (C) are the
substitute defense; they make "violate, then pretend it's done" impossible.
