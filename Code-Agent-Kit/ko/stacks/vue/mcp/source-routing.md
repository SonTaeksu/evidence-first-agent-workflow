# Source Routing — Vue.js

아래 Server는 모두 **2026-08-05**에 MCP Inspector로 검증했습니다. 자격 증명 없이 연결되었고, Tool
목록을 반환했으며, 실제 `tools/call`에 응답했습니다. 판정과 실행 기록, 그리고 무엇보다 *검증하지
않은* 것이
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에 정리되어
있습니다.

| Server | Endpoint | Verdict | Tool | 역할 |
|---|---|---|---:|---|
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | **PASS** | 4 | 공식 문서 Repository |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | **PARTIAL** | 5 | Ecosystem 검색, 선택 사항 |

Transport는 전부 **Streamable HTTP**입니다. 취향이 아닙니다. 같은 Checker를 SSE로 돌린 이전 실행에서
모든 GitMCP Endpoint가 `405`를 반환했습니다. Streamable HTTP를 못 쓰는 Client에는 이 문서 끝의
`mcp-remote` Bridge가 필요합니다.

### `vue-docs` — PASS

Endpoint: `https://gitmcp.io/vuejs/docs`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰된 Tool:

- `fetch_docs_documentation`
- `search_docs_documentation`
- `search_docs_code`
- `fetch_generic_url_content`

용도: Vue 문서를 출처에서 그대로 읽기, 그리고 Vue 2와 Vue 3의 모든 답을 가르는 Version별 Page.

### `vue-docs-specialized` — PARTIAL

Endpoint: `https://mcp.vue-mcp.org/mcp`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰된 Tool:

- `vue_docs_search`
- `vue_api_lookup`
- `vue_get_related`
- `set_framework_preferences`
- `ecosystem_search`

용도: 검색 Tool이 동작할 때에 한해 더 넓은 Ecosystem(Router, Pinia, Vite, Vitest, Nuxt) 조회.

> **주의.** 연결과 tools/list는 성공했으나 `vue_docs_search`는 실제 호출에서 isError:true를 반환했습니다. 기본 의존 대상이 아닙니다. License도 OSI 승인이 아닌 FSL-1.1-ALv2이고, 한 사람이 단일 Hosted Endpoint 뒤에서 유지보수합니다.

## 이 Source는 아닙니다

Vue 질문에 Microsoft Learn으로 답하지 않습니다. Vue 2의 답을 Vue 3 Project로, 또는 그 반대로 옮기지 않습니다 — Reactivity System이 다릅니다.

질문을 엉뚱한 Server로 보내도 Error는 없습니다. 대신 다른 기술에 대한 자신만만한 답이 나오고, 그편이
더 나쁩니다.

## `dotnet/docs`와 Tool 이름을 공유합니다

GitMCP는 Repository 이름에서 Tool 이름을 만드는데, 이 Stack의 Repository와 `dotnet/docs`는 마지막
Segment가 같습니다. 둘 다 다음을 노출합니다:

- `fetch_docs_documentation`
- `search_docs_documentation`
- `search_docs_code`

**금지가 아니라 주의이며, 그 구분이 중요합니다.** 대부분의 Client는 Tool을 Server로 한정합니다 —
Claude Code는 `mcp__<server>__<tool>`로 보여 줍니다 — 그래서 둘 다 등록해도 따로 지정 가능한 Tool
두 개가 되고 충돌은 없습니다. 특정 Client가 이름을 평탄화하는지는 그 Client의 성질이며 여기서
시험하지 않았습니다.

어떤 Client에서든 남는 문제는, 선택하는 Model 입장에서 Base 이름이 같고 어느 Repository를 검색하는지
로만 목적이 갈리는 Tool 두 개가 보인다는 점입니다. 각 Tool의 *Description*이 자기 Repository를
밝히는지는 검증 실행에서 기록하지 않았으므로, Model이 둘을 얼마나 쉽게 구분하는지는 괜찮은 것이 아니라
unknown입니다.

값싼 대응이 둘 있습니다. Server 이름은 구분되고 설명적으로 유지합니다 — 밋밋한 `docs`가 아니라 위의
`vue-docs`처럼. Namespace를 쓰는 Client에서는 그 이름이 두 Tool을 가르는 유일한 단서입니다. 그리고 둘
다 등록했다면 선택을 추론에 맡기지 말고 요청에서 쓸 Server를 지정합니다.

