# Stack 전용 Agent Rule — Vue.js

Root `AGENTS.md`를 확장하며, 같은 내용을 반복하지 않습니다.

- Stack 의존 구현 전에 `STACK-READINESS.json`을 읽습니다.
- 상태가 `unknown`인 Blocking Capability는 해당 Pattern을 금지합니다.
  "주의해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`로 라우팅합니다. 이 Stack의 Authoritative Source는
  `context7`이고 `microsoft-learn`은 아닙니다. 이유는 그 File에 있습니다.
- 기억 대신 `references/verified-facts.md`와 `references/pitfalls.md`를 씁니다. 그곳의 모든
  항목은 검증 위치를 밝힙니다.
- 선택한 Capability는 Project Map에 기록하고 Gate Analysis에서 반복합니다.

## Stack 금지 사항

- Version 민감 Fact를 기억으로 말하지 않습니다. Vue 질문에 Microsoft Learn으로 답하지 않습니다. Vue 2의 답을 Vue 3 Project로, 또는 그 반대로 옮기지 않습니다 — Reactivity System이 다릅니다.
- 명령과 Exit Code 없이 Validation 통과를 보고하지 않습니다.
- Owner 대신 `STACK-INPUTS.md` 행을 채우지 않습니다. 답하지 않은 입력은 Blocked Stack이며,
  그것은 올바른 상태입니다.
