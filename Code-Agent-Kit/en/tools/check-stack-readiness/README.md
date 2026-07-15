# check-stack-readiness

Validates that a stack pack contains the documents, evidence, user confirmations, and capability decisions required before stack-dependent implementation.

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

Exit codes:

- `0`: ready, or provisional with `--allow-provisional`
- `2`: blocked, unresolved required input, or unaccepted provisional state
- `1`: tool or file error

This tool checks completeness, not truth. Evidence provenance and owner review establish truth.
