# Gate Design Principles

How to add a deterministic check without destroying the checks that already work.

`enforcement-matrix.md` records what each rule enforces. This document records what a check must satisfy before it earns a place there.

These are not proposals. They were derived from observed failures across twelve real sessions on a closed network, using small and mid-sized local models, and they are stated in the order in which they were learned.

## Why these exist — three observed facts

Every rule below follows from one of these. When adapting this workflow, check first that these premises still hold in your environment.

### 1. A rule written in a document is not followed, regardless of model class

Models read a rule and violated it anyway. The worst observed case: a project document recorded "this project has no shared library — do not call its functions", the model **read that file**, then wrote the missing functions itself because a call was undefined. The invented file broke the build, and generation failed six times in a row.

Improving the document does not fix this. A program has to catch it.

### 2. Context compaction erases rules

The observed environment was a 64k context with automatic compaction around 50k. In one 12,811-line session, knowledge was retrieved twice, first at line 6,778 — everything before that was written from memory. A 15KB reference fetched early is already gone by the time code is written, which is why "read the document, then revert to training habit" repeats.

| Where a rule lives | After compaction | Conclusion |
|---|---|---|
| `AGENTS.md`, resident in the system prompt | **survives** | non-negotiable rules go here, and stay short |
| a document fetched during the session | **lost** | detail and reference only; never depend on it for a rule |
| a CLI check or a git hook | **unaffected** | strongest. Move a rule here whenever it can be moved |

### 3. A self-reported "done" cannot be trusted — the dangerous form is rationalized failure

Observed: compile passed, so "done", while a missing runtime dependency crashed on launch. Tests passed 6 of 6, so "done", while the test harness bypassed the path prefix and the real server returned 404. A generator reported `Success 46, Fail 1`, and the model wrote that the failure was "normal because that file is a different type" and declared completion — the failing file was one it had created itself. An install wrote 6 of 33 files and reported "install complete", recording files it never received as "verified".

So the rule is not "do not miss a failure". It is **do not normalize a failure with an explanation**. And it needs a machine judgement — a count or a hash comparison — behind it.

## The principles

### 1. A document cannot enforce; only a machine judgement did

Rules that were moved into a program were followed. Rules that stayed in prose were not, whether or not the model read them. Treat every rule as a candidate for relocation into a check, and treat prose as the fallback for what cannot be relocated.

### 2. Block only what is certain

One false positive and the developer starts using `--no-verify`; after that the entire hook is inert. The cost of a false alarm is not one wasted minute, it is every check you have.

```text
ADVISORY
→ WARN (observed on real work)
→ BLOCK (zero false positives observed)
```

Promote in that order only.

### 3. When uncertain, WARN — but do not let the most dangerous case end up the most weakly guarded

The obvious application of principle 2 is to downgrade anything doubtful to WARN. Applied without thought, that produces a matrix where trivial issues block and catastrophic ones merely warn.

**A silent failure must BLOCK.** A failure that is loud — a build error, an exception, a visible stack trace — can afford to be a WARN, because something else will surface it. A failure that returns HTTP 200 with zero rows, or renders an empty screen, or exits 0 having done nothing, has nothing else to surface it. Certainty is the reason to block; being unobservable is the reason it must be.

### 4. The escape hatch is an explicit marker, never an implicit one

Every check needs a way out, or the first legitimate exception kills it. But the way out must be a **declaration of intent** written by a person into the source:

```text
// gate:allow-rest   ← exempt, because someone stated the intent
```

Never exempt on the basis of circumstance — "the file already exists", "the value is non-empty", "this directory looks generated". An implicit exemption is indistinguishable from the defect it was meant to allow, and it silently widens until the check means nothing.

### 5. The rule ID belongs to the tool, not to the model

Give every acceptance criterion a stable ID, and make the **check print it on failure**. Do not ask the model to tag its own output with the ID or to declare which rule it satisfied — that step gets skipped, and small models skip it always.

Traceability then holds without the model's cooperation, which is the only kind of traceability worth having.

### 6. Put the basis for judgement in a project document, not in the model's head

A check that depends on the model deciding "does this project use X?" is a check the model can walk around by deciding differently next time. Record the decision once — in the project map or an equivalent state document — and have the check read it.

Recorded intent as the basis means the verdict is the same on Tuesday as it was on Monday, and it catches the model when it takes a different route to the same mistake.

### 7. Remove the decision and execution goes up

A check that requires the operator to choose which files to pass will not be run. Observed: across twelve sessions, checks were run essentially zero times, because deciding the arguments was itself a step, and that step got skipped.

The fix is a runner that takes no arguments and defaults to the obvious scope — files changed since the last check. Widen with an explicit flag when needed. Every decision you remove is a place the check can no longer be skipped.

### 8. Compile and test passing is not behaviour

A compiler does not check runtime dependencies. A test harness may not exercise the path the real deployment uses. Record artifact, rendered output, and runtime as separate layers, and never let one stand in for another. A layer that could not run is `PENDING` with a reason — never `PASS`.

### 9. Your own output fails the same way

The kit that enforces these rules broke them repeatedly: a template copied and not updated (twice), duplicated step numbers, an ambiguous phrase that caused a build failure downstream.

Two consequences, and they are not optional:

- **Verify artifacts by measurement**, not by reading them over. Compare counts, sizes, hashes.
- **Generate documents from a diff and a count.** Any number a human or a model copies by hand is a place the document goes stale silently. If a number must be written, record the rule by which it can be measured, so the claim is checkable at all.

This is also why a template the kit tells you to copy must pass the kit's own validation unmodified. When it does not, the only exit is to bypass the gate — and the failure message helpfully explains how.

## Publish the limits, do not hide them

Some rules cannot be checked by any program. "Did you output the five stages?" "Did you sync before starting?" "Did you actually read the file instead of assuming?" — that last one was the most frequently violated rule observed, and it is unverifiable from any artifact.

**Write those limits into the public documentation exactly as they are.** Concealing them buys nothing and costs trust. The advisory section of an enforcement matrix is not an embarrassment; it is the list of coverage gaps, which is the same thing as the roadmap for the next tool.

Three structural walls remain, and no principle here removes them:

- **A check only fires automatically if something triggers it.** No commit, no hook installed, work outside the repository root — it leaks. Reducing the friction of running it manually helps; it does not close the hole.
- **Without CI, there is no way to beat an uncooperative model.** Where CI is available, running the full check on push or pull request is the only mechanism that does not depend on cooperation. Ship a CI example.
- **Context compaction cannot be fixed with a tool.** Keeping the always-resident rules short is the only defence, which means every rule added must be weighed against making that file too large to survive.

## Applying this

Before adding a check to `enforcement-matrix.md`:

- [ ] the rule was moved into a program because prose did not hold it (principle 1);
- [ ] the verdict is deterministic and does not depend on wording or file naming;
- [ ] known-good material was run through it and produced zero findings;
- [ ] a silent failure blocks, and a loud one may warn (principle 3);
- [ ] the exemption path is an explicit marker, and no implicit exemption exists (principle 4);
- [ ] the tool prints the rule ID itself (principle 5);
- [ ] the basis for the verdict is a project document, not a model judgement (principle 6);
- [ ] the runner needs no arguments for the common case (principle 7);
- [ ] a self-test covers one passing and one deliberately failing fixture;
- [ ] the runner actually passes the check the arguments it needs, confirmed by running it;
- [ ] exit `0` pass, `2` validation failure, `1` tool error;
- [ ] the severity matches the evidence, and BLOCK is claimed only after zero false positives;
- [ ] anything this check still cannot catch is written into the advisory section rather than omitted.
