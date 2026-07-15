# check-build-log

Generic deterministic scanner for build or generator logs.

```bash
python tools/check-build-log/check_build_log.py build.log \
  --config stacks/<stack>/validation/build-log-patterns.json
```

A stack supplies error patterns, ignored patterns, and required success markers.
