# Stack 전용 Agent Rule — Rust

이 File은 Root `AGENTS.md`를 확장합니다. 같은 내용을 반복하지 않습니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- Blocking Capability의 상태가 `unknown`이면 그에 의존하는 Pattern은 금지입니다.
  "조심해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`를 통해 라우팅합니다. 이 Stack에서 권위 있는 Source는
  `context7`이고 `microsoft-learn`은 아닙니다. 이유는 그 문서에 적혀 있습니다.
- 기억 대신 `references/verified-facts.md`와 `references/pitfalls.md`를 사용합니다.
  그 안의 모든 항목은 어디서 확인했는지를 밝히고 있습니다.
- 선택한 Capability는 모두 Project Map에 기록하고 Gate Analysis에서 다시 언급합니다.

## Stack 금지 사항

- Version에 민감한 Fact를 기억으로 진술하지 않습니다. 서로 다른 Async Runtime의 문서를 섞지 않습니다. 그 Type들은 서로 바꿔 쓸 수 없습니다. 2018 edition 이전 Source로 답하지 않습니다.
- 명령과 Exit Code 없이 Validation이 통과했다고 보고하지 않습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답변되지 않은 입력은
  Blocked Stack이며, 그것은 올바른 상태입니다.
