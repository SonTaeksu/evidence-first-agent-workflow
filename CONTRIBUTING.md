# Contributing

**English** | [한국어](CONTRIBUTING.ko.md)

Contributions are welcome, especially:

- failed adoption reports;
- deterministic gate improvements;
- corrections to project-state handling;
- new stack profiles;
- paired control/treatment results;
- translations.

## Before opening a pull request

1. Keep the core workflow independent from a specific technology stack.
2. Put stack-specific rules under `stacks/<stack-name>/`.
3. Do not include customer, employer, or proprietary project information.
4. Add validation evidence.
5. Update `current.md`, `history.md`, and Project Map when modifying the sample.
6. Explain unexpected files in the final Git Diff.

## New stack profile contract

Copy `stacks/_template/` — not `templates/stack-profile/` — and fill in every document the readiness validator requires:

```text
STACK.md                          references/_index.md
STACK-INPUTS.md                   references/pitfalls.md
AGENTS.stack.md                   references/verified-facts.md
SKILL.md                          skeletons/README.md
capability-detection.md           validation/validation-profile.md
feature-model.md
artifact-contract.md              STACK-READINESS.json
communication-contract.md
evidence-provenance.md
```

All fourteen documents must exist and be non-empty. A missing or empty one is a hard failure, not a warning.

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

Submit a stack as `ready` only when that command exits 0. `provisional` and `blocked` are legitimate states — say which one you are submitting and why.

Two rules that trip people up:

- **Evidence cannot be empty.** A resolved input or capability with no evidence fails validation. That is deliberate: it makes a fact filled in from model memory impossible to pass off as verified.
- **`declared_state` must match reality.** Declaring `ready` on a stack that derives to `blocked` is itself a failure.

A sample application is optional for the first pull request but strongly recommended.

## Adding a new check

A deterministic check earns a place in `docs/core/enforcement-matrix.md` only after it satisfies [`docs/core/gate-design-principles.md`](Code-Agent-Kit/en/docs/core/gate-design-principles.md):

- the rule was moved into a program because prose did not hold it;
- the verdict is deterministic and does not depend on wording or file naming;
- known-good material was run through it and produced zero findings;
- a **silent** failure blocks; a loud one may warn;
- the exemption path is an explicit marker written by a person, never an implicit circumstance;
- the tool prints its own rule identifier on failure — the model is not asked to tag anything;
- the basis for the verdict is a project document, not a model judgement;
- the runner needs no arguments for the common case;
- a `self_test.py` covers one passing and one deliberately failing fixture;
- the runner actually passes the arguments the check needs, confirmed by running it;
- exit `0` for pass, `2` for validation failure, `1` for tool error;
- whatever the check still cannot catch is written into the advisory section, not omitted.

Claim `BLOCK` only after observing zero false positives. One false alarm and the operator starts using `--no-verify`; after that the whole hook is inert.

Do not remove an advisory row to make the matrix look better. The advisory section is the list of coverage gaps, which is the same thing as the roadmap.

## Both language mirrors

`Code-Agent-Kit/en/` and `Code-Agent-Kit/ko/` hold identical relative paths. Only prose is translated; scripts are byte-identical. Verify before opening a pull request:

```bash
python Code-Agent-Kit/en/tools/check-mirror-parity/check_mirror_parity.py --root Code-Agent-Kit
python Code-Agent-Kit/en/tools/check-kit-selfcheck/check_kit_selfcheck.py --root Code-Agent-Kit/en
```

## Feedback is not required by the license

The project requests feedback because it is still under validation. This request does not add an extra license condition.