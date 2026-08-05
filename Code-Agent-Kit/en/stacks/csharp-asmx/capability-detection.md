# Capability Detection — ASMX Web Service 2.0 (.NET Framework 4+)

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| soap-version | `Web.config` protocol configuration and the generated WSDL | keep the configured version | confirm with the owner | block changing the contract surface |
| proxy-generation | a `wsdl.exe` step or a Web Reference folder | regenerate and adapt in a wrapper | hand-written client with a recorded reason | block contract invention |
| authentication | IIS and `Web.config` authentication configuration | integrate with the configured mechanism | escalate to the owner | block security changes |
| external-consumers | owner statement, plus any published WSDL | treat the contract as frozen and version additively | change in place once the owner confirms no consumers | block any breaking change |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
