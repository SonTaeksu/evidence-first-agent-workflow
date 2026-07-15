# 개발자 Guide

## Mental Model

Agent가 개발 책임을 대신하지 않습니다.

Agent 역할:

- 상황별 작업 Prompt 따르기
- 작은 Routing 문서를 먼저 읽기
- Evidence 수집
- 제한된 범위 구현
- 결정론적 Gate 실행
- 다음 Session을 위한 State 갱신

개발자 역할:

- 방향 선택
- 미확인 요구사항 결정
- 보안과 Product 동작 Review
- Reference Asset과 Visual Baseline 승인
- 최종 Diff와 Evidence 검토

## 표준 경로

```text
동기화와 방향 잡기
→ Analysis
→ Task
→ Todo와 Micro-Verify
→ Checklist
→ Verification
→ State 갱신
→ Review와 Commit
```

## 상황별 Router

| 상황 | 시작 문서 |
|---|---|
| 신규 기능 | `prompts/3-new-feature.md` |
| 기능 수정 | `prompts/4-modify-feature.md` |
| 실패 Debug | `prompts/6-debug-fix.md` |
| 격리 실험 | `prompts/5-demo-sample.md` |
| 새 채팅에서 이어서 작업 | Active Worklog의 Resume Point |

모든 상황은 `prompts/0-sync-and-orient.md`로 시작합니다.

## 원본 기반 UI 작업

```text
Image
→ Reference Image Manifest
→ 이름 있는 영역과 Color Evidence

SPA HTML
→ Rendered DOM
→ Screen Specification
→ Block과 Data Checklist

Implementation
→ 구현 화면 Specification
→ 완전성 비교
→ Accessibility 및 Color Gate
```

Build가 성공했어도 UI Block이 비거나 빠졌으면 완료가 아닙니다.

## 읽기 순서

1. Root README
2. Getting Started
3. Core Workflow
4. Prompt Router
5. Stack Profile
6. Sample
7. Pre-commit Validation

이 Guide는 사용하는 방법을 설명합니다. 규범 문서를 덮어쓰지 않습니다.
