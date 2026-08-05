# C# Windows Forms Reference Index

Route by task. Do not preload every reference.

| Task or component | Reference | Why it is needed |
|---|---|---|
| Stack adoption | `../STACK-INPUTS.md`, `../capability-detection.md` | the build command depends on the project format |
| Feature boundary | `../feature-model.md` | a `UserControl` shared by two screens is a shared dependency |
| Artifact creation | `../artifact-contract.md`, `../skeletons/README.md` | which file the designer owns |
| Layout evidence | `ui-evidence-contract.md` | Windows Forms has no rendered document |
| Threading and background work | `../communication-contract.md`, `pitfalls.md` | cross-thread access raises at runtime, not at compile time |
| Scaling and DPI | `verified-facts.md`, `pitfalls.md` | manifest settings override `App.config` |
| Known failures | `pitfalls.md` | verified failure modes and the stage each surfaces at |
| Version facts | `verified-facts.md` | what was verified, and when |
| Build and packaging | `../validation/build.md` | restore differs by package management |
| UI gates | `../validation/ui.md` | what counts as rendered-output evidence here |
