# C# Windows Forms Skeleton Sources

`MinimalApp/` is the known-good starting point. Copy the relevant minimal pattern; do not invent project, configuration, or manifest content from memory — those files are schema-sensitive and easy to get wrong in ways the compiler does not catch.

| File | What it fixes in place |
|---|---|
| `MinimalApp.csproj` | SDK-style project targeting `net472`, `OutputType` `WinExe`, direct Windows Forms references |
| `App.config` | `supportedRuntime` for 4.7.2 and the `DpiAwareness=PerMonitorV2` section |
| `app.manifest` | Windows 10 `supportedOS` declaration, without which the DPI key has no effect |
| `Program.cs` | `EnableVisualStyles` as the first call, `[STAThread]`, service injected at the entry point |
| `MainForm.cs` | behaviour only, with the UI-thread marshalling pattern |
| `MainForm.Designer.cs` | layout only, in the form the designer produces |
| `Services/` | the single boundary the form uses to reach anything outside itself |
| `screen-spec.json` | the declaration the designer-tree check compares against |

## Rules

- Record the source and version when copying into a project.
- Preserve the original here; modify the copy.
- Do not copy `net472` into a project whose detected target differs. Confirm the target first.
- Do not copy the manifest DPI approach from older material found elsewhere — this skeleton configures DPI in `App.config` on purpose.
- Exclude confidential skeletons from public repositories. Everything here is synthetic.

## Verifying the skeleton itself

```bash
python ../tools/extract_designer_tree.py --designer MinimalApp/MainForm.Designer.cs --output /tmp/tree.json
python ../tools/check_designer_spec.py --tree /tmp/tree.json --spec MinimalApp/screen-spec.json
```

The kit's own skeleton must pass the kit's own check. When it does not, the skeleton is the defect.
