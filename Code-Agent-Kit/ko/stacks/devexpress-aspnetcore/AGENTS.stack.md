# Stack별 Agent Rule — DevExpress for ASP.NET Core

이 파일은 Root `AGENTS.md`를 확장합니다. 그 내용을 되풀이하지 않습니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- 상태가 `unknown`인 Blocking Capability는 그에 의존하는 패턴을 금지합니다.
  "조심해서 진행"이 아니라 금지입니다. 여기서 가장 중요한 것은
  `ui-component-layer`입니다. 해결되기 전까지 Component를 추가한다는 것은 서로 다른
  두 제품 사이에서 추측한다는 뜻입니다.
- 문서 조회는 `mcp/source-routing.md`를 통해 라우팅합니다. DevExpress에 대해서는
  `dxdocs`가 권위 있고, ASP.NET Core와 EF Core와 .NET에 대해서는 `microsoft-learn`이
  권위 있으며 DevExpress에 대해서는 어떤 것도 권위가 없습니다.
- 기억 대신 `references/verified-facts.md`와 `references/pitfalls.md`를 사용합니다.
  그곳의 모든 항목은 어디서 확인되었는지를 밝힙니다.
- 선택한 모든 Capability를 Project Map에 기록하고 Gate Analysis에서 다시 언급합니다.

## Stack 금지 사항

- **DevExpress API 질문에 `microsoft-learn`으로 답하지 않고, 기억으로도 답하지
  않습니다.** Component 이름, Property 이름, tag helper 이름, Service 등록 호출은 모두
  Version에 민감하고, 지어내면 모두 그럴듯해 보입니다. `dxdocs`를 통해 조회합니다.
- Server-side Control에 대한 답을 DevExtreme의 Client-side Widget을 쓰는 Project에
  섞지 않고, 그 반대도 하지 않습니다. 서로 다른 제품이며, 옮겨 온 답은 자신 있게
  틀립니다.
- WinForms나 WPF Reporting 답을 이 Web Host로 가져오지 않고, 그 반대도 하지 않습니다.
- Package가 참조되어 있다는 이유로 Report Designer나 Document Viewer가 동작한다고
  가정하지 않습니다. 등록과 Client Asset은 별개의 사실이고, 각각 따로 확인합니다.
- 캐시된 Restore를 근거로 Build가 통과했다고 보고하지 않습니다. Private Feed는 실제로
  거기까지 도달하는 Restore로만 검증됩니다.
- 이 Project에서 읽지 않은 Version 번호, Package 식별자, 라이선스 키를 여기 있는 어떤
  문서에도 쓰지 않습니다.
- 명령과 그 Exit Code 없이 Validation이 통과했다고 보고하지 않습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답변되지 않은 입력은 Stack이
  차단된 상태이며, 그것이 올바른 상태입니다.
