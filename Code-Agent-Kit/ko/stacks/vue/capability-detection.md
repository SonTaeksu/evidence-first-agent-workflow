# Capability Detection — Vue.js

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| major-version | the `vue` entry in the lock file — not `package.json`, which may name a range | answer within that version's rules | confirm with the owner | block any version-sensitive API use |
| build-tool | a bundler config file and the package scripts | use the configured build | confirm with the owner | block build configuration changes |
| state-management | a store package in the dependencies and a store directory | use the existing store | component-local state | block introducing a store library |
| test-runner | a runner in devDependencies and a test script | run the configured runner | report that no runner exists | block claiming tests pass |
| typescript | a `tsconfig` plus `lang="ts"` in components | keep types | keep plain JavaScript | block a mixed-language change |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
