# Stack 전용 Agent Rule — DevExpress WPF (v24.2+)

이 File은 Root `AGENTS.md`를 확장하며 같은 내용을 반복하지 않습니다. 또한
`../csharp-wpf/AGENTS.stack.md`도 확장하며 그쪽은 계속 유효합니다. 이 Stack은 WPF Rule을
대체하는 것이 아니라 그 위에 DevExpress Rule을 더합니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- Blocking Capability의 상태가 `unknown`이면 그에 의존하는 Pattern은 금지입니다.
  "조심해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`를 통해 라우팅합니다. DevExpress에 대해서는
  `dxdocs`가 권위 있고, 평범한 WPF와 XAML과 .NET에 대해서는 `microsoft-learn`과
  `wpf-docs`가 권위 있습니다. 어느 쪽도 다른 쪽을 대신해 답하지 않습니다.
- 기억 대신 `references/verified-facts.md`와 `references/pitfalls.md`를 사용합니다.
  그 안의 모든 항목은 어디서 확인했는지를 밝히고 있습니다.
- 선택한 Capability는 모두 Project Map에 기록하고 Gate Analysis에서 다시 언급합니다.

## Stack 금지 사항

- DevExpress API 질문에 `microsoft-learn`이나 `wpf-docs`나 기억으로 답하지 않습니다.
  Microsoft는 이 Control들을 문서화하지 않으며, 조회가 아니라 기억으로 떠올린
  DevExpress 답은 Version의 모양을 하고 있습니다. 대개 Compile되고, 그래서 Review를
  통과해 살아남습니다.
- 어떤 `GridControl` View Type을 위해 쓰인 답을 다른 View Type에 적용하지 않습니다.
  View Type을 먼저 확정해야 합니다.
- 답을 DevExpress Version 사이로 옮기지 않습니다. v24.2 Project에서는 최신 Endpoint를
  조회하지 말고 문서 Server를 v24.2에 고정합니다.
- 이 Profile이 평범한 WPF까지 다룬다고 여기지 않습니다. Binding Trace, Dispatcher,
  Resource 조회, XAML Compile은 `../csharp-wpf`를 읽습니다.
- 명령과 Exit Code 없이 Validation이 통과했다고 보고하지 않으며, 개발자 Machine에서
  Theme이 적용된 UI가 올바르다고 보고하지 않습니다. 그 Machine에는 배포 여부와 무관하게
  Theme Assembly가 이미 있습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답변되지 않은 입력은
  Blocked Stack이며, 그것은 올바른 상태입니다.
