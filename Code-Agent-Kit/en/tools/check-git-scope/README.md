# check-git-scope

Compares the final change set with the design and worklog scope.

Improvements adopted from the Code Agent Kit:

- `origin/main` → `main` → `master` base fallback;
- uncommitted and committed change detection;
- direct expected-file input;
- acknowledged unexpected files with reason;
- artifact-existence fallback when Git is unavailable;
- optional strict failure for expected but unchanged files.

Design-based use:

```bash
python tools/check-git-scope/check_git_scope.py \
  --design docs/designs/feature.md \
  --scope samples/application
```

Worklog list:

```bash
python tools/check-git-scope/check_git_scope.py \
  --expected-file expected-files.txt \
  --ack-file acknowledged-files.txt
```

An acknowledged file is not silently ignored. Its reason and impact must be recorded in the design or worklog.
