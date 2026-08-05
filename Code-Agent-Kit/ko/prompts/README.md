# 작업 진입 Prompt Router

워크플로우 문서를 반복 가능한 작업 진입 절차로 바꾼 Prompt입니다.

| 상황 | Prompt |
|---|---|
| 모든 작업 시작 | `0-sync-and-orient.md` |
| 기존 프로젝트 분석 | `1-analyze-existing-project.md` |
| 신규 프로젝트 시작 | `2-bootstrap-new-project.md` |
| 신규 기능 추가 | `3-new-feature.md` |
| 기존 기능 수정 | `4-modify-feature.md` |
| 격리된 Demo 작성 | `5-demo-sample.md` |
| 잘못 구현된 기능 Debug | `6-debug-fix.md` |
| 이미 킷을 쓰는 Project에서 킷 갱신 | `7-update-the-kit.md` |
| 기술 스택을 채우거나 추가 | `8-fill-stack.md` |

모든 Prompt는 `GATE.md`를 사용합니다.

이어서 하는 작업은 Worklog Header와 Resume Point로 Feature만 확인한 뒤 Git, Project Map, Feature Current를 읽고 전체 Worklog를 Load하여 재개합니다.
