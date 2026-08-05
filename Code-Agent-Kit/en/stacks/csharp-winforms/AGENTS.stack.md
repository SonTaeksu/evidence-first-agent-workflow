# C# Windows Forms Agent Rules

This file extends root `AGENTS.md`.

- Run stack-readiness validation before adopting this profile in another project.
- Confirm the project format before writing a build command. SDK-style `net472` builds with MSBuild or `dotnet build`; a legacy `.csproj` builds with MSBuild only. Do not assume both.
- Do not hand-edit `*.Designer.cs` layout beyond what the designer would produce. It is regenerated and hand edits are lost. Behaviour belongs in the partial class file.
- Do not edit a form `.resx` outside the designer.
- Never touch a control from a thread that did not create it. Marshal through `Control.Invoke` or `BeginInvoke`, and check `IsHandleCreated` when `InvokeRequired` returns `false` on a background thread.
- Service and data code uses `ConfigureAwait(false)`. Only form code resumes on the UI thread.
- Configure DPI awareness in `App.config`, not in the manifest. The manifest overrides `App.config` and is no longer the recommended route.
- Keep `Application.EnableVisualStyles()` as the first call in the entry point.
- Route every server, file, or database call through the confirmed service entry point. Do not add a second one.
- Produce rendered-output evidence from the designer control tree. A build that succeeds is not evidence that the form contains anything.
- Report runtime behaviour as `PENDING` with a stated reason when no UI automation capability is confirmed. Do not claim it passed.

## Stack Prohibitions

- no `UseWindowsForms` on a `net472` target — it belongs to the .NET Desktop SDK and a `net<n>.0-windows` target;
- no `BinaryFormatter` for new serialization work, including resource payloads;
- no database, authentication, localization, or deployment change while its capability is `unknown`;
- no hard-coded TLS protocol version — .NET Framework 4.7 and later defer to the operating system;
- no bulk process termination by image name when a build or a launched application must be stopped.
