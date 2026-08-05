# 7 — Update the kit in a project

Use this when a project already has the kit installed and a newer version exists. Not for a first install — for that, copy the language mirror and run `0-sync-and-orient.md`.

## Why this has its own procedure

An installation that falls behind means the newest rules and checks **are not running in that project**, and nothing says so. Observed: a project sat two revisions behind while its own documentation described checks that were not present. Every one of those checks was silently off.

The failure mode is specific and it has happened: an update is attempted, the agent sees files that already exist, treats "already present" as "already correct", writes six of thirty-three files, and reports **install complete** — leaving the project in a mixed state that nobody can distinguish from a good one.

## 1. Establish whether an update is needed

Compare the version the project has against the version available. If the kit records a version banner, read it; otherwise compare the manifest.

```bash
python tools/check-kit-installation/check_kit_installation.py --root .
```

Different version, or a missing required file, means update.

## 2. Copy — never transcribe

```bash
python install-kit.py --target /path/to/your-project --mode core --stack <your-stack> --overwrite
```

> **Do not have the agent read each file and write it back.** File contents pass through the context twice — once being read, once being written — and past the compaction threshold the agent starts inventing content that looks plausible. This is not hypothetical: in one observed session eleven files were written that had never been read, including a fake commit hook that exited 0, and the completion report said every file had been fetched correctly.
>
> Copying is a filesystem operation. Nothing passes through the model, so there is nothing to invent.

## 3. Overwrite the kit; never overwrite what a person wrote

| What | Rule |
|---|---|
| Kit content — `prompts/`, `docs/core/`, `tools/`, `scripts/`, `stacks/_template/`, `AGENTS.md` | **overwrite unconditionally** |
| Project state — `docs/project-map.md`, `docs/features/*`, `docs/architecture/*`, `docs/worklogs/*` | **never overwrite** — create only when absent |
| Your stack pack | overwrite only the parts you have not customised; diff first |

> ⚠️ **"The file already exists" is not a reason to skip it.** A version increase means the *contents* of existing files changed. That is the whole point of updating.

## 4. Judge completion by counting, not by reporting

```bash
python tools/check-kit-installation/check_kit_installation.py --root /path/to/your-project
python tools/check-last/check_last.py --root /path/to/your-project --all
```

Report the numbers side by side, and **separate what was written from what was skipped**:

```text
written N / skipped because already present M / not received 0
```

Reporting a skipped file as installed is the failure this line exists to prevent — one observed run listed eleven documents as installed that it had never touched. "I installed N files" must be a count taken by listing the tree again, not a number recalled from earlier in the session.

If the update was split across sessions, do the full count **once at the end**. A partial install breaks quietly in the next session.

## 5. Re-arm the commit hook

Files on disk do not activate the hook. Git hooks live in `.git/hooks/`, which does not travel with a clone.

```bash
git config core.hooksPath tools/enforce-agent-gates
```

This is per repository and per clone. It is the step agents skip most reliably, so a person should do it alongside `git init`.

## 6. Verify, then say done

```bash
python tools/check-last/check_last.py --root /path/to/your-project --all
```

Exit 0, with the count from step 4 recorded. Before that, the honest status is `verified, pending commit` — not `complete`.
