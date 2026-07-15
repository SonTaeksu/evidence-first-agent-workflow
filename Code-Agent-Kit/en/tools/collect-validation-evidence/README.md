# collect-validation-evidence

Runs a command, captures combined output, writes Markdown and JSON evidence, and returns the original command exit code.

Example:

```bash
python tools/collect-validation-evidence/collect.py \
  --name frontend-build \
  --cwd samples/react-aspnetcore-taskflow/frontend \
  --output samples/react-aspnetcore-taskflow/docs/evidence/generated/frontend-build.md \
  -- npm run build
```
