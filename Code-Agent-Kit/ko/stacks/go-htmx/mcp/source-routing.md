# Source Routing — Go + HTMX

아래 Server는 모두 **2026-08-05**에 MCP Inspector로 확인했습니다. 인증 없이
접속했고, Tool 목록을 냈고, 실제 `tools/call`에 답했습니다. 판정과 실행 기록,
그리고 무엇보다 *확인하지 않은 것*은
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
적혀 있습니다.

| Server | Endpoint | 판정 | Tool | 역할 |
|---|---|---|---:|---|
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | **PASS** | 4 | Project Repository, 문서와 Code |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | **PASS** | 3 | Repository 구조, 생성된 설명 |

전송 방식은 전부 **Streamable HTTP**입니다. 취향이 아닙니다. 같은 검사를 이전에 SSE로
돌렸을 때 모든 GitMCP Endpoint가 `405`를 냈습니다. Streamable HTTP를 못 쓰는
Client는 이 문서 끝에 나오는 `mcp-remote` Bridge가 필요합니다.

### `go-htmx-docs` — PASS

Endpoint: `https://gitmcp.io/donseba/go-htmx`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰한 노출 Tool:

- `fetch_go_htmx_documentation`
- `search_go_htmx_documentation`
- `search_go_htmx_code`
- `fetch_generic_url_content`

용도: Header 검사 Helper, Middleware, Component Rendering, SSE Code — 실제 함수가 어디 있는지.

### `deepwiki` — PASS

Endpoint: `https://mcp.deepwiki.com/mcp`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰한 노출 Tool:

- `ask_question`
- `read_wiki_contents`
- `read_wiki_structure`

용도: 어디에 있는지 찾기 전에, 조각들이 어떻게 연결되는지 파악할 때.

> **주의.** 이 Server의 답은 Model이 생성한 것입니다. 최종 인용으로 삼지 말고 GitMCP로 Repository에서 확인하십시오.

## 이 Source는 아닙니다

이런 질문에 Single-page Framework 문서로 답하지 않습니다. Client측 Router도 없고 Client State Store도 없습니다.

질문을 엉뚱한 Server로 보내도 오류는 나지 않습니다. 다른 기술에 대한 확신에 찬 답이
나오고, 그게 더 나쁩니다.


## 우선순위

1. 이 Project의 Code, Manifest, Lock File.
2. Exit Code를 포함한 결정론적 Build 및 Test Evidence.
3. 위 표의 Server, 적힌 순서대로.
4. 공식 Release Notes, Version 사이에 달라진 동작에 대해.
5. Model의 기억 — Version에 민감한 Fact에는 절대 쓰지 않습니다.

## 실제로 호출하게 만들기

Server를 등록했다고 Model이 그것을 쓰는 것은 아닙니다. 다음 Rule은 이 File뿐 아니라
Project의 Agent 지침에도 들어가야 합니다.

- API, Version별 동작, 구성에 관한 질문을 학습 지식만으로 답하지 않습니다;
- 그 Stack의 `search_*` Tool을 먼저 부르고, 본문은 `fetch_*`로 가져옵니다;
- 문서와 구현이 어긋날 수 있으면 `search_*_code`로 교차 확인합니다;
- Repository의 기본 Branch가 이 Project에 설치된 Version과 같다고 가정하지 않습니다;
- 사용한 Repository, 경로, Version 또는 Commit을 밝힙니다;
- 검색해서 없었으면 없었다고 말합니다. 기억으로 메우지 않습니다.

## Version에 민감한 조회

기억하지 말고 항상 조회합니다:

- 어떤 Version에서 API가 생기거나 바뀌었는지;
- 구성 Key의 정확한 철자;
- 기본값 — 조용히 바뀌었을 가능성이 가장 높은 것.

## Fallback

Project의 Version과 Source가 서술하는 Version이 다르면 **멈추고 그 불일치를
보고합니다**. 해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.


## 밖으로 내보내기 전에

이들은 **공개된 제3자 Endpoint**입니다. 호출 한 번에 Query, Agent가 조립한 Tool
인자, 그리고 함께 실어 보낸 Context가 나갑니다. 거기에는 비공개 Source, 고객 Data,
내부 Hostname, Credential, 공개되지 않은 Repository 이름, 가공되지 않은 운영 Log가
섞일 수 있습니다.

폐쇄망에서는 이들을 운영 의존성으로 삼지 마십시오. 공식 Repository를 내부에
Mirroring하고, Commit을 고정하고, Index를 만든 뒤, 답변마다 Repository, 경로,
Commit, 조회 날짜를 함께 돌려주는 내부 읽기 전용 MCP를 제공하십시오. 공개
Endpoint는 공개 기술 조사에만 씁니다.

## 연결하기

이 문서 옆의 `mcp-profile.json.example`에 위 표의 Server가 그대로 들어 있습니다.
Agent가 읽는 Adapter 설정으로 복사하십시오.

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`; MCP는 Client에서 구성 |

Kit의 Root 설정에는 이 문서의 모든 Server가 켜진 채로 들어 있습니다. 이것은 공개
Kit이고, Endpoint를 먼저 찾아 헤매지 않아도 동작하게 하려는 것입니다. 그 대가를
숨기지는 않겠습니다. 검증 가이드의 권고는 오히려 전부 담는 것의 반대입니다.
Project가 실제로 쓰는 Stack만 등록하면 "도구 라우팅 오류와 불필요한 도구 스키마
컨텍스트를 줄일 수 있다"고 적혀 있습니다. 그러니 이 Project가 쓰지 않는 Stack의
항목은 지우십시오. 그것은 정상적인 편집이지 기능 축소가 아닙니다. 그리고 폐쇄망에서
어느 하나라도 켜 둔 채로 두기 전에 위 절을 읽으십시오. 거기서는 이 Endpoint가 아니라
내부 Mirror가 정답입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`.
중요한 값은 전송 방식과 URL 둘뿐입니다.

`stdio`만 되는 Client라면:

```json
{
  "mcpServers": {
    "go-htmx-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/donseba/go-htmx"]
    }
  }
}
```

## 다시 확인하기

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/donseba/go-htmx   --transport http --method tools/list --format json
```

Tool 이름이 바뀌었다면 그것은 사소한 사항이 아니라 Finding입니다. 위 Routing Rule이
특정 Tool 이름을 지목하고 있기 때문입니다.