## 우선순위

1. 이 Project의 Code, Manifest, Lock File.
2. Exit Code가 붙은 결정론적 Build 및 Test Evidence.
3. 위의 Server들, 나열된 순서대로.
4. Version 사이에 달라진 동작에 대한 공식 Release Notes.
5. Model Memory — Version 민감 Fact에는 쓰지 않습니다.

## 실제로 호출하게 만들기

Server 등록만으로 Model이 그것을 쓰지는 않습니다. 여기뿐 아니라 Project의 Agent 지침에도 들어가야 할
규칙:

- API, Version 동작, 구성 질문을 학습 지식만으로 답하지 않습니다;
- 먼저 그 Stack의 `search_*` Tool을 호출하고, 본문은 `fetch_*`로 가져옵니다;
- 문서와 구현이 어긋날 수 있으면 `search_*_code`로 교차 확인합니다;
- Repository의 기본 Branch가 이 Project에 설치된 Version과 같다고 가정하지 않습니다;
- 사용한 Repository, 경로, Version 또는 Commit을 밝힙니다;
- 검색에서 아무것도 찾지 못하면 그렇게 말합니다. 기억으로 빈칸을 메우지 않습니다.

## Version 민감 조회

기억하지 말고 항상 조회합니다:

- 어떤 Version이 API를 도입했거나 바꾸었는지;
- 구성 Key의 정확한 철자;
- 기본값 — 조용히 바뀌었을 가능성이 가장 큰 항목.

## Fallback

Project의 Version이 Source가 서술하는 Version과 다르면 **멈추고 불일치를 보고합니다**. 미해결 항목은
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.


## 밖으로 무엇이든 내보내기 전에

이들은 **공개된 제3자 Endpoint**입니다. 호출 한 번에 Query, Agent가 조립한 Tool 인자, 그리고 함께
넣은 Context가 전송됩니다. 거기에 비공개 Source, 고객 데이터, 내부 Hostname, 자격 증명, 미공개
Repository 이름, 가공되지 않은 운영 Log가 실릴 수 있습니다.

폐쇄망에서는 운영 의존 대상으로 삼지 않습니다. 공식 Repository를 내부에 Mirror하고, Commit을 고정하고,
Index를 만들고, 모든 답에 Repository, 경로, Commit, 조회 날짜를 반환하는 내부 읽기 전용 MCP를
운영합니다. 공개 Endpoint는 공개 기술 조사에만 씁니다.

## 연결하기

이 문서 옆의 `mcp-profile.json.example`에 표의 Server가 그대로 있습니다. Agent가 읽는 Adapter 설정으로
복사합니다:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`; MCP는 Client에서 설정 |

Kit의 Root 설정에는 이 문서의 모든 Server가 활성화된 채로 있습니다. 이것은 공개 Kit이고, Endpoint부터
찾아다니지 않아도 동작하게 만든 것입니다. 그 대가는 숨기지 않습니다. 검증 Guide 자신의 권고는 전부
담아 배포하는 것과 반대입니다. Project가 실제로 쓰는 Stack만 등록하면 "Tool 라우팅 오류와 불필요한
Tool Schema Context를 줄인다"고 되어 있습니다. 그러니 이 Project가 쓰지 않는 Stack의 Entry는
지우십시오 — 격하가 아니라 평범한 편집입니다. 그리고 폐쇄망에서 어느 하나라도 켜 둔 채로 두기 전에 위
절을 읽으십시오. 폐쇄망에서 맞는 답은 이 Endpoint가 아니라 내부 Mirror입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. 중요한 값은
Transport와 URL 둘뿐입니다.

`stdio`만 쓰는 Client라면:

```json
{
  "mcpServers": {
    "vue-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/vuejs/docs"]
    }
  }
}
```

## 다시 확인하기

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/vuejs/docs   --transport http --method tools/list --format json
```

Tool 이름이 바뀐 것은 사소한 사항이 아니라 Finding입니다. 위의 라우팅 규칙이 특정 Tool을 지목하고
있습니다.
