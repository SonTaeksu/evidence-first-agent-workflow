# 검증된 Fact — DevExpress WinForms

이 File은 명시된 Source에 대조해 명시된 날짜에 확인한 Fact를 담습니다. *이 Project*에 관한
내용은 아직 없습니다. 이 Stack이 이 Repository에서 실제 Project에 쓰인 적이 없기 때문이며,
그것은 누락이 아니라 올바른 상태입니다.

여기 있는 것은 문서 Source Layer입니다. Version에 민감하고, Stack 전체가 그것을 통해
라우팅되기 때문입니다.

| Fact | 범위 | 검증 대상 | 날짜 |
|---|---|---|---|
| DevExpress 문서 MCP Endpoint는 `https://api.devexpress.com/mcp/docs`이며 인증을 요구하지 않는다 | the endpoint | 공식 DevExpress 문서 | 2026-06-16 |
| Transport는 Streamable HTTP뿐이며, Browser GET은 `405 Method Not Allowed`를 반환하고, 문서는 그것이 결함이 아니라 예상된 응답이라고 밝힌다 | the endpoint | 공식 DevExpress 문서 | 2026-06-16 |
| Version 고정은 `?v=` Query Parameter를 쓰며 v24.2보다 이전 Release에서는 지원되지 않는다; `?v=24.2`가 문서에 있는 예시다 | v24.2 이상 | 공식 DevExpress 문서 | 2026-06-16 |
| Server가 노출하는 Tool은 정확히 두 개다: `devexpress_docs_search`(Semantic 검색, 상위 다섯 개 일치 반환)와 `devexpress_docs_get_content`(URL로 도움말 Topic 전체를 내려받음) | the endpoint | 공식 DevExpress 문서 | 2026-06-16 |
| 미리 정의된 Prompt가 존재한다: `mcp.dxdocs.devexpress_docs_query_workflow` | the endpoint | 공식 DevExpress 문서 | 2026-06-16 |
| 문서에 적힌 Server 이름은 최신 Release용 `dxdocs`와 고정용 `dxdocs24_2`이다 | the endpoint | 공식 DevExpress 문서 | 2026-06-16 |
| `https://learn.microsoft.com/api/mcp`는 자격 증명 없이 연결되며 Tool 3개를 노출한다 | the endpoint | MCP Inspector 실행, `docs/core/mcp-source-verification.md` | 2026-08-05 |
| `https://api.devexpress.com/mcp/docs`는 자격 증명 없이 연결되며 그 `tools/list`는 문서에 적힌 두 Tool을 정확히 반환한다 | the endpoint | MCP Inspector `tools/list`, `--transport http`, Owner의 Machine | 2026-08-06 |
| `devexpress_docs_search`는 `technologies`(array, `minItems: 1`, 닫힌 enum, **required**)와 `question`(string, **required**)을 받는다 | the endpoint | 같은 `tools/list` 출력 | 2026-08-06 |
| `technologies` enum은 닫혀 있으며 그 구성원은 `Angular`, `AspNet`, `AspNetBootstrap`, `AspNetCore`, `AspNetMvc`, `ASPxThemeBuilder`, `ASPxThemeDeployer`, `Blazor`, `CodedUIExtension`, `CoreLibraries`, `Dashboard`, `DesignSystem`, `DevExtremeAspNetMvc`, `eud`, `eXpressAppFramework`, `GeneralInformation`, `jQuery`, `MAUI`, `OfficeFileAPI`, `OfficeFileApiJava`, `React`, `ReportServer`, `SkinEditor`, `VCL`, `Vue`, `WindowsForms`, `WPF`, `WpfThemeDesigner`, `XPO`, `XpoProfiler`, `XtraReports`이다 — 이 Stack의 값은 `WindowsForms`이다 | the endpoint | 같은 `tools/list` 출력 | 2026-08-06 |
| `devexpress_docs_get_content`는 `url`(string, **required**)을 받으며, 그 자신의 설명이 일반 지식으로 URL을 조립하는 것을 금지한다 — URL은 `devexpress_docs_search` 결과에서 와야 한다 | the endpoint | 같은 `tools/list` 출력 | 2026-08-06 |
| Server 자신의 Tool 설명이 모든 `devexpress_docs_get_content`보다 `devexpress_docs_search`를 먼저 요구한다. 검색이 Snippet만 반환하기 때문이다 | the endpoint | 같은 `tools/list` 출력 | 2026-08-06 |

**2026-08-06 실행의 등급을 정확히 적으면 이렇습니다.** 연결되었고 Tool 목록을 받았습니다.
`tools/call`은 실행하지 **않았습니다**. `docs/core/mcp-source-verification.md`의 열네 개
Server가 `PASS`인 것은 각각이 실제 호출에 답했기 때문입니다. 이 Endpoint는 거기까지 가지
않았고 `PASS`로 기록되지 않았습니다. `https://api.devexpress.com/mcp/docs?v=24.2`는 아예
시험하지 않았습니다.

## 검증되지 않은 것으로 기록

| 주장 | 위 표에 없는 이유 |
|---|---|
| `api.devexpress.com/mcp/docs`가 실제 `tools/call`에 답한다는 것 | `⟨확인 필요: 위 Schema로 인자를 만들어 devexpress_docs_search에 대해 MCP Inspector tools/call을 실행할 것 — 2026-08-06 실행은 tools/list에서 멈췄다⟩` |
| 고정된 `api.devexpress.com/mcp/docs?v=24.2`가 무엇에든 답한다는 것 | `⟨확인 필요: 고정된 URL에 대해 MCP Inspector tools/list를 실행할 것 — 2026-08-06 실행은 고정되지 않은 URL만 썼고, 고정되지 않은 쪽이 답한다는 사실은 고정된 쪽의 Evidence가 아니다⟩` |

## 규칙

- 각 행에는 Source가 있어야 합니다. Source가 없으면 기억일 뿐이고, 기억은 누구의 Reference
  File에도 들어가지 않습니다.
- Version에 민감한 Fact는 어떤 Version에 대해 검증했는지 명시합니다.
- `references/pitfalls.md`는 기술의 속성을 담고, 이 File은 Source에 대조해 확인한 Fact를
  담습니다. 둘은 같지 않으며 합치지 않습니다.
- 문서는 실제로 응답한 호출보다 약한 등급의 Evidence입니다. 문서를 Source로 삼은 행은
  나중에 누군가 그 호출을 실행해도 여전히 문서를 Source로 남습니다 — 그 실행은 행을 하나
  추가할 뿐, 이 행을 승격시키지 않습니다.
