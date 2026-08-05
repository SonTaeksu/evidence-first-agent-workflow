# Capability Detection — Go + HTMX

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| language-version | the `go` directive in `go.mod`, and `go version` | answer within it | confirm with the owner | block loop-variable-sensitive work |
| htmx-version | the script tag or vendored asset | answer within it | confirm with the owner | block attribute-behaviour assumptions |
| template-engine | `html/template` usage or another engine in `go.mod` | use it | confirm with the owner | block introducing an engine |
| fragment-convention | existing handlers that branch on `HX-Request` | follow the established convention | confirm the convention with the owner | block inventing a fragment protocol |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
