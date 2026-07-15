# ADR-004: Stack이 소유하는 Feature Boundary

- 상태: accepted

## 결정

Core는 모든 Stack이 Feature Boundary와 Action Model을 정의하도록 요구합니다. Core가 Screen, Service, Endpoint, File 중 하나를 보편적인 Feature 단위로 강제하지 않습니다.

## 버린 대안

특정 UI Framework의 Screen Model을 모든 Stack에 적용.

## 이유

Enterprise Screen Framework, React Application, API, Library, Batch System은 Ownership와 Deployment Boundary가 다릅니다.
