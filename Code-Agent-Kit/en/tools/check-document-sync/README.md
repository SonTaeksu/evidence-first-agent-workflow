# check-document-sync

Checks:

- code changed without any state-document update;
- required state files are missing;
- Project Map references a missing repository path.

Example:

```bash
python tools/check-document-sync/check_document_sync.py \
  --base main \
  --scope samples/react-aspnetcore-taskflow \
  --current docs/current.md \
  --history docs/history.md \
  --project-map docs/project-map.md
```
