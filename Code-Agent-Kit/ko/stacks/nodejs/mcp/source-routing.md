# Source Routing — Node.js

아래 Server는 모두 **2026-08-05**에 MCP Inspector로 검증했습니다. 자격 증명 없이
연결되었고, Tool 목록을 반환했으며, 실제 `tools/call`에 응답했습니다. 판정과 실행 기록,
그리고 무엇보다 *검증하지 않은 것*은
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
기록되어 있습니다.

| Server | Endpoint | 판정 | Tool 수 | 역할 |
|---|---|---|---:|---|
| `nodejs-docs` | `https://gitmcp.io/nodejs/node` | **PASS** | 4 | 공식 Repository, 문서/API와 Source |

Transport는 모두 **Streamable HTTP**입니다. 취향의 문제가 아닙니다. 같은 Checker를
이전에 SSE로 돌렸을 때 모든 GitMCP Endpoint가 `405`를 반환했습니다. Streamable HTTP를
말하지 못하는 Client는 `mcp-remote` Bridge가 필요하며, 그 방법은 이 문서 끝에 있습니다.

### `nodejs-docs` — PASS

Endpoint: `https://gitmcp.io/nodejs/node`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰한, 노출되는 Tool:

- `fetch_node_documentation`
- `search_node_documentation`
- `search_node_code`
- `fetch_generic_url_content`

용도: 원본 그대로의 API 문서, 그리고 문서가 Version 경계에 대해 모호할 때의 구현 Code.

## 이 Source는 아님

Browser JavaScript 문서로 Node 질문에 답하지 않습니다. Framework를 가정하지 않습니다. Node Project에 Framework가 없을 수도 있습니다.

질문을 엉뚱한 Server로 Routing해도 Error는 나지 않습니다. 대신 다른 기술에 대한 확신에
찬 답이 나오는데, 그게 더 나쁩니다.


## 우선순위

1. 이 Project의 Code, Manifest, Lock File.
2. Exit Code를 포함한 결정론적 Build 및 Test Evidence.
3. 위 Table의 Server. 나열된 순서대로.
4. 공식 Release Note. Version 사이에 바뀐 동작에 씁니다.
5. Model의 기억 — Version 민감 Fact에는 절대 쓰지 않습니다.

## 실제로 호출하게 만들기

Server를 등록했다고 Model이 그것을 쓰지는 않습니다. 아래 Rule은 여기뿐 아니라 Project의
Agent 지시문에도 들어가야 합니다.

- API, Version 동작, 설정에 관한 질문에 학습 지식만으로 답하지 않습니다;
- 먼저 그 Stack의 `search_*` Tool을 호출하고, 본문 자체는 `fetch_*`로 가져옵니다;
- 문서와 구현이 어긋날 수 있는 경우 `search_*_code`로 교차 확인합니다;
- Repository의 기본 Branch가 이 Project에 설치된 Version과 같다고 가정하지 않습니다;
- 사용한 Repository, 경로, Version 또는 Commit을 밝힙니다;
- 검색 결과가 없으면 없다고 말합니다. 빈자리를 기억으로 채우지 않습니다.

## Version 민감 조회

기억에 의존하지 말고 항상 찾아봅니다.

- 어떤 Version에서 API가 도입되거나 바뀌었는지;
- 설정 Key의 정확한 철자;
- 기본값. 조용히 바뀌었을 가능성이 가장 큰 항목입니다.

## Fallback

Project의 Version이 Source가 서술하는 Version과 다르면 **멈추고 불일치를 보고합니다**.
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 이름만 있고 검증하지 않음

아래는 Local `stdio` Server입니다. 검증 실행에 **포함되지 않았으므로** 여기 있는 무엇도
그것이 동작한다는 뜻이 아닙니다. 아무도 다시 찾아 헤매지 않도록 이름을 적어 두었고,
아무도 이름을 Test로 착각하지 않도록 표시해 두었습니다.

**`nodejs-api-docs`** — `snyk-labs/mcp-server-nodejs-api-docs`

검증 실행에 없었고, Repository를 살펴본 결과도 좋지 않습니다. Star 9개, Commit 36개, Release 없음, Open Issue 0개에 Open Pull Request 42개 — Dependency Bot만 쌓이는 방치된 Repository의 모양입니다. `snyk-labs`는 실험용 Org입니다.

## 바깥으로 무언가 보내기 전에

이들은 **공개된 서드파티 Endpoint**입니다. 호출 한 번에 질의, Agent가 조립한 Tool 인자,
그리고 Agent가 함께 넣은 Context가 나갑니다. 거기에는 비공개 Source, 고객 데이터,
내부 Hostname, 자격 증명, 공개되지 않은 Repository 이름, 가공 없는 운영 Log가 실릴 수
있습니다.

폐쇄망에서는 이것을 운영 의존성으로 삼지 마십시오. 공식 Repository를 내부에 Mirror하고,
Commit을 고정하고, Index를 만들고, 답마다 Repository, 경로, Commit, 조회 날짜를 함께
돌려주는 내부 읽기 전용 MCP를 제공하십시오. 공개 Endpoint는 공개 기술 조사에만
사용합니다.

## 연결

이 문서 옆의 `mcp-profile.json.example`에 위 Table의 Server가 그대로 들어 있습니다.
Agent가 읽는 Adapter 설정에 복사하십시오.

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`, MCP는 Client에서 설정 |

Kit의 Root 설정에는 이 문서의 모든 Server가 활성화된 채로 들어 있습니다.
이것은 공개 Kit이고, 누구도 Endpoint부터 찾아다니지 않아도 동작하게 하려는 것입니다.
그 대가는 숨기지 않습니다. 검증 Guide 자신의 권고는 전부 싣는 것과 반대입니다.
Project가 실제로 쓰는 Stack만 등록하면 "Tool Routing 오류와 불필요한 Tool Schema
Context가 줄어든다"고 적혀 있습니다. 그러니 이 Project가 쓰지 않는 Stack의 항목은
지우십시오. 그것은 정상적인 편집이지 격하가 아닙니다. 그리고 폐쇄망에서 무엇이든
켜 둔 채로 두기 전에 위 절을 읽으십시오. 폐쇄망의 정답은 이 Endpoint가 아니라 내부
Mirror입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`.
중요한 값은 Transport와 URL 둘뿐입니다.

`stdio`만 말하는 Client라면:

```json
{
  "mcpServers": {
    "nodejs-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/nodejs/node"]
    }
  }
}
```

## 다시 확인하기

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/nodejs/node   --transport http --method tools/list --format json
```

Tool 이름이 바뀌었다면 그것은 사소한 사항이 아니라 Finding입니다. 위의 Routing Rule이
특정 Tool 이름을 지목하고 있기 때문입니다.
