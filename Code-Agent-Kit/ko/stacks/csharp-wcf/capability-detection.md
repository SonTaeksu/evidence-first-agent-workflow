# Capability Detection — WCF (.NET Framework 4.7.2+)

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| transport-binding | `<bindings>` in the service configuration | reuse the configured binding | confirm a binding with the owner before adding one | block endpoint changes |
| security-mode | binding `security` element and any credential configuration | keep the configured mode | escalate to the owner | block any change touching authentication or transport security |
| generated-proxy | a service reference folder or a `svcutil` invocation in the build | regenerate and adapt in a wrapper | hand-written contract client with a recorded reason | block contract invention |
| hosting-model | an `.svc` file plus IIS configuration, or a self-host entry point | follow the existing model | confirm with the owner | block hosting changes |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
