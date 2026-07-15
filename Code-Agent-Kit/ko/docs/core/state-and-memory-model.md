# State 및 Memory Model

## 문서 역할

| 문서 | 수명 | 목적 |
|---|---|---|
| Project Map | Project | Feature, Architecture State, Capability, Shared Dependency Routing |
| Feature Current | 지속·갱신 | 이후 모든 수정 작업의 시작점인 검증된 상태 |
| Feature History | 지속·Append-only | Commit과 PR의 사람이 읽는 Index |
| Feature Worklog | 작업 진행 중 임시 | Gate 진행, Todo, Evidence, Resume Point |
| Architecture Current/History | Project | 여러 Feature에 영향을 주는 System 및 Database 결정 |

## 필수 시작 순서

Active Worklog가 미완료 Task를 식별하지만 구현 전에 Current State를 반드시 다시 읽습니다.

```text
Worklog Header
→ Git
→ Project Map
→ Feature Current
→ Current Related Files
→ 전체 Worklog
→ 재개
```

완료된 Feature의 새 작업:

```text
Git
→ Project Map
→ Feature Current
→ Related Files
→ 새 Worklog
→ Analysis
```

## Current State

Current에는 검증된 현재 상태만 기록합니다.

- Code-verified Commit
- 가능한 경우 Last PR
- Behavior와 Contract
- 역할별 File
- Shared Dependency
- Capability 결정
- 3단 Validation 상태
- Known Issue
- Next Candidate Work

## History

History는 Append-only입니다.

- 이전 Entry를 삭제하거나 조용히 수정하지 않습니다.
- Correction은 잘못된 Entry를 참조하는 새 Entry로 추가합니다.
- Commit, PR, Evidence, Validation, Impact, Shared File Regression을 기록합니다.

## Worklog Lifecycle

```text
생성
→ Gate 진행 중 갱신
→ 완료
→ 검증 결과를 Current/History/Project Map에 반영
→ Archive 또는 종료
```

Archive Worklog는 실행 Evidence이며 이후 기능 수정의 시작 State가 아닙니다.
