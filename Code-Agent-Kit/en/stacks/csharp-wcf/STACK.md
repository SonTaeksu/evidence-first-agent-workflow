# Stack Profile — WCF (.NET Framework 4.7.2+)

SOAP and net.tcp services on WCF, targeting .NET Framework 4.7.2 or newer.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `I*.cs` — the service contract: `[ServiceContract]` with `[OperationContract]` members.
- `*.svc` / host project — IIS-hosted or self-hosted; which one changes the configuration source.
- `App.config` / `Web.config` — `<system.serviceModel>`: bindings, behaviors, endpoints. Behaviour lives here, not in code.
- Generated client — `svcutil` or a Visual Studio service reference; regenerated output overwrites edits.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- A contract change is a wire-format change. Both sides must be regenerated, and an unregenerated client fails at runtime, not at build.
- `DataContractSerializer` orders members alphabetically unless `Order` is set on `[DataMember]`. Order is part of the contract.
- An exception that is not declared as a `[FaultContract]` reaches the client as a generic fault with no detail.
- `InstanceContextMode`, `ConcurrencyMode` and session support interact; changing one without the others produces intermittent behaviour.
- Metadata (MEX) exposure is a configuration decision with a security consequence.
