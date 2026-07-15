# 0 — 동기화와 방향 잡기

## 미완료 작업

1. Active Worklog의 Header와 Resume Point만 읽어 Feature를 확인합니다.
2. Git Root, Branch, Status, 사용할 수 있는 Base를 확인합니다.
3. 가능한 경우 `origin/main`을 Fetch하고 비교합니다.
4. Project Map을 읽습니다.
5. 대상 Feature Current를 읽습니다.
6. Current의 Related Files와 Shared Dependencies를 읽습니다.
7. 전체 Worklog를 읽습니다.
8. Incoming Change 충돌을 해결한 뒤 기록된 Gate 단계부터 재개합니다.

## 완료된 기존 Feature의 새 작업

1. Git Root, Branch, Status, 사용할 수 있는 Base 확인
2. 가능한 경우 `origin/main` Fetch 및 비교
3. Project Map 읽기
4. 대상 Feature Current 읽기
5. Current의 Related Files와 Shared Dependencies 읽기
6. 새 Worklog 생성
7. 상황별 Prompt와 `GATE.md` 진행

Remote가 없으면 Local `main` 또는 `master`를 사용하고 Remote 동기화가 불가능했다고 기록합니다.
