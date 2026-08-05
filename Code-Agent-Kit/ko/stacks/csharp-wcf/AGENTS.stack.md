# Stack-Specific Agent Rules — WCF (.NET Framework 4.7.2+)

This file extends root `AGENTS.md`. It does not repeat it.

- Read `STACK-READINESS.json` before any stack-dependent implementation.
- A blocking capability with status `unknown` prohibits the dependent pattern.
  Not "proceed carefully" — prohibits.
- Route documentation lookups through `mcp/source-routing.md`. `microsoft-learn` is
  authoritative for this stack; `context7` is not, for the reason stated there.
- Use `references/verified-facts.md` and `references/pitfalls.md` instead of
  recall. Every entry there names where it was verified.
- Record every selected capability in the Project Map and repeat it in Gate
  Analysis.

## Stack prohibitions

- Do not state a version-sensitive fact from memory. Do not route WCF questions to a package-documentation server, and do not answer them from ASP.NET Core or gRPC documentation — the configuration model is unrelated.
- Do not report a validation as passed without the command and its exit code.
- Do not fill a row of `STACK-INPUTS.md` on the owner's behalf. An unanswered
  input is a blocked stack, which is a correct state.
