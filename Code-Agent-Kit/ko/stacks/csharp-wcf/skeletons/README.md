# Skeletons — WCF (.NET Framework 4.7.2+)

No skeleton is shipped for this stack.

That is deliberate rather than pending. A skeleton nobody has built is a liability:
it looks authoritative, it is copied, and its first real use is where the defect
is found. The toolchain for this stack was not available where this profile was
written, so there was no way to establish that a skeleton compiled.

When one is added, it must arrive with the build command and exit code that
produced it.

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
