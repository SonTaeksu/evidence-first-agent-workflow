# Artifact Contract — WCF (.NET Framework 4.7.2+)

What this stack produces, and what counts as evidence that it was produced.

## Build output

`⟨verification required: the artefact this project's build produces and where⟩`

## What is evidence

- A build or test **exit code**, with the command that produced it. A log line
  saying success while the exit code is non-zero is not evidence — it is the
  failure mode this kit exists to catch.
- A file that exists at a stated path. `check-stack-readiness` resolves evidence
  paths, so a cited path that does not exist is treated as absent.

## What is not evidence

- A self-report with no command.
- Output from a development server. Development-mode success does not establish
  that a production build works.
- A screenshot with nothing to compare it against.
