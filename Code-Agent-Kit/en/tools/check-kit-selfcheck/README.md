# check-kit-selfcheck

Runs the kit's own seed material through the kit's own validation. A template the kit tells the reader to copy must pass unmodified; when it does not, the only exit is to bypass the gate.

```bash
python tools/check-kit-selfcheck/check_kit_selfcheck.py --root .
python tools/check-kit-selfcheck/self_test.py
```

Two assertions:

- **Seed templates.** Each documented copy source is copied exactly as instructed and validated. A blank seed is *supposed* to report `blocked`, because its inputs are deliberately unknown, so unresolved inputs and capabilities are ignored. Only structural failures count: a missing or empty required document, an array of the wrong type, and a declared state that contradicts the derived state.
- **Shipped stacks.** A stack whose manifest declares `ready` must validate as ready.

Exit codes:

- `0`: the kit passes its own checks
- `2`: a seed or a shipped stack is blocked by the kit's own validation
- `1`: tool or file error

Use `--seed <path>` to override the default copy sources. Rationale in [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §4.
