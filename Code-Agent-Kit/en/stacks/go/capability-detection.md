# Capability Detection — Go

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| language-version | the `go` directive in `go.mod`, and `go version` on the validating machine | answer within it | confirm with the owner | block anything sensitive to the 1.22 loop-variable change |
| http-router | a router package in `go.mod`, or `net/http` usage | use it | use `net/http` with a recorded reason | block introducing a router |
| data-access | a driver or query-builder requirement plus its wiring | use the existing layer | confirm with the owner | block data access invention |
| logging | a logging package, or `log/slog` usage | use the existing logger | use `log/slog` with a recorded reason | block introducing a logger |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
