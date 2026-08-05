# Rust

Services and tools in Rust with Cargo. The async runtime and the error model are load-bearing choices that pervade the code.

**State: `blocked`.** Not broken — waiting. The owner inputs in
`STACK-INPUTS.md` are unanswered, so `check-stack-readiness` derives `blocked`,
and `tools/check-last` deliberately skips a stack in that state so a
placeholder does not produce a false alarm on every run.

What is already here and useful:

- `references/pitfalls.md` — failures in this stack that produce no error message;
- `capability-detection.md` — how to tell what this project actually uses;
- `mcp/source-routing.md` — which documentation source is authoritative, and
  which must not be consulted.

To reach `ready`, answer `STACK-INPUTS.md` with evidence that exists. Evidence is
measured, not declared:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
