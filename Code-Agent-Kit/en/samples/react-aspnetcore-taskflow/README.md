# TaskFlow — React + ASP.NET Core Sample

TaskFlow is a deliberately small feature workflow application used to demonstrate:

- Document First design;
- mandatory Git baseline and Diff review;
- official-source MCP routing;
- deterministic backend and frontend validation;
- validation-based `current.md` handoff;
- feature evolution in `history.md`;
- stack-independent workflow plus stack-specific rules.

## Features

- list work items;
- create a task;
- move a task through a controlled status workflow;
- submit for approval;
- approve or reject;
- responsive UI;
- backend API tests;
- frontend component test;
- Playwright E2E and narrow-viewport check.

## Requirements

- .NET SDK 10.x
- Node.js 22.12 or later
- npm
- Playwright Chromium for E2E

## Run locally

Backend:

```bash
cd backend/TaskFlow.Api
dotnet run
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Open:

```text
http://127.0.0.1:5173
```

## Validate

PowerShell:

```powershell
./scripts/validate.ps1
```

Bash:

```bash
./scripts/validate.sh
```

The script writes evidence under:

```text
docs/evidence/generated/
```

## Docker

```bash
docker compose up --build
```

- UI: `http://localhost:5173`
- API health: `http://localhost:8080/health`

## Workflow documents

- [AGENTS.md](AGENTS.md)
- [current.md](docs/current.md)
- [history.md](docs/history.md)
- [Project Map](docs/project-map.md)
- [Initial design](docs/designs/001-initial-taskflow.md)
- [Priority-field experiment](docs/designs/002-priority-field.example.md)

## Suggested experiment

Use a fresh agent chat and request:

> Add `priority` with Low, Normal, and High values. Display it on each card and allow selecting it when creating a task. Follow AGENTS.md and do not finish until deterministic validation passes.

Compare the result with the prepared design example.
