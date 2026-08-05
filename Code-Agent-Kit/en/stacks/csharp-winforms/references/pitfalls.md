# C# Windows Forms Verified Pitfalls

| Incorrect assumption | Verified rule | Evidence | Failure stage |
|---|---|---|---|
| A background task may update a label directly | Controls belong to their creating thread; marshal through `Invoke` or `BeginInvoke` | Microsoft Learn, `Control.InvokeRequired` | runtime |
| `InvokeRequired == false` means the call is safe | It is also `false` when the handle does not exist yet; check `IsHandleCreated` on a background thread | Microsoft Learn, same page | runtime, intermittent |
| Setting `CheckForIllegalCrossThreadCalls = false` fixes the exception | It removes the detection, not the race | Microsoft Learn, *How to handle cross-thread operations with controls* | runtime, later and worse |
| Layout edits in `*.Designer.cs` survive | The designer regenerates the file and hand edits are lost | `artifact-contract.md` | next designer save |
| A form `.resx` can be edited in a resource editor | Changes made outside the designer can be lost | Microsoft Learn, *What is Windows Forms Designer?* | build or next designer save |
| Adding DPI settings to the manifest is equivalent to `App.config` | The manifest overrides `App.config`, and the manifest route is no longer recommended | Microsoft Learn, *High DPI support in Windows Forms* | rendered output |
| `DpiAwareness=PerMonitorV2` alone enables high DPI | Windows 10 compatibility must also be declared in the manifest, and `EnableVisualStyles` must run first | Microsoft Learn, same article | rendered output |
| `<UseWindowsForms>true</UseWindowsForms>` enables Windows Forms on `net472` | That property belongs to the .NET Desktop SDK and a `net<n>.0-windows` target; on `net472` the assemblies are referenced directly | Microsoft Learn, *MSBuild reference for .NET Desktop SDK projects* | compile |
| `dotnet build` works for every .NET Framework project | It works for SDK-style projects with the targeting pack installed; a legacy `.csproj` needs MSBuild | `capability-detection.md` | compile |
| A successful build proves the screen is correct | Compilation says nothing about what the form contains; compare the designer control tree against the specification | `ui-evidence-contract.md` | rendered output |
| A declared control is a visible control | A control never added to a parent's `Controls` collection is invisible | `artifact-contract.md` | rendered output |
| The TLS protocol version should be pinned in code | From .NET Framework 4.7 the stack defers to the operating system | Microsoft Learn, *What's new in .NET Framework* | runtime, after an OS change |
| `BinaryFormatter` is fine for resources and settings | It is insecure and not trustworthy for deserialization | Microsoft Learn, *What is Windows Forms Designer?* | runtime, security |
