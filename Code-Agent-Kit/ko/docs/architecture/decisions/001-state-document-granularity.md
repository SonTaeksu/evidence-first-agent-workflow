# ADR-001: State 문서 Granularity

- 상태: accepted

## 결정

Feature마다 Current 1개, Append-only History 1개, Active Worklog 최대 1개를 사용합니다. Create, Update, Delete, Import, Export 같은 Action은 Stack이 별도 배포 Boundary로 정의하지 않는 한 같은 Feature State 안에 둡니다.

## 버린 대안

CRUD 동사별 Current File.

## 이유

동사별 File은 동기화 비용, 모호한 완료, 중복 상태를 만듭니다. Feature Current는 다음 Agent에게 검증된 시작 지도 하나를 제공합니다.
