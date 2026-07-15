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

A new stack profile should provide:

```text
STACK.md
AGENTS.stack.md
mcp/source-routing.md
validation/validation-profile.md
```

A sample application is optional for the first pull request but strongly recommended.

## Feedback is not required by the license

The project requests feedback because it is still under validation. This request does not add an extra license condition.