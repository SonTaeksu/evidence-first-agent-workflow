# Capability Detection — Elixir

A capability is detected from the repository, never assumed. The Unknown Rule is
what applies when detection is inconclusive, and it blocks rather than guesses —
one wrong guess costs more than the pause.

| Capability | Detection | Present Path | Absent Path | Unknown Rule |
|---|---|---|---|---|
| versions | `elixir` requirement in `mix.exs`, `mix.lock`, and `elixir --version` on the validating machine | answer within them | confirm with the owner | block version-sensitive work |
| phoenix-liveview | the `phoenix` and `phoenix_live_view` entries in `mix.lock` | answer within those versions | confirm with the owner | block lifecycle-sensitive LiveView work |
| ecto | the `ecto` entries plus a repo module and migrations | use the existing repo and migrations | confirm with the owner | block data access invention |
| project-shape | an `apps/` directory for an umbrella, or its absence | follow it | confirm with the owner | block restructuring |
| asset-pipeline | the configured asset tooling in `mix.exs` and `config` | use it | confirm with the owner | block introducing a bundler |

Every capability a feature relies on must appear in the Project Map and be
repeated in Gate Analysis, so that a later reader can see which branch was taken
and why.
