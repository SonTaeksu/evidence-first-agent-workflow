# Skeletons — DevExpress WPF (v24.2+)

No skeleton is shipped for this stack.

That is deliberate rather than pending, and here it is also a licensing
consequence. DevExpress assemblies are restored from a licensed feed, so a
skeleton could not have been built where this profile was written and could not
be distributed with the kit even if it had been. A skeleton nobody has compiled
is a liability: it looks authoritative, it is copied, and its first real use is
where the defect is found.

`../../csharp-wpf/skeletons/` holds a plain WPF skeleton. It is the right starting
point for the parts of an application that are not DevExpress, and it carries the
same caveat — it has not been compiled either.

When a skeleton is added here, it must arrive with the build command and exit
code that produced it, and with the DevExpress version that was restored.

## What a skeleton here must contain

- the smallest thing that builds and runs;
- the project or manifest file, since that is where version-sensitive settings
  live and where they are most often wrong;
- one example of each convention a generated file has to follow;
- the theme application point, and the published output showing the theme
  assemblies present — without that, the skeleton demonstrates the failure it
  should be preventing.

## What it must not contain

- a version pinned to whatever was current when it was written, presented as a
  requirement;
- a library the project has not chosen, which makes the skeleton a decision
  rather than a starting point — in this stack that includes the choice between
  the DevExpress MVVM framework and a third-party one.
