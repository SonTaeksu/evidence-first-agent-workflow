# check-state-model

Validates:

- Project Map feature routing, architecture, capabilities, and shared reverse index;
- feature-current front matter and required sections;
- matching append-only feature history;
- system and database architecture state;
- worklog current pointer and five mandatory Gate headings.

```bash
python tools/check-state-model/check_state_model.py \
  --project-docs samples/react-aspnetcore-taskflow/docs
```
