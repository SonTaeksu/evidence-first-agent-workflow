# Portable Code Agent Kit — English

> **New here? Read [QUICKSTART.md](QUICKSTART.md) first — one page, a result in 3 steps.**

This directory is a complete, self-contained English mirror. Copy **this directory's contents** into a target repository, or run the installer.

## Fastest use

```bash
python install-kit.py --target /path/to/project --mode full
```

PowerShell:

```powershell
.\install-kit.ps1 -Target C:\path	o\project -Mode full
```

Core-only with one stack profile:

```bash
python install-kit.py --target /path/to/project --mode core --stack react-aspnetcore
```

## Included

- root agent rules and adapters;
- prompts and mandatory Gate;
- agent-facing core docs and architecture decisions;
- human onboarding docs excluded from normal indexing by `.agentignore`;
- state, worklog, project-map, and stack templates;
- stack profiles and readiness checks;
- deterministic tools and scripts;
- demos and demo template;
- reference-asset directories for images, SPA HTML, and generated evidence;
- optional sample application and inactive CI template;
- license texts and manifest.

## Start

1. Read `AGENTS.md`.
2. Read `docs/getting-started/README.md`.
3. Fill or verify the selected stack's `STACK-INPUTS.md`.
4. Run stack readiness.
5. Start through `prompts/0-sync-an