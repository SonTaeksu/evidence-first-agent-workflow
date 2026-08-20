# Stack Profile — DevExpress for ASP.NET Core

DevExpress components on ASP.NET Core MVC and Razor Pages, plus DevExpress
Reporting hosted on the web. v24.2 or later. Blazor is out of scope; see
`README.md`.

## Runtime and framework versions

`⟨verification required: the exact .NET target framework, the .NET SDK on the
validating machine, and the exact DevExpress package version, read from this
project's project files and restore output⟩`

A supported range is not a version, and "v24.2 or later" is a range. The
DevExpress version decides which components exist, which of them are current and
which are superseded, and — separately — whether the documentation endpoint in
`mcp/source-routing.md` can be pinned at all. See `STACK-INPUTS.md`.

## Directory structure

The shape below is the ASP.NET Core shape; nothing here is DevExpress-specific
except what it has to carry.

- the application entry point, where services are registered — the Report
  Designer and the Document Viewer do not work without explicit registration,
  so this file is load-bearing for any reporting change;
- `Controllers/` and `Views/`, or `Pages/`, or both — which one this project uses
  is a detected capability, not an assumption;
- the layout and any bundling or asset configuration — DevExpress components
  need client-side assets delivered, and the mechanism differs by project;
- wherever report definitions live. That location is a project decision, and it
  is the thing `ReportStorageWebExtension` is written against.

`⟨verification required: this project's actual layout, including where report
definitions are stored and whether they are compiled in, on disk, or in a
database⟩`

## Package source

The DevExpress packages come from a **private NuGet feed that requires
credentials**. This is a property of the product, not of any project.

What follows from it, and what a project must confirm rather than assume:

- which feed URL this project restores from;
- where the credential comes from on a developer machine, and separately on the
  build agent — they are usually not the same mechanism;
- whether a clean restore, with no warm package cache, actually succeeds.

`⟨verification required: all three, on the machine that runs validation⟩`

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

Whatever it is, a build that restores entirely from cache has not exercised the
feed. That is worth saying because it is the failure that reaches CI first.

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- **DevExpress for ASP.NET Core exists in two shapes.** There are server-side
  controls with their tag helpers, rendered and configured on the server, and
  there are DevExtreme's client-side widgets, configured in JavaScript in the
  browser. They are different products with different configuration surfaces and
  different documentation. Which one a project uses is a fact to detect, and a
  project may well use both in different places.
- **The Report Designer and the Document Viewer require explicit service
  registration.** They are not enabled by referencing a package. A host that
  omits the registration typically fails at request time rather than at build
  time.
- **They also require client-side assets to be delivered.** The viewer and the
  designer are browser components; if the static or bundled resources are not
  served, the page renders without them and the server reports nothing.
- **Report storage is something a project implements.** `ReportStorageWebExtension`
  is an extension point, not a working default. Until a project provides one, the
  designer has nowhere to open reports from and nowhere to save them to.
- **Reporting spans desktop and web.** This profile covers the web host. A
  WinForms or WPF host answers the same questions differently and must not be
  answered from here.
- **The DevExpress API is versioned and this profile is not a substitute for
  looking it up.** Do not state a component name, a property name or a
  registration call from memory; route it through `mcp/source-routing.md`.
