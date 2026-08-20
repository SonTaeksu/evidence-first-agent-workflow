# Capability Detection — DevExpress for ASP.NET Core

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

This stack has more capabilities than most because more of it is optional. A
DevExpress reference in a project file says almost nothing on its own: it does
not say which component line is in use, it does not say whether reporting is
hosted, and it certainly does not say whether the pieces reporting needs are
present.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | the resolved DevExpress package version from restore output or the lock file — not the range in the project file | answer within that version's rules and pin documentation lookups to it | confirm with the owner | block any version-sensitive API use; block pinning an MCP documentation version |
| ui-component-layer | which DevExpress packages are referenced, and whether views configure components on the server or scripts configure widgets in the browser | follow the layer already in use in that area of the codebase | confirm with the owner before introducing either | block adding a component of either kind |
| page-model | whether the project has controllers with views, page models, or both | follow the existing model for that area | confirm with the owner | block adding a page or a controller |
| reporting-host | the reporting service registration in application startup, and the endpoints or handlers the viewer and designer are served through | extend the existing host | report that reporting is not hosted rather than adding a host | block adding or changing a report viewer or designer host |
| report-storage | an implementation deriving from `ReportStorageWebExtension`, and its registration | use the existing storage and its addressing convention | report that no storage exists — the designer cannot open or save without one | block opening or saving a report from the designer |
| client-resource-delivery | how static and bundled assets reach the browser: the static-file configuration, the layout, and any bundling configuration | add assets through the existing mechanism | confirm with the owner | block adding a component that needs client-side assets |

## Why `ui-component-layer` comes first

DevExpress for ASP.NET Core is two products under one brand: server-side controls
with tag helpers, configured and rendered on the server, and DevExtreme's
client-side widgets, configured in JavaScript and rendered in the browser. They
have separate documentation, separate configuration surfaces and separate failure
modes.

An agent that has not settled which one a project uses will produce code that
reads correctly, compiles in some cases, and belongs to the other product. That
is why this capability blocks rather than warns.

A project may use both, in different areas. So the detection is per area of the
codebase, and the answer is recorded per area — not once for the repository.

## Detection is reading, not inferring

- A package reference is evidence that a package is referenced. It is not
  evidence that a component from it is used, nor that reporting is hosted.
- A registration call in startup is evidence that something was registered. What
  it registers is a version-sensitive fact and is looked up, not recalled.
- An asset referenced in a layout is evidence that the layout asks for it. Whether
  it is served is a separate check.

`⟨verification required: the exact package identifiers, registration calls and
asset paths this project uses — read them from the project, and confirm the API
names through dxdocs rather than from this document⟩`

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
