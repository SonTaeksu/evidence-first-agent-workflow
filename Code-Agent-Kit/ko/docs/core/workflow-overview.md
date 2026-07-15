# Core Workflow 개요

## 권한 및 State 우선순위

```text
Code 및 생성 Artifact
→ 결정론적 Validation
→ Feature Current
→ Project Map
→ Append-only History
→ 실행 Checkpoint인 Active Worklog
```

Worklog가 Current보다 우선하지 않습니다. Worklog는 미완료 실행을 기록하고 Feature Current는 검증된 현재 상태를 기록합니다.

## 완료된 기존 Feature의 새 작업

```text
요청
→ Git 기준점과 Diff
→ Project Map
→ Feature Current
→ Related Files 및 Shared Dependencies
→ Stack Readiness와 Capability
→ 새 Worklog
→ 5단계 Gate
→ 구현 및 Validation
→ Current/History/Project Map 동기화
→ 최종 Diff
→ DoD
```

## 미완료 작업 재개

```text
Worklog Header 및 Resume Point
→ Git 기준점과 Diff
→ Project Map
→ Feature Current
→ Related Files
→ 전체 Worklog
→ 기록된 Gate 단계
```

## Knowledge Routing

```text
Project Map
→ Stack SKILL
→ Task 전용 검증 Reference
→ Source 검사
→ 여전히 필요할 때만 Search
```

일반 Tutorial을 Project Evidence 대신 Load하지 않습니다.

## Validation

적용되는 Layer를 별도 기록합니다.

- Artifact / Compile
- Rendered Output
- Runtime Behavior
- Accessibility / Color

모델 자기신고는 Evidence가 아닙니다.

## 완료

Production 완료에는 다음이 필요합니다.

- 필수 결정론적 Gate PASS
- Feature Current에 검증 Commit 기록
- Feature History Append
- Project Map 및 Shared File Reverse Index 갱신
- Active Worklog 종료 또는 Archive
- 최종 Git Diff 검토
- 미해결 항목 PENDING 유지

기능 하나 또는 일관된 Task Group이 DoD를 통과하면 다음 Feature는 새 채팅에서 시작합니다.
