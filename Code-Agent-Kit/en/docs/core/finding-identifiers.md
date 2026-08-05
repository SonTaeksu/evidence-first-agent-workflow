# Finding Identifiers

Every check prints its own identifier when it fails. The model is never asked to declare which rule it satisfied.

## The rule

```text
<tool-directory-name>:<finding-id>
```

```text
check-shell-safety:ps1-bom
check-mirror-parity:orphan-path
check-stack-readiness:missing-document
csharp-winforms/designer-spec:missing-control
```

The tool directory name is the namespace. Tool directories are already unique, so two checks cannot collide, and a stack pack that ships its own validator needs no central allocation.

## Why the tool owns it, not the model

Asking a model to tag its output with the rule it satisfied is a step, and steps get skipped — small models skip this one every time. An identifier the *tool* prints survives regardless of whether the model cooperated, and that is the only kind of traceability worth having.

This also makes two machine checks possible that are otherwise impossible:

- **Documented but not implemented.** A rule listed in `enforcement-matrix.md` whose identifier no tool ever emits is a rule that does not run. The matrix says it is enforced; nothing enforces it.
- **Implemented but not documented.** An identifier a tool emits that appears in no matrix row is an undocumented verdict — the operator sees a failure with no way to look up what it means.

Both were observed as real defects before identifiers existed: a check that ran correctly but printed no identifier could not be traced to its rule, and a rule that lived only in a handoff document was absent from the matrix for three releases.

## Writing a finding id

- lowercase, hyphenated, no spaces;
- names the **condition**, not the fix — `orphan-path`, not `add-missing-file`;
- stable. **Do not rename one.** A self-describing identifier is tempting to improve; every rename breaks every document, worklog, and suppression that referenced it. If a name turns out wrong, add the better one and keep the old one emitting alongside until nothing references it.

## Format of a failure line

```text
<path>:<line>: [<tool>:<finding-id>] <what is wrong> — <why it matters>
```

The identifier goes in brackets so it can be extracted mechanically. Everything after it is for the person reading.

## The bracketed prefix is a contract

`[<tool>:<finding-id>]` at the head of a failure line is a **stable interface**, not formatting. Other tools read it. Changing it, or emitting a failure without it, breaks those readers.

Two obligations follow.

**A machine consumer matches the identifier, never the prose.** Everything after the bracket is for the person reading and may be reworded at any time. A consumer that matches a sentence dies the next time somebody improves that sentence, and nothing is watching — the check keeps exiting 0 and looks healthy.

This is not hypothetical. `check-kit-selfcheck` classified the readiness validator's failures by prose prefix (`"Missing or empty required document:"`). When the validator's messages gained identifiers, every prefix stopped matching, and its seed assertion became completely inert: deleting a required document from a seed reported CLEAN and exit 0 for three releases. Its own self-test caught this; nothing ran the self-test.

**Changing the format is not done until every consumer is updated.** Finding the consumers is a survey, not a guess:

```bash
grep -rn "startswith(\|importlib\|\.stdout" --include=*.py tools/
grep -rn "grep\|Select-String" --include=*.sh --include=*.ps1 --include=*.yml .
```

Prefer not to have consumers that parse at all. Where a tool needs another tool's verdict, invoking it as a subprocess and reading identifiers off its output is better than importing its internals: the CLI is the layer every agent, hook and CI job actually uses, so exercising it keeps this contract honest, while an imported function couples to a signature nobody else depends on — and cannot be mirrored by a `.ps1` twin at all.

## What this is not

An identifier is not a severity. `check-shell-safety:ps1-bom` blocks; another finding from the same tool may only warn. Severity lives in `enforcement-matrix.md`, next to the identifier.

An identifier is not a promise that the check is correct. It is a handle for talking about the check.

## Verifying the twins agree

`.py` and `.ps1` implementations of the same check must produce the **same exit code and the same identifier set** on the same input. Comparing exit codes alone is not enough: two implementations can both exit 2 for different reasons and look identical.

```bash
python tools/check-script-parity/check_script_parity.py --root .
```

See [`gate-design-principles.md`](gate-design-principles.md) §5.
