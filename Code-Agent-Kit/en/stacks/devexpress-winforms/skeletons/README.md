# Skeletons — DevExpress WinForms

No skeleton is shipped for this stack.

That is deliberate rather than pending, and here the reason is concrete: the
DevExpress assemblies are a licensed dependency and were not available in the
environment where this profile was written, so there was no way to establish that
a skeleton compiled. A skeleton nobody has built is a liability — it looks
authoritative, it is copied, and its first real use is where the defect is found.

The plain Windows Forms skeleton in
[`../../csharp-winforms/skeletons/MinimalApp/`](../../csharp-winforms/skeletons/)
is real and does compile. It is the right starting point for the parts of a
DevExpress project that are not DevExpress: project file, runtime configuration,
manifest, entry point, and the separation of behaviour from designer-generated
layout.

When a DevExpress skeleton is added, it must arrive with the build command and
exit code that produced it, and with the DevExpress release it was built against.

## What a skeleton here must contain

- the smallest thing that builds and runs;
- the project or manifest file, since that is where version-sensitive settings
  live and where they are most often wrong;
- the DevExpress references with a resolved version, not a range;
- whatever licensing artefact the build actually required, with a note on how the
  licence reached the machine;
- one example of each convention a generated file has to follow.

## What it must not contain

- a DevExpress version pinned to whatever was current when it was written,
  presented as a requirement;
- a control the project has not chosen, which makes the skeleton a decision rather
  than a starting point;
- a licence key, a licence file's contents, or anything else that is the
  organisation's entitlement rather than the kit's material.
