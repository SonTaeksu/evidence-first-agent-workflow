# check-build-log

Build 또는 Generator Log를 검사하는 Generic 결정론적 Scanner입니다.

```bash
python tools/check-build-log/check_build_log.py build.log \
  --config stacks/<stack>/validation/build-log-patterns.json
```

Stack이 Error Pattern, Ignore Pattern, 필수 Success Marker를 제공합니다.
