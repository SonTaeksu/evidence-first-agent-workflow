# Design Concepts Ledger

**English** | [한국어](DESIGN-CONCEPTS.ko.md)

This document records **why** the workflow is designed this way. Operational rules live in `AGENTS.md`, `prompts/`, stack profiles, and tools. When a future change intentionally alters a concept below, record the reason in an architecture decision.

## 0. Problems this workflow addresses

The workflow was created for three recurring problems:

1. **Models cannot reliably infer niche, legacy, or internal framework facts.**  
   A plausible API name is not evidence. Framework-specific knowledge must come from verified references, installed artifacts, real skeleton files, source inspection, or official documentation.

2. **Small and closed-network models lose instruction adherence as rules accumulate.**  
   Passive guidance is not enough. The workflow uses short routing documents, fixed output scaffolds, mandatory gates, and program exit codes.

3. **Long-lived project cost is dominated by state recovery and handoff.**  
   The current implementation state, history, evidence, and completion criteria are stored in files instead of depending on a chat session.

The reusable model is:

```text
Framework-agnostic governance core
+
Verified stack or organization knowledge pack
```

## A. Governance model

### A1. Externalized memory and progressive disclosure

The model does not reload the entire repository for every task.

```text
Project Map
→ feature current state
→ related files by role
→ active worklog when unfinished
→ actual source
→ search only when evidence is still insufficient
```

The Project Map routes. Feature current state explains the verified implementation. Code and deterministic evidence remain the source of truth.

### A2. Thin root rules and selective routing

`AGENTS.md` is always loaded and must remain short. Detailed procedures belong in:

- `prompts/`
- `docs/core/`
- `stacks/<stack>/`
- `tools/*/README.md`

A stack `SKILL.md` routes to the smallest relevant reference. General framework tutorials should not be copied into a knowledge pack merely because they are available.

### A3. Mandatory five-stage gate

All file-producing work follows:

```text
1 Analysis
→ 2 Task
→ 3 Todo and Micro-Verify
→ 4 Checklist
→ 5 Verification
```

The five headings are an output scaffold, not a suggestion. Missing stages mean the gate has not been completed.

A local Todo failure repeats that Todo. A wrong assumption, scope error, or unknown capability returns to Analysis.

### A4. Current, history, and worklog are different documents

```text
current
= persistent, verified state of the feature
= mandatory starting point for later modification

history
= append-only change record
= prior entries are never silently edited or deleted

worklog
= temporary checkpoint for an unfinished task
= Gate progress, Todo state, extracted evidence, and Resume Point
= never a replacement for current
```

A worklog can identify the feature in a new session, but the agent still reads Git state, Project Map, and the feature current document before resuming.

### A5. Definition of Done

Completion requires:

- deterministic validation;
- current state updated and linked to the verified commit;
- append-only history entry with commit and PR when available;
- Project Map and shared-file reverse index updated;
- active worklog completed or archived;
- final Git Diff reviewed;
- all unresolved checks reported as `PENDING`, never as `PASS`.

### A6. Project Map as a routing and impact index

The Project Map contains:

- feature routing;
- current/history/worklog paths;
- entry points;
- architecture state documents;
- environment capability decisions;
- shared-file reverse dependencies and required regression checks.

## B. Honesty and evidence

### B1. Calibrated uncertainty

Unknown information is recorded as:

```text
⟨verification required: what must be checked and how⟩
```

Guessing a value is not progress. When a previous diagnosis is found to be wrong, record a correction before continuing. A correct result with an incorrect explanation is not considered verified.

### B2. Artifact, rendered output, and runtime are separate gates

```text
Artifact or compile success
≠ rendered output fidelity
≠ runtime behavior
```

A build can pass while visual blocks are empty or runtime behavior fails. UI work records all applicable layers separately.

**When a stack has no rendered document, the layer is replaced, not dropped.** A desktop UI framework may produce nothing a program can inspect without launching the application. The temptation is to let the rendered-output layer collapse into "the build succeeded" — which is exactly the failure this concept exists to prevent. The stack pack must supply a substitute declaration that a program can compare against a specification written before implementation. The C# Windows Forms pack does this by parsing the designer file's control tree; see `stacks/csharp-winforms/references/ui-evidence-contract.md`.

### B3. Primary-source provenance

Stack facts record:

- claim;
- source type and location;
- version;
- verification method;
- verification date;
- confidence;
- unresolved placeholder when evidence is missing.

Useful source types include official documentation, installed SDK files, source repositories, binary or API inspection, official samples, and user-supplied authoritative material.

## C. Capability enforcement

Important environment choices are enforced in three layers because a small model may ignore a single instruction:

1. **Project Map** records the detected capability and evidence.
2. **Gate Analysis output** states the selected implementation path.
3. **Stack rule** prohibits APIs or patterns until the capability is confirmed.

Examples include:

- shared API client;
- generated SDK;
- authentication provider;
- ORM or data-access style;
- runtime and SDK version;
- shared communication library;
- design system;
- generated-code ownership.

A capability with status `unknown` blocks the dependent implementation path.

