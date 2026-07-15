# ADR-002: Reference 선택 Load

- 상태: accepted

## 결정

Project Map과 Stack SKILL Routing을 통해 Reference를 Load합니다. Knowledge Pack 전체를 상시 Load하지 않습니다.

## 버린 대안

모든 Framework 문서를 항상 Load.

## 이유

큰 Context는 비용과 Lost-in-the-middle 위험을 높입니다. Knowledge Pack은 추론하기 어려운 Fact에 집중하고 작업 관련 Reference만 Routing해야 합니다.
