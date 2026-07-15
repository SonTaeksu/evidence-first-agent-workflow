# Feature Worklog 및 Handoff — 작업 이름

```yaml
feature: feature-key
current: docs/features/feature-key.current.md
status: in-progress
started: YYYY-MM-DD
updated: YYYY-MM-DDTHH:MM:SSZ
branch: feature/example
baseline: main-commit
last_commit: none
gate_stage: 1-analysis
```

> 임시 Checkpoint입니다. 새 Session은 Header로 Feature를 확인한 뒤 Git, Project Map, Feature Current를 읽고 전체 Worklog를 읽습니다.

## Resume Point

- 다음 작업:
- 현재 Gate 단계:
- Current 이후 열 File:
- 이미 추출한 Evidence:
- 다시 읽지 않아도 되는 Source Asset:
- Blocking `⟨확인 필요⟩` 항목:

## 1. Analysis

- 요청:
- 대상 Feature:
- Project Map Route:
- Feature Current 요약:
- Git 기준점과 Incoming Change:
- 영향 File:
- Shared File 영향:
- 가정:
- 미확인:

### Environment Capability Decision

| Capability | 상태 | Evidence | 선택 경로 |
|---|---|---|---|
| | present / absent / unknown | | |

### Source Evidence 및 Provenance

- 원본 Asset Hash:
- 공식 또는 1차 Source:
- Reference Image Manifest:
- SPA Screen Specification:
- Block, Grid, Column, Row:
- Color Region:
- Contract Mapping:

## 2. Task

- 목표:
- Acceptance Criteria:
- 제외 범위:
- Validation 명령:

### Expected Files

- [ ]

### 인정된 예상 밖 File

- [ ] path — 이유, 영향, 필요한 Regression

## 3. Todo와 Micro-Verify

**진행률:** 0 / 0

- [ ] Todo 1
  - 변경:
  - Micro-Verify 명령:
  - 결과:
  - 실패 처리: Todo 반복 / Analysis 복귀
- [ ] Todo 2
  - 변경:
  - Micro-Verify 명령:
  - 결과:
  - 실패 처리: Todo 반복 / Analysis 복귀

## 4. Checklist

- [ ] Architecture와 Naming
- [ ] Contract 동기화
- [ ] Source 충실도
- [ ] Artifact, Rendered Output, Runtime을 별도로 검증
- [ ] Color 및 Accessibility Evidence
- [ ] Error, Loading, Empty, Placeholder State
- [ ] Security 및 Trust Boundary
- [ ] Shared File Reverse 영향
- [ ] 무관한 변경 없음
- [ ] 사람용 Guide를 Agent Rule로 취급하지 않음

## 5. Verification

| Layer 또는 Gate | 명령 | Exit | 결과 | Evidence |
|---|---|---:|---|---|
| Artifact / Compile | | | | |
| Unit / Integration | | | | |
| Rendered Output | | | | |
| Runtime Behavior / E2E | | | | |
| Screen Spec 완전성 | | | | |
| Color / Accessibility | | | | |
| Git Scope | | | | |
| Document Sync | | | | |

## Correction, Decision, Pending

- Correction:
- Decision:
- PENDING:

## 완료

- [ ] 필수 Validation PASS
- [ ] Feature Current에 Code-verified Commit 기록
- [ ] Append-only Feature History Entry 추가
- [ ] Project Map과 Shared File Reverse Index 갱신
- [ ] Active Worklog 종료 또는 Archive
- [ ] 최종 Git Diff 검토
- [ ] 다음 Feature는 새 채팅에서 시작
