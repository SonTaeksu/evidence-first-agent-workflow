# Capability Detection — Next.js

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| router-mode | presence of `app/` and/or `pages/` | follow that mode's rules | confirm with the owner | block routing or data-fetching work |
| major-version | the `next` entry in the lock file | answer within that version | confirm with the owner | block anything touching caching or rendering defaults |
| rendering-strategy | route segment configuration and `next.config` output mode | preserve the strategy | confirm with the owner | block changes that alter static or dynamic behaviour |
| data-layer | the data or ORM packages present and any server-only modules | use the existing layer | confirm with the owner | block direct data access invention |
| auth | an auth package plus its route handlers or middleware | integrate with it | escalate to the owner | block security changes |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
