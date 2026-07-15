# Backend Validation

Required:

```bash
dotnet restore
dotnet build --no-restore
dotnet test --no-build
```

Evidence:

- target framework and SDK;
- build exit code;
- test summary;
- API contract changes;
- final backend diff.
