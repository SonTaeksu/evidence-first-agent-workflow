# C# Windows Forms Validation Profile

## Verification commands (mandatory)

Completion (`prompts/GATE.md` §5) is not reached until these pass. A self-report is not a substitute for an exit code.

| Gate | Command (copy-paste) | Pass criterion |
|---|---|---|
| Stack readiness | `python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/csharp-winforms` | exit 0 |
| Restore | `msbuild {PROJECT}.csproj /t:Restore` | exit 0 |
| Build / compile | `msbuild {PROJECT}.csproj /t:Build /p:Configuration=Release` | exit 0 **and** no `error` or `warning as error` marker in the log |
| Unit / integration | `vstest.console.exe {OUTDIR}\{PROJECT}.Tests.dll` | exit 0, all target tests pass |
| Rendered output | `python stacks/csharp-winforms/tools/extract_designer_tree.py --designer {FORM}.Designer.cs --output {EVIDENCE}\tree.json` then `python stacks/csharp-winforms/tools/check_designer_spec.py --tree {EVIDENCE}\tree.json --spec {EVIDENCE}\spec.json` | exit 0 |
| Tool self-test | `python stacks/csharp-winforms/tools/self_test.py` | exit 0 |
| Scope / state | Git-scope and document-sync tools | exit 0 |

An SDK-style project may substitute `dotnet build` and `dotnet test`. A legacy `.csproj` may not. Confirm `project-format` in `capability-detection.md` before choosing.

Keep paths as `{PLACEHOLDERS}`. Never commit an absolute SDK, vendor, or user path — the sanitization gate blocks it.

## Layers and what each proves

| Layer | Evidence | If it cannot run |
|---|---|---|
| Artifact / compile | MSBuild exit code and log | never skipped |
| Rendered output | designer-tree comparison | never skipped; the tree is always available |
| Runtime behaviour | UI automation, only when the capability is confirmed | `PENDING` with the reason recorded |
| Accessibility / colour | automation or screenshot evidence | `PENDING` with the reason recorded |

A layer that cannot run remains `PENDING` with a reason. It is never recorded as `PASS`.

## Long-running processes

Launching the application for manual inspection is a long-running process. Start it through the managed runner and stop only that process; never terminate by image name.

```bash
python tools/run-managed-service/run_service.py start --name app --cwd {dir} -- {OUTDIR}\{PROJECT}.exe
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name app
```

## Failure signals to read in the build log

- `MSB3644` — the targeting pack for the declared framework is not installed. The code is not the defect.
- `CS0246` on a Windows Forms type — the `System.Windows.Forms` reference is missing, or the project format was misdetected.
- `MSB4803` — an MSBuild task unsupported by `dotnet build` on a legacy project. Use MSBuild.
- A build that succeeds while the designer-tree check fails — compilation never proved the screen contents.
