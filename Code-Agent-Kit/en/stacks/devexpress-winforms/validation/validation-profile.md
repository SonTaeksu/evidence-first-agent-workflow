# Validation Profile — DevExpress WinForms

## Commands

`⟨verification required: this project's exact commands⟩`

The shape they take in this stack:

- **Restore.** Whatever makes the DevExpress assemblies available — a package feed, an installed product, or both. `⟨verification required: which, and what the build agent needs⟩` A restore that changes a lock file is a change, and must be reported.
- **Build.** The command the project's format allows; see `../../csharp-winforms/capability-detection.md`, because SDK-style and legacy projects do not build the same way. Exit code is the verdict.
- **Test.** The configured runner. Absence is reported, not assumed to pass.
- **Lint and analyzers.** Whichever are configured.

## Pass criterion

The **exit code**, in every case. A success message with a non-zero exit is a
failure, and treating the message as the verdict is the specific mistake this kit
was built to prevent.

## Which machine ran it

Record it. For most stacks this is a nicety; here it is load-bearing, because the
DevExpress licence is a property of the machine rather than of the source. "The
build passes" without a machine is a claim about somebody's laptop.

## Rendered-output evidence

Windows Forms produces no rendered document, and adding DevExpress does not create
one. The evidence route is the designer control tree, exactly as
[`../../csharp-winforms/references/ui-evidence-contract.md`](../../csharp-winforms/references/ui-evidence-contract.md)
describes.

One caveat, and it is not resolved: that route parses `*.Designer.cs` to extract a
control tree, and DevExpress designer output declares controls and their
containment differently from plain Windows Forms.
`⟨verification required: whether csharp-winforms/tools/extract_designer_tree.py
parses a DevExpress designer file correctly — run it against a real one and
compare the extracted tree with the file⟩` Until that is answered, treat a
rendered-output result from that tool on a DevExpress form as unconfirmed rather
than as a pass.

## Layers and what each proves

| Layer | Evidence | If it cannot run |
|---|---|---|
| Artifact / compile | build exit code and log, with the machine named | never skipped |
| Rendered output | designer control tree, subject to the caveat above | `PENDING` with the reason recorded |
| Runtime behaviour | UI automation, only when the capability is confirmed | `PENDING` with the reason recorded |
| Accessibility / colour | automation or screenshot evidence | `PENDING` with the reason recorded |

A layer that cannot run remains `PENDING` with a reason. It is never recorded as
`PASS`.

## Long-running processes

Launching the application for manual inspection is a long-running process. Start
and stop it through `tools/run-managed-service/run_service.py` (or its PowerShell
twin), which tracks the process by PID and start time and stops only that process
tree.

Never stop a process by image name. `Get-Process node | Stop-Process` and
`pkill -f node` also kill the MCP servers the agent itself depends on, and the
user's unrelated work.

## Recording a result

Command, exit code, the machine, and both versions — the .NET target and the
DevExpress release. Without them the result cannot be compared to anything later.
