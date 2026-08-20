# Skeletons — DevExpress for ASP.NET Core

No skeleton is shipped for this stack.

That is deliberate rather than pending, and here it is also unavoidable. A
skeleton nobody has built is a liability: it looks authoritative, it is copied,
and its first real use is where the defect is found. The DevExpress packages come
from a **private feed that requires credentials**, so a skeleton for this stack
cannot be built — or verified by a reader — without an entitlement this kit does
not have and cannot ship.

A skeleton that was never restored, never compiled and never rendered would be
exactly the invented material this kit exists to prevent.

When one is added, it must arrive with the build command and exit code that
produced it, and with the DevExpress version it was built against.

## What a skeleton here must contain

- the smallest thing that builds and runs;
- the project file, since that is where the target framework and the DevExpress
  package version live, and where they are most often wrong;
- the feed configuration, with the credential referenced rather than embedded;
- the service registration reporting needs, if reporting is in scope for the
  skeleton — because omitting it is the most common way a working reference
  becomes a broken one;
- the asset delivery, for the same reason;
- one example of each convention a generated file has to follow.

## What it must not contain

- a licence key, a credential, or a feed URL that carries one;
- a version pinned to whatever was current when it was written, presented as a
  requirement;
- components from both the server-side and the client-side line mixed together,
  which turns the skeleton into a source of exactly the confusion
  `references/pitfalls.md` opens with;
- a library the project has not chosen, which makes the skeleton a decision
  rather than a starting point.
