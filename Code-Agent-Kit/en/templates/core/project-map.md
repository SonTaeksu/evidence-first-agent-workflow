# Project Map

## Project Summary

- Repository:
- Default branch:
- Primary stack profiles:
- Project current summary:
- Last map verification:

## Features

| Feature Key | Current | History | Active Worklog | Entry Points | Stack |
|---|---|---|---|---|---|
| | | | | | |

## Architecture State

| Area | Current | History | Owner |
|---|---|---|---|
| System | `architecture/system.current.md` | `architecture/system.history.md` | |
| Database | `architecture/database.current.md` | `architecture/database.history.md` | |

## Environment Record

Fill this once, during bootstrap. Without it every agent and every session rediscovers the
same facts by trial and error, and each rediscovery is a chance to get it wrong.

| Item | Value | Why it matters |
|---|---|---|
| OS and shell | | the command separator is `;` in PowerShell and `&&` in cmd |
| Shell version | | PowerShell 5.1 has no `&&`, no `??`, no ternary |
| Does the repository path contain a space? | | if yes, every path must be quoted, and `cd` should be avoided |
| Python available, and under which name | | `python3` / `python` / `py` / none — no Python means the `.ps1` checks are the only gate |
| Node / package manager | | |
| Build tool and where its root file lives | | a backend in its own root needs `mvn -f` or the equivalent |
| SDK / toolchain paths | | record them; do not retype them |
| Long-command wrapper | | the generated `.bat` or `.sh`, git-ignored, one per machine |
| Fixed log filename | | so a check always knows which file to read |
| CI available? | | without CI, the commit hook is the only automatic enforcement |
| Commit hook installed? | | git hooks do not travel with a clone — a person installs it once per repository |

## Environment Capabilities

| Capability | Status | Evidence | Selected Path | Verified |
|---|---|---|---|---|
| | present / absent / unknown | | | |

`unknown` blocks implementation that depends on the capability.

## Shared File Reverse Index

| Shared File | Used By Features | Risk | Required Regression |
|---|---|---|---|
| | | | |

## Global Entry Points

- UI:
- API:
- Domain:
- Data:
- Tests:
- Validation:

## Routing Notes

-
