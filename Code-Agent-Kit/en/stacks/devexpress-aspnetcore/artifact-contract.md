# Artifact Contract — DevExpress for ASP.NET Core

What this stack produces, and what counts as evidence that it was produced.

## Build output

`⟨verification required: the artefacts this project's build produces and where —
the compiled application, whatever static assets are emitted or copied, and
whether report definitions are among the outputs or are stored elsewhere⟩`

Two things this stack produces that are easy to leave out of an artefact list:

- **the client-side assets** the components need. They are part of what has to be
  deployed, and a deployment that omits them produces a page that renders without
  the component and without an error;
- **the report definitions**, if this project stores them outside the assembly.
  They are then not build output at all, and treating them as if they were is how
  a deployment silently ships last month's reports.

## What is evidence

- A build or test **exit code**, with the command that produced it. A log line
  saying success while the exit code is non-zero is not evidence — it is the
  failure mode this kit exists to catch.
- A **restore that reached the feed**, for anything involving the DevExpress
  packages. A restore served entirely from a local cache proves that the cache
  has the package, which is a different claim.
- A file that exists at a stated path. `check-stack-readiness` resolves evidence
  paths, so a cited path that does not exist is treated as absent.
- For anything visual, a **rendered document or page actually produced by a run**,
  with the run recorded.

## What is not evidence

- A self-report with no command.
- Output from a development server. Development-mode success does not establish
  that a production build works, and in this stack it particularly does not
  establish that bundled assets are served the way production serves them.
- A page that loaded. A DevExpress component that failed to initialise leaves a
  page that loads.
- A screenshot with nothing to compare it against.
