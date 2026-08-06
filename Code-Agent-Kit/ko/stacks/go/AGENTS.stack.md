# Stack 전용 Agent Rule — Go

이 File은 Root `AGENTS.md`를 확장합니다. 같은 내용을 반복하지 않습니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- Blocking Capability의 상태가 `unknown`이면 그에 의존하는 Pattern은 금지됩니다.
  "조심해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`를 거칩니다. 이 Stack에서 권위 있는 Source는
  `context7`이고 `microsoft-learn`은 아닙니다. 이유는 그 File에 적혀 있습니다.
- 기억에 의존하지 말고 `references/verified-facts.md`와 `references/pitfalls.md`를
  사용합니다. 그곳의 모든 항목에는 어디서 확인했는지가 함께 적혀 있습니다.
- 선택한 Capability는 빠짐없이 Project Map에 기록하고 Gate Analysis에서 다시
  언급합니다.

## Stack 금지 사항

- Version에 민감한 사실을 기억에서 꺼내 말하지 않습니다. 다른 언어의 동시성 문서나 Error 문서를 근거로 Go 질문에 답하지 않습니다. Framework를 가정하지 않습니다. 이 Stack은 표준 Library가 전부인 경우가 많습니다.
- 명령과 그 exit code 없이 Validation이 통과했다고 보고하지 않습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답이 없는 입력은
  Blocked Stack이고, 그것은 올바른 상태입니다.
