# Verified Facts — DevExpress for ASP.NET Core

비어 있고, 그것이 맞습니다. 이 Stack은 이 Repository의 실제 Project에 아직 사용된 적이
없으므로, 읽은 것이 아니라 확인된 것은 아무것도 없습니다.

| 사실 | 확인 대상 | 날짜 |
|---|---|---|

## 위 표에 속하지 않는, 측정된 사실 하나

`dxdocs` Endpoint 자체는 **2026-08-06**에 측정되었습니다. MCP Inspector, CLI, Streamable
HTTP 위의 `tools/list`, 자격 증명 없음. 연결되었고 문서화된 두 Tool을 그 Input Schema와
함께 돌려주었으며, 그 내용은 `mcp/source-routing.md`에 기록되어 있습니다. 등급은
**`tools/list` 측정됨, `tools/call` 없음**이며, 실제 호출에 답한
`docs/core/mcp-source-verification.md`의 Server들이 지닌 `PASS`보다 약합니다. 고정된
`?v=24.2` Endpoint는 검증되지 않았습니다.

이것을 표에 넣지 않고 여기에 적어 둔 이유는, 이 Project에 관한 사실이 아니라 공유 Source에
관한 사실이고 이 표는 이 Project에 관한 사실을 위한 것이기 때문입니다.

## 규칙

- 행에는 Source가 필요합니다. 없으면 기억이고, 기억은 누구의 Reference 파일에도 들어가지
  않습니다.
- Version에 민감한 사실은 어떤 Version에 대해 확인되었는지를 밝힙니다. 이 Stack에서는
  .NET Version뿐 아니라 DevExpress Version을 뜻합니다 — 둘은 따로 움직입니다.
- DevExpress 사실은 출처인 도움말 항목 URL을 밝혀서, 나중에 읽는 사람이 다시 검색해 다른
  곳에 도착하는 대신 동일한 페이지를 가져올 수 있게 합니다.
- `references/pitfalls.md`는 기술의 성질을 담고, 이 파일은 *이 Project*에 관한 사실을
  담습니다. 둘은 같지 않으며 합치지 않습니다.
