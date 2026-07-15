# Git Workflow 및 State 문서

권장 Production Workflow:

```text
Protected Main 동기화
→ Feature Branch
→ Worklog 및 Gate
→ Validation
→ Current/History/Project Map 동기화
→ Commit
→ Pull Request
→ Protected Main Merge
```

## State 연결

Feature Current:

```yaml
code-verified: "2026-07-14 @abc1234"
last-pr: "#42"
```

Feature History에는 Baseline, Branch, Commit, PR, Evidence, Regression을 기록합니다.

## Protection 원칙

- Protected Main에서 Release 작업 직접 수행 금지
- 필수 Validation이 FAIL 또는 미보고 상태면 Merge 금지
- PENDING은 조용히 허용하지 않고 명시적 Policy 결정 필요
- Shared File 변경은 영향 Feature와 Regression 기록
- 필요한 경우 Merge 후 State 동기화 Commit으로 최종 Commit Identifier 기록

PR Infrastructure가 없는 Project는 이유를 기록하고 사용할 수 있는 가장 강한 Review 방식을 사용합니다.
