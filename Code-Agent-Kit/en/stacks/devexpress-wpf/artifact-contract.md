# Artifact Contract — DevExpress WPF (v24.2+)

What this stack produces, and what counts as evidence that it was produced.

## Build output

`⟨verification required: the artefact this project's build produces and where⟩`

## What is evidence

- A build or test **exit code**, with the command that produced it. A log line
  saying success while the exit code is non-zero is not evidence — it is the
  failure mode this kit exists to catch.
- A file that exists at a stated path. `check-stack-readiness` resolves evidence
  paths, so a cited path that does not exist is treated as absent.
- For anything themed: the **published output**, listing the theme assemblies
  actually present. This stack needs that specifically, because the compiled code
  does not reference them and the build cannot notice they are gone.

## What is not evidence

- A self-report with no command.
- Output from a development server. Development-mode success does not establish
  that a production build works.
- A screenshot with nothing to compare it against.
- A screenshot taken on a developer machine offered as proof that the theme
  deploys. That machine has the full DevExpress installation on it; the target
  machine has whatever the build copied. These are different claims and only the
  second one matters.
