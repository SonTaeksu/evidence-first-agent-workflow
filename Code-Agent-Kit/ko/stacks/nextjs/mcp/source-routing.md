# Source Routing — Next.js

아래 Server는 모두 **2026-08-05**에 MCP Inspector로 검증했습니다. 자격 증명 없이 연결하고,
Tool 목록을 받고, 실제 `tools/call`에 응답하는 것까지 확인했습니다. 판정, 실행 기록,
그리고 무엇보다 *무엇을 검증하지 않았는지*는
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
기록되어 있습니다.

| Server | Endpoint | 판정 | Tool | 역할 |
|---|---|---|---:|---|
| `nextjs-docs` | `https://gitmcp.io/vercel/next.js` | **PASS** | 4 | 공식 Repository, 문서와 Source |

Transport는 전부 **Streamable HTTP**입니다. 취향의 문제가 아닙니다. 같은 검사기를 이전에
SSE로 돌렸을 때 GitMCP Endpoint가 전부 `405`를 냈습니다. Streamable HTTP를 쓰지 못하는
Client는 이 문서 끝에 있는 `mcp-remote` Bridge가 필요합니다.

### `nextjs-docs` — PASS

Endpoint: `https://gitmcp.io/vercel/next.js`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관찰한, 노출되는 Tool:

- `fetch_next_js_documentation`
- `search_next_js_documentation`
- `search_next_js_code`
- `fetch_generic_url_content`

용도: App Router와 Pages Router Page, Route Segment 설정, 설치된 Major Version의 Caching 및 Rendering 동작.

## 이 Source는 아닙니다

Rendering, Caching, Routing이 얽힌 Next.js 질문에 일반 React 문서로 답하지 않습니다. Framework가 그 동작을 바꿉니다. App Router와 Pages Router 지침을 섞지 않습니다.

질문을 잘못된 Server로 보내도 Error는 나지 않습니다. 대신 다른 기술에 대한 자신만만한
답이 나오는데, 그쪽이 더 나쁩니다.


## 우선순위

1. 이 Project의 Code, Manifest, Lock File.
2. Exit Code를 갖춘 결정론적 Build 및 Test Evidence.
3. 위 Server들, 표에 적힌 순서대로.
4. Version 사이에 바뀐 동작에 대한 공식 Release Note.
5. 모델 기억 — Version에 민감한 Fact에는 절대 쓰지 않습니다.

## 애초에 호출하게 만들기

Server를 등록한다고 모델이 그것을 쓰지는 않습니다. 다음 규칙은 여기만이 아니라 Project의
Agent 지침에 들어가야 합니다.

- API, Version 동작, 설정에 관한 질문을 학습 지식만으로 답하지 않는다;
- 먼저 그 Stack의 `search_*` Tool을 호출하고, 해당 대목 자체는 `fetch_*`로 가져온다;
- 문서와 구현이 어긋날 수 있으면 `search_*_code`로 교차 확인한다;
- Repository의 기본 Branch가 이 Project의 설치 Version과 같다고 절대 가정하지 않는다;
- 사용한 Repository, 경로, Version 또는 Commit을 밝힌다;
- 검색으로 아무것도 찾지 못했으면 그렇다고 말한다. 그 빈자리를 기억으로 채우지 않는다.

## Version에 민감한 조회

기억하지 말고 항상 조회합니다:

- 어떤 Version이 API를 도입했거나 바꿨는지;
- 설정 Key의 정확한 철자;
- 기본값. 조용히 바뀌었을 가능성이 가장 큰 것입니다.

## Fallback

Project의 Version이 Source가 서술하는 Version과 다르면 **멈추고 불일치를 보고합니다**.
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 이름만 적고 검증하지 않은 것

이들은 Local `stdio` Server입니다. 검증 실행에 **포함되지 않았으므로**, 여기 있는 어떤
문장도 이들이 동작한다고 말하지 않습니다. 아무도 다시 찾아 헤매지 않도록 이름을 적어
두었고, 이름을 시험으로 착각하지 않도록 표시해 두었습니다.

**`next-devtools`** — `npx -y next-devtools-mcp@latest`

Vercel이 직접 만든 것으로, 문서를 읽는 용도가 아니라 *실행 중인* Project를 진단하는 용도입니다. 검증 실행에는 포함되지 않았습니다.

## 밖으로 무엇이든 내보내기 전에

이들은 **공개된 서드파티 Endpoint**입니다. 호출 한 번에 질의, Agent가 조립한 Tool 인자,
그리고 함께 실린 Context가 전송됩니다. 거기에는 비공개 Source, 고객 데이터, 내부 Hostname,
자격 증명, 공개되지 않은 Repository 이름, 가공되지 않은 운영 Log가 실릴 수 있습니다.

폐쇄망에서는 이것들을 운영 의존성으로 삼지 않습니다. 공식 Repository를 내부에 Mirroring하고,
Commit을 고정하고, 색인한 다음, 모든 답에 Repository, 경로, Commit, 조회 날짜를 함께
반환하는 내부 읽기 전용 MCP를 제공합니다. 공개 Endpoint는 공개 기술 조사에만 씁니다.

## 연결

이 문서 옆의 `mcp-profile.json.example`에 위 표의 Server가 그대로 들어 있습니다. Agent가
읽는 Adapter 설정으로 복사합니다.

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`; MCP는 Client에서 설정 |

Kit의 Root 설정에는 이 문서의 모든 Server가 켜진 채로 들어 있습니다. 이것은 공개 Kit이고,
누구도 Endpoint를 먼저 찾아 헤매지 않아도 동작하도록 만든 것입니다. 그 대가는 숨기지
않습니다. 검증 가이드 자신의 권고는 전부 실어 보내는 것과 정반대입니다. Project가 실제로
쓰는 Stack만 등록하면 "도구 라우팅 오류와 불필요한 도구 스키마 컨텍스트를 줄일 수 있다"고
적혀 있습니다. 그러니 이 Project가 쓰지 않는 Stack의 항목은 지우십시오. 그것은 정상적인
편집이지 기능 축소가 아닙니다. 그리고 폐쇄망에서 어느 하나라도 켜 둔 채로 두기 전에 위
절을 읽으십시오. 거기서 옳은 답은 이 Endpoint들이 아니라 내부 Mirror입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. 중요한
값은 Transport와 URL 두 가지입니다.

`stdio`만 쓰는 Client라면:

```json
{
  "mcpServers": {
    "nextjs-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/vercel/next.js"]
    }
  }
}
```

## 재검사

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/vercel/next.js   --transport http --method tools/list --format json
```

바뀐 Tool 이름은 사소한 부분이 아니라 Finding입니다. 위 Routing 규칙이 특정 Tool 이름을
지목하고 있기 때문입니다.
