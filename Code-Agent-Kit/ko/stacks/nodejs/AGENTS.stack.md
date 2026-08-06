# Stack별 Agent Rule — Node.js

이 File은 Root `AGENTS.md`를 확장합니다. 같은 내용을 다시 적지 않습니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- 상태가 `unknown`인 Blocking Capability는 그에 의존하는 Pattern을 금지합니다.
  "조심해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`를 거칩니다. 이 Stack의 정본은 `context7`이고
  `microsoft-learn`은 아닙니다. 이유는 그 File에 적혀 있습니다.
- 기억에 의존하지 말고 `references/verified-facts.md`와 `references/pitfalls.md`를
  사용합니다. 그곳의 모든 항목은 어디서 검증했는지를 밝힙니다.
- 선택한 Capability는 전부 Project Map에 기록하고 Gate Analysis에서 다시 언급합니다.

## Stack 금지 사항

- Version 민감 Fact를 기억으로 말하지 않습니다. Browser JavaScript 문서로 Node 질문에 답하지 않습니다. Framework를 가정하지 않습니다. Node Project에 Framework가 없을 수도 있습니다.
- 명령과 그 Exit Code 없이 Validation이 통과했다고 보고하지 않습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답하지 않은 입력은
  Blocked Stack이고, 그것이 올바른 상태입니다.
