# Git Workflow and State Documents

Recommended production workflow:

```text
sync protected main
→ feature branch
→ worklog and Gate
→ validation
→ current/history/Project Map synchronization
→ commit
→ pull request
→ protected main merge
```

## State linkage

Feature current:

```yaml
code-verified: "2026-07-14 @abc1234"
last-pr: "#42"
```

Feature history records baseline, branch, commit, PR, evidence, and regression.

## Protection principles

- no direct release work on protected main;
- no merge while required validation is FAIL or unreported;
- PENDING requires an explicit policy decision, not silent acceptance;
- shared-file changes list affected features and regression checks;
- post-merge commit identifiers may be added through a state synchronization commit when necessary.

Projects without PR infrastructure record the reason and use the strongest available review mechanism.
