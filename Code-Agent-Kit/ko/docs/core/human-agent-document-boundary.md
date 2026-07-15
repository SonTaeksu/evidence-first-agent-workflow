# 사람용 문서와 Agent 문서의 경계

사람의 Onboarding 문서와 Agent 운영 규칙은 목적이 다릅니다.

## Agent가 읽는 문서

짧고 규범적인 문서로 유지합니다.

- `AGENTS.md`
- 가장 가까운 Stack 또는 Sample AGENTS
- Active Worklog
- Current State
- Project Map
- Design 및 Validation Profile
- 작업에 필요한 공식 문서

## 사람만 읽는 문서

예:

- 긴 개발자 Onboarding Guide
- 교육용 설명
- Screenshot과 Tutorial
- 조직적 배경 설명
- 사람을 위한 FAQ

`docs/human/` 아래에 두고 `.agentignore`로 제외합니다. 규범 문서로 Link할 수 있지만 운영 규칙을 조용히 다시 정의하면 안 됩니다.

## 이유

긴 개발자 Guide는 사람에게 유용하지만 모델 Context를 낭비하고 실제 운영 규칙과 중복·충돌할 수 있습니다. Agent는 짧은 정본을 따르고, 개발자 Guide는 사람이 그 정본을 사용하는 방법을 설명해야 합니다.
