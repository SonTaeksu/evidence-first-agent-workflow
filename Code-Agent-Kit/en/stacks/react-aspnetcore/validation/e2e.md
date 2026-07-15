# End-to-End Validation

Start backend and frontend before running:

```bash
npm run e2e
```

Minimum checks:

- task list loads;
- a task can be created;
- status can move to In Progress;
- task can be submitted for approval;
- approval changes status to Approved;
- error messages are visible;
- narrow viewport does not introduce unintended page scrolling.
