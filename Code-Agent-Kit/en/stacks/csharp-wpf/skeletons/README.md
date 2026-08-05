# Skeletons — WPF (.NET Framework 4.7.2+)

A minimal skeleton is present under this directory.

**It has not been compiled.** The window that wrote it had no MSBuild and no
.NET Framework targeting pack, so the only honest statement is that the files
exist and are internally consistent. Build it once on a machine that has the
toolchain, record the command and exit code in `STACK-INPUTS.md`, and that turns
this from a claim into evidence.

## What a skeleton here must contain

- the smallest thing that builds and runs;
- the project or manifest file, since that is where version-sensitive settings
  live and where they are most often wrong;
- one example of each convention a generated file has to follow.

## What it must not contain

- a version pinned to whatever was current when it was written, presented as a
  requirement;
- a library the project has not chosen, which makes the skeleton a decision
  rather than a starting point.