## D. Stack-owned concepts

The generic core does not decide every framework boundary. Each stack profile defines:

- feature boundary and action model;
- artifacts that must be real framework files;
- installed-version rules;
- communication and data contracts;
- capability-detection logic;
- verified facts and pitfalls;
- skeleton or golden reference files;
- validation commands and failure signals.

Stack-specific names and internal library names stay in the relevant private or public stack pack, not in the generic core.

## E. Deterministic input and output handling

### E1. Input preprocessing

- Image: preserve original bytes, ICC, EXIF, pixel hashes, palette, regions, and normalized lossless output.
- SPA: render JavaScript, store rendered-DOM hash, and extract structural evidence.
- Static HTML: preserve source and read bounded sections.
- Large MCP or search result: store only the needed fact and provenance; do not carry the full result into later sessions.

### E2. Output verification

An honesty rule assumes the model can evaluate its own output; a weaker model will mark an empty or broken artifact as "passed." So the model's self-report is never a gate — a deterministic tool with an exit code is. Self-assessment does not substitute for a passing check, and the check must run automatically (commit and CI), not only when the agent chooses to. Tools inspect:

- build and test exit codes;
- generated artifacts;
- Git scope;
- screen structure;
- required columns, rows, controls, buttons, and visual blocks;
- empty placeholders;
- color contrast and runtime colors;
- binding or contract evidence when the stack adapter supports it.

### E3. Gate design, and the cost of a false positive

A gate survives on the assumption that a failure means a real defect. One false alarm breaks that assumption, the operator starts using `--no-verify`, and the whole hook goes inert. The cost of a false positive is not one wasted minute; it is every check you have.

This inverts the usual instinct: a check that might be wrong stays at WARN, and `BLOCK` is claimed only after zero false positives have been observed on real material.

But the naive application of that rule produces a matrix where trivial issues block and catastrophic ones merely warn. So the second half of the rule matters as much as the first: **a silent failure must block.** A loud failure — a build error, an exception — can afford to be a warning, because something else surfaces it. A response that returns success with zero rows, a screen that renders empty, a run that exits 0 having done nothing: nothing else surfaces those. Certainty is why a check may block; being unobservable is why it must.

The remaining conditions, derived from the same observations:

- **The escape hatch is an explicit marker, never an implicit one.** Every check needs a way out or the first legitimate exception kills it — but the way out is a declaration of intent written by a person, not a circumstance like "the file already exists". An implicit exemption is indistinguishable from the defect it was meant to allow.
- **The rule ID belongs to the tool.** The check prints its own identifier on failure. Asking the model to tag its output with the rule it satisfied is a step that gets skipped, and small models skip it always. Traceability that survives without the model's cooperation is the only kind worth having.
- **The basis for judgement lives in a project document.** A check that depends on the model deciding "does this project use X" is one the model walks around by deciding differently tomorrow. Record the decision once in project state and have the check read it.
- **Removing a decision raises execution.** A check that requires choosing which files to pass does not get run; deciding the arguments is itself a step, and that step is what gets skipped. The runner takes no arguments for the common case.
- **Your own output fails the same way.** A template the kit tells the user to copy must pass the kit's own validation unmodified, or the only exit is bypassing the gate. Verify artifacts by measurement rather than re-reading them, and generate documents from a diff and a count — every hand-copied number is a place the document goes stale silently.

The full statement, with the observed failures each rule was derived from, is in `docs/core/gate-design-principles.md`.

## F. Rejected alternatives

The following approaches were rejected:

- splitting current state into one file per CRUD verb;
- repeating large detail blocks for every action when actions share one feature state;
- loading all references in every session;
- relying on one passive capability instruction;
- treating a successful build as proof of visual or runtime correctness;
- keeping human onboarding guides in normal agent context;
- silently accepting unexpected changed files;
- renaming stable paths solely to modernize terminology.

Rejected decisions are recorded under `docs/architecture/decisions/` so future agents do not reintroduce them without an explicit reason.

## G. Operating lessons

- Small models need fewer always-loaded rules and more mechanical gates.
- General knowledge that the model already knows can reduce signal; knowledge packs should focus on project-specific or inference-resistant facts.
- Session compression loses design decisions; current, history, worklog, and decisions protect against that loss.
- MCP retrieval still consumes context. Summarize verified facts and provenance, then discard unnecessary retrieval text.
- Niche-framework facts require primary-source verification.
- An observation is not a diagnosis. Counting how often a term appears says nothing about whether a rule is scoped — the scope may live in one of those occurrences. The dangerous outcome is not a missed defect but a confident correction built on a wrong reading, because it edits working material.
- Numbers written by hand into documents go stale silently. Generate them, or record the rule by which they can be measured. A number with neither is unverifiable, and no amount of reading will settle it.
- A check the project writes about itself finds defects the project could not see. Two of the four defects repaired in v0.1.9 were found by the kit's new self-check on its first run; the other two were found by a person reading, and are still not machine-checkable.

## H. Public positioning

The core is a tool-agnostic context-