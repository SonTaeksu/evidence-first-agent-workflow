# Pitfalls — DevExpress for ASP.NET Core

Each of these is a property of the technology, verifiable independently of any
project. They are collected because they share one characteristic: **the failure
is silent, or the error message names something other than the cause.** A stack
whose failures announce themselves does not need a list like this.

## Two component lines share one brand

DevExpress ships server-side controls with tag helpers for ASP.NET Core, and it
ships DevExtreme's client-side widgets. Both are "DevExpress components", both
appear in the same documentation site, and both have samples that look like the
answer. A snippet from the wrong line does not announce itself: it is valid code
for a product this project is not using. Settle `ui-component-layer` before
writing anything — see `capability-detection.md`.

## A restore from cache proves nothing about the feed

The DevExpress packages come from a private feed that needs credentials. A
developer machine with the packages already in its local cache restores without
ever contacting the feed, so a broken or unauthenticated feed configuration stays
invisible until a clean agent tries. The failure then arrives in CI, in someone
else's change.

The check is a restore with no warm cache, on the machine that matters.
`⟨verification required: how this project performs one, and on which agent⟩`

## Referencing the reporting packages does not host reporting

The Report Designer and the Document Viewer need **explicit service
registration**. Adding the package reference compiles, and the application starts.
What is missing surfaces when a request actually needs the service — which is
after deployment, on a page nobody exercised in the build.

`⟨verification required: the exact registration this project's DevExpress version
requires, looked up through dxdocs — do not write it from memory⟩`

## Registration without client assets renders an empty page

The viewer and the designer are browser components. If the static or bundled
resources they need are not served, the server returns a page with a status of
200, the request log looks healthy, and the component is simply not there. The
diagnosis is in the browser console, not in the application log.

Two separate things to confirm, because either alone is not enough: that the
assets exist in the deployed output, and that the application is configured to
serve them at the path the page asks for.

## `ReportStorageWebExtension` is an extension point, not a default

Report storage is something a project implements. Until it does, the designer has
nowhere to open reports from and nowhere to save them to. The characteristic
shape of the failure is partial: an unimplemented member is not a build error, so
the designer loads, lists nothing or lists something, and then fails at the moment
a user clicks save — the point at which their work is lost rather than the point
at which the defect was introduced.

Implement every member the extension point defines, and test the save path
specifically. It is the one nobody exercises.

## Report definitions bind to field names, and nothing checks them

A report names the fields it binds to. Rename a column, change a result shape, or
reshape a view model, and the compiler is satisfied while the report fails at
render time. The report is also usually not in the same review as the schema
change, so the two never meet until a user opens the report.

Any change to a data shape a report consumes is a change to the report. Treat it
as a shared-file change; `feature-model.md` says why.

## Reports authored for a desktop host are not the same question

DevExpress Reporting covers desktop and web. Capabilities available in a WinForms
or WPF host — interactivity, export paths, designer behaviour — do not transfer
to the web host by default, and an answer written for one does not hold for the
other. This profile covers the web host only.

## A documentation search under the wrong `technologies` value still answers

`devexpress_docs_search` takes a closed enum, and reporting is a **separate**
value: `XtraReports`, not something inside `AspNetCore`. A reporting question sent
with `AspNetCore` alone does not fail — it searches the component corpus and
returns component topics, which are real DevExpress documentation about the wrong
subject. The mistake is invisible in the answer; it is only visible in the
arguments. Send both values for reporting, and see `mcp/source-routing.md` for the
measured enum. A value that is *not* in the set behaves differently and more
kindly: the call is rejected against the schema rather than answered.

## Version pinning for documentation stops at v24.2

The documentation endpoint accepts a version pin no earlier than v24.2. On an
older codebase there is no supported way to pin, so a lookup returns whatever the
current documentation says and the mismatch is not signalled. That is not a
workaround to route around; it is a reason to treat every version-sensitive
answer on such a project as unresolved. See `mcp/source-routing.md`.
