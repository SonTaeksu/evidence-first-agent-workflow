# Stack Profile — ASMX Web Service 2.0 (.NET Framework 4+)

Legacy ASP.NET Web Services (`.asmx`) on .NET Framework 4 or newer. Microsoft documents ASMX as a legacy technology; it is here for maintaining what exists, not for new work.

## Runtime and framework versions

`⟨verification required: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

A supported range is not a version. See `STACK-INPUTS.md`.

## Directory structure

- `*.asmx` + `*.asmx.cs` — `[WebService]` class with `[WebMethod]` members.
- `Web.config` — the ASP.NET pipeline; protocol support is configured here.
- Generated proxy — `wsdl.exe` or an 'Add Web Reference' proxy deriving from `SoapHttpClientProtocol`.

## Build commands

`⟨verification required: the project's own build command and its pass criterion⟩`

## Test commands

`⟨verification required: the project's own test command and its pass criterion⟩`

## Known constraints

These are properties of the technology and hold regardless of the project.

- Serialization is `XmlSerializer`, not `DataContractSerializer`. Types need a public parameterless constructor and public settable members; private state does not round-trip.
- Contracts are classes, not interfaces. There is no interface-based contract as in WCF.
- A nullable value type needs the `XxxSpecified` companion property pattern, or absence and default are indistinguishable.
- The WSDL is generated from the code, so a signature change is a contract change with no separate artefact to review.
- SOAP 1.1 and 1.2 support is a configuration matter and affects the request the client must send.
