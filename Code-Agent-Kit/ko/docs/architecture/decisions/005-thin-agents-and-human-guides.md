# ADR-005: 얇은 AGENTS와 사람용 Guide 분리

- 상태: accepted

## 결정

Root `AGENTS.md`는 짧고 규범적으로 유지합니다. 상세 절차는 Routing 문서에 둡니다. 긴 Onboarding Guide는 `docs/human/`에 두고 일반 Agent Indexing에서 제외합니다.

## 버린 대안

모든 Agent Adapter에 운영 세부 내용을 복제하고, 개발자 Tutorial을 일상적인 Agent Context에 Load.

## 이유

복제 Rule은 서로 달라집니다. 긴 Guide는 Context를 사용하고 실제 정본과 충돌할 수 있습니다.
