# Getting Started

## 1. Read the design and state model

Start with:

- `DESIGN-CONCEPTS.md`
- `AGENTS.md`
- `docs/core/state-and-memory-model.md`
- `docs/getting-started/stack-input-requirements.md`

## 2. Inspect Git and the project route

```bash
git status
```

For the sample, read:

```text
samples/react-aspnetcore-taskflow/docs/project-map.md
samples/react-aspnetcore-taskflow/docs/features/task-flow.current.md
```

Project-level `docs/current.md` is a summary. Feature modification begins from feature current.

## 3. Confirm stack readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

For another project, copy the stack template and supply the owner inputs before implementation.

## 4. Confirm MCP

For Codex:

```bash
codex mcp list
```

Expected:

- `microsoft_learn`
- `context7`

MCP is a knowledge source. Retrieved facts must be compacted into evidence provenance.

## 5. Start the task

New feature or modification:

1. run `prompts/0-sync-and-orient.md`;
2. use the matching prompt under `prompts/`;
3. create a worklog from `templates/core/worklog.md`;
4. use all five mandatory Gate headings;
5. resolve blocking capabilities before code.

Unfinished task:

```text
worklog header
→ Git
→ Project Map
→ feature current
→ current Related Files
→ full worklog
→ resume
```

## 6. Run the TaskFlow sample

Backend:

```bash
cd samples/react-aspnetcore-taskflow/backend/TaskFlow.Api
dotnet run
```

Frontend:

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm install
npm run dev
```

Open `http://localhost:5173`.

## 7. Suggested first experiment

Add a task-priority field.

The agent should:

1. read Task Flow current and shared dependencies;
2. confirm React/.NET stack readiness;
3. create a new worklog;
4. verify version-sensitive facts;
5. update frontend and backend contracts together;
6. run artifact, rendered-output, runtime, and color gates;
7. update feature current with the verified commit;
8. append feature history;
9. update Project Map and reverse index;
10. review the final Diff.

## 8. Run validation

Full repository gate:

```powershell
./scripts/pre-commit-validate.ps1
```

Sample-only gate:

```powershell
./samples/react-aspnetcore-taskflow/scripts/validate.ps1
```

Bash equivalents are also provided.
