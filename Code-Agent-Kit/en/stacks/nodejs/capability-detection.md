# Capability Detection — Node.js

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| module-system | `type` in `package.json` and the extensions in use | follow it consistently | confirm with the owner | block adding a module in the other system |
| runtime-version | `node --version` on the validating machine, plus the lock file | answer within that version | confirm with the owner | block use of version-sensitive APIs |
| http-framework | a framework in the dependencies and its wiring | use it | use `node:http` directly with a recorded reason | block introducing a framework |
| test-runner | a runner in devDependencies, or `node:test` usage | run the configured runner | report that none exists | block claiming tests pass |
| typescript | a `tsconfig` and a build or loader step | keep types and the build step | plain JavaScript | block a mixed-language change |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
