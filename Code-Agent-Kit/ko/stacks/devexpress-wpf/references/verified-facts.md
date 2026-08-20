# 검증된 Fact — DevExpress WPF (v24.2+)

비어 있고, 그것이 맞습니다. 이 Stack은 이 Repository에서 아직 실제 Project에
쓰인 적이 없어서, 읽어 온 것이 아니라 확인한 것이라고 할 만한 내용이 없습니다.

| Fact | 확인 대상 | 날짜 |
|---|---|---|

## Rule

- 행에는 Source가 있어야 합니다. Source가 없으면 그것은 기억이고, 기억은 누구의
  Reference File에도 들어가지 않습니다.
- Version에 민감한 Fact는 어떤 Version에 대해 확인했는지를 밝힙니다. 이 Stack에서 그것은
  DevExpress Version을 뜻하며, 그것이 이 Fact들이 움직이는 축입니다. .NET Target만으로는
  동작을 특정할 수 없습니다.
- `references/pitfalls.md`는 기술 자체의 속성을 담고, 이 File은 *이 Project*에 관한
  Fact를 담습니다. 둘은 같지 않으며 합치지 않습니다.
- DevExpress 문서 Server 자체에 관한 Fact는 여기가 아니라 `../mcp/source-routing.md`에
  들어가며, 그 File은 측정이 무엇을 다뤘고 무엇을 열어 둔 채로 남겼는지를 정확히
  기록합니다. 요약하면 **2026-08-06**에 `https://api.devexpress.com/mcp/docs`를 대상으로
  한 MCP Inspector
  `tools/list`가 Credential 없이 성공했고 Tool 두 개를 그 전체 입력 Schema와 함께
  돌려주었으며, 그 Schema는 거기에 옮겨 적혀 있습니다. 등급은 **Tool 목록은 냈으나
  호출은 하지 않음**입니다. 실제 `tools/call`은 실행되지 않았으므로,
  `../../../docs/core/mcp-source-verification.md`의 열네 Server가 하나에 답해서 얻은
  `PASS`를 이것은 **가지지 않습니다**. 그리고 `?v=24.2`는 따로 시험되지 않았습니다.
