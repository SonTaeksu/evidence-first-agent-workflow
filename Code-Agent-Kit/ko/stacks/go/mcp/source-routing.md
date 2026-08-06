# Source Routing — Go

아래의 모든 Server는 **2026-08-05**에 MCP Inspector로 확인했습니다. 인증 없이
접속했고, Tool 목록을 냈고, 실제 `tools/call`에 답했습니다. 판정과 실행 기록,
그리고 무엇보다 *확인하지 않은* 것은
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
적혀 있습니다.

| Server | Endpoint | 판정 | Tools | 역할 |
|---|---|---|---:|---|
| `go-docs` | `https://gitmcp.io/golang/go` | **PASS** | 4 | 공식 Repository, 언어와 표준 Library |

전송 방식은 전부 **Streamable HTTP**입니다. 취향이 아닙니다. 같은 검사를 앞서 SSE로
돌렸을 때 모든 GitMCP Endpoint가 `405`를 냈습니다. Streamable HTTP를 못 쓰는
Client는 이 문서 끝에 나오는 `mcp-remote` Bridge가 필요합니다.

### `go-docs` — PASS

Endpoint: `https://gitmcp.io/golang/go`  (Streamable HTTP)

문서에 적힌 것이 아니라 실제로 관측된, 노출되는 Tool:

- `fetch_go_documentation`
- `search_go_documentation`
- `search_go_code`
- `fetch_generic_url_content`

쓰임새: 표준 Library 문서와 그 구현, 그리고 언어 규칙이 언제 바뀌었는지 기록한 Release Note.

## 이 Source는 아닙니다

다른 언어의 동시성 문서나 Error 문서를 근거로 Go 질문에 답하지 않습니다. Framework를 가정하지 않습니다. 이 Stack은 표준 Library가 전부인 경우가 많습니다.

질문을 엉뚱한 Server로 보내도 Error는 나지 않습니다. 다른 기술에 대한 확신에 찬 답이
나오고, 그게 더 나쁩니다.


## 우선순위

1. 이 Project의 코드, Manifest, Lock File.
2. exit code가 딸린 결정론적 Build 및 Test Evidence.
3. 위의 Server들, 적힌 순서대로.
4. 공식 Release Note. Version 사이에 동작이 바뀐 경우.
5. 모델 기억 — Version에 민감한 사실에는 절대 쓰지 않습니다.

## 애초에 호출하게 만들기

Server를 등록했다고 모델이 그것을 쓰는 것은 아닙니다. 다음 규칙은 여기뿐 아니라
Project의 Agent 지침에 들어가야 합니다.

- API, Version별 동작, 설정에 관한 질문을 학습 지식만으로 답하지 않습니다;
- Stack의 `search_*` Tool을 먼저 부르고, 본문은 `fetch_*`로 가져옵니다;
- 문서와 구현이 어긋날 수 있으면 `search_*_code`로 교차 확인합니다;
- Repository의 기본 Branch가 이 Project에 설치된 Version과 같다고 가정하지 않습니다;
- 사용한 Repository, 경로, Version 또는 Commit을 밝힙니다;
- 검색해서 없었으면 없었다고 말합니다. 기억으로 메우지 않습니다.

## Version에 민감한 조회

기억하지 말고 반드시 찾아볼 것:

- 어떤 Version에서 API가 생기거나 바뀌었는지;
- 설정 Key의 정확한 철자;
- 기본값. 조용히 바뀌었을 가능성이 가장 큰 항목입니다.

## Fallback

Project의 Version과 Source가 설명하는 Version이 다르면 **멈추고 그 불일치를
보고합니다**. 그리고 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 이름만 있고 검증하지 않은 것

아래는 Local `stdio` Server입니다. 검증한 실행에 **포함되지 않았으므로**, 여기
적힌 어떤 것도 동작을 보장하지 않습니다. 아무도 다시 찾아 헤매지 않도록 이름을
적어 두되, 이름을 시험으로 착각하지 않도록 표시해 둡니다.

**`gopls`** — `gopls mcp`

Go의 공식 Language Server에는 *현재* Project를 분석하는 실험적 MCP Mode가 있습니다. gopls v0.20 이상이 필요합니다. 검증한 실행에는 포함되지 않았습니다.

## 바깥으로 보내기 전에

이들은 **공개된 제3자 Endpoint**입니다. 호출 한 번에 질의, Agent가 조립한 Tool
인자, 그리고 그것이 함께 넣은 Context가 나갑니다. 거기에는 비공개 소스, 고객
데이터, 내부 Hostname, 자격 증명, 공개되지 않은 Repository 이름, 가공되지 않은 운영
Log가 실릴 수 있습니다.

폐쇄망에서는 이들을 운영 의존성으로 삼지 마십시오. 공식 Repository를 내부에 Mirror하고,
Commit을 고정하고, Index를 만들고, 모든 답변에 Repository·경로·Commit·조회 날짜를
돌려주는 내부 읽기 전용 MCP를 제공하십시오. 공개 Endpoint는 공개 기술을 조사할
때만 씁니다.

## 연결하기

이 문서 옆의 `mcp-profile.json.example`에 위 표의 Server가 그대로 들어 있습니다.
Agent가 읽는 Adapter 설정으로 복사해 넣으십시오.

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | 규칙은 `.clinerules/`, MCP는 Client에서 설정 |

Kit의 Root 설정에는 이 문서의 모든 Server가 켜진 채로 들어 있습니다. 이것은 공개
Kit이고, 아무도 Endpoint를 찾아 헤매지 않아도 동작하게 하려는 것입니다. 그 대가를
숨기지는 않겠습니다. 검증 가이드 자신의 권고는 전부 넣어 배포하는 것과 정반대입니다.
Project가 실제로 쓰는 Stack만 등록하면 "Tool Routing Error와 불필요한 Tool Schema
Context를 줄일 수 있다"고 적혀 있습니다. 그러니 이 Project가 쓰지 않는 Stack의
항목은 지우십시오. 그것은 정상적인 편집이지 기능 축소가 아닙니다. 그리고 폐쇄망에서
무엇이든 켜 두기 전에 위 Section을 읽으십시오. 거기서는 이 Endpoint들이 아니라 내부
Mirror가 정답입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`.
중요한 값은 전송 방식과 URL 두 가지입니다.

`stdio`만 되는 Client라면:

```json
{
  "mcpServers": {
    "go-docs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://gitmcp.io/golang/go"]
    }
  }
}
```

## 다시 확인하기

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/golang/go   --transport http --method tools/list --format json
```

Tool 이름이 바뀌었다면 그것은 사소한 일이 아니라 하나의 발견입니다. 위의 Routing
규칙이 특정 Tool 이름을 지목하고 있기 때문입니다.
