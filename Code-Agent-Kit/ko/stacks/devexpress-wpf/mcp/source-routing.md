# Source Routing — DevExpress WPF (v24.2+)

이 Stack은 서로 다른 두 종류의 Source로 라우팅하며, 그 갈림이 전부입니다.
**DevExpress는 자기 Control을 문서화하고 Microsoft는 하지 않습니다.** 둘 중 엉뚱한 쪽이
답한 질문은 확신에 차서 틀린 채로 돌아옵니다.

아래 Server 가운데 둘은 **2026-08-05**에 MCP Inspector로 확인했습니다. 인증 없이
접속했고, Tool 목록을 냈고, 실제 `tools/call`에 답했습니다. 그 판정은
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
적혀 있습니다.

DevExpress Endpoint에는 **2026-08-06**에 따로 접속했습니다. 인증 없이 연결되었고
`tools/list`를 돌려주었으므로, 아래의 Tool 이름 둘과 그 입력 Schema는 이제 읽어 온 것이
아니라 **측정된** 것입니다. 다만 그 문서의 열네 Server만큼 멀리 가지는 않았습니다.
**실제 `tools/call`은 이 Endpoint에 대해 한 번도 실행되지 않았습니다.** 그들의 `PASS`는 이
Endpoint가 얻어 낸 것보다 강한 등급이며, 이 문서는 그것을 빌려 오지 않습니다. 둘을
같은 것으로 취급하기 전에 아래 "2026-08-06 실행이 확립한 것과 확립하지 않은 것"을
읽으십시오.

| Server | Endpoint | 판정 | Tool | 역할 |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **TOOLS LISTED, NOT CALLED** (2026-08-06) | 측정 2 | DevExpress 공식 문서, 최신 |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **NOT SEPARATELY EXERCISED** | 문서상 2 | 같은 것을 v24.2에 고정 |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | Microsoft 공식 문서 — 평범한 WPF, XAML, .NET |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | **PASS** | 4 | WPF 개념 문서를 Source에서 직접 |

전송 방식은 전부 **Streamable HTTP**입니다. DevExpress Endpoint에서는 그것이 취향이 아니라
유일하게 지원되는 전송 방식입니다. Browser로 그 URL을 열면 `405 Method Not Allowed`가
돌아오고, DevExpress 문서는 이 응답이 결함이 아니라 예상된 것이라고 밝히고 있습니다.
따라서 Browser에서 받은 `405`는 Server가 죽었다고 결론지을 근거가 아닙니다. Streamable
HTTP를 못 쓰는 Client는 이 문서 끝에 나오는 `mcp-remote` Bridge가 필요합니다.

## DevExpress Server

아래의 Endpoint, 전송 방식, `?v=` 고정, 그리고 Prompt 이름은 **2026-06-16**에 읽은
DevExpress 공식 문서에서 가져온 것입니다. "### Tool" 아래의 Tool 이름과 입력 Schema는
종류가 다릅니다. 그것은 **2026-08-06**의 실제 MCP Inspector 실행에서 받은 `tools/list`
응답에서 읽어 낸 것이며, 문서에 적힌 것이 아니라 관찰된 것입니다.

Endpoint: `https://api.devexpress.com/mcp/docs`  (Streamable HTTP, **인증 없음**)

### Version 고정

Version은 `?v=` Query Parameter로 선택합니다. 문서에 나온 예시는 다음과 같습니다:

```
https://api.devexpress.com/mcp/docs?v=24.2
```

**고정은 v24.2보다 이른 Version에서는 지원되지 않습니다.** v16.x나 그 밖의 24.2 이전
Release를 고정할 지원되는 방법은 없으며, 이 Stack Profile의 적용 범위가 DevExpress WPF
일반이 아니라 v24.2 이상인 이유가 그것입니다.

### Tool

둘, 오직 둘입니다. 아래 두 Schema는 모두 2026-08-06 `tools/list` 응답에서 옮겨 적은
것입니다.

#### `devexpress_docs_search`

문서에 대한 의미 검색입니다. 자기 설명이 스스로 속한 Workflow의 형태를 밝히고 있습니다.
아래는 그 설명을 그대로 옮긴 것입니다:

> Search DevExpress documentation for a given technology and a question. If you
> want to search for multiple technologies, pass them as a list. This tool
> returns only snippets/excerpts; full content requires a follow-up
> `devexpress_docs_get_content` call on a chosen URL. ALWAYS call
> `devexpress_docs_search` before ANY `devexpress_docs_get_content` call in a
> user request chain.

두 Property 모두 **필수**입니다:

| Property | Type | 비고 |
|---|---|---|
| `technologies` | array, `minItems: 1` | 항목은 **닫힌 enum**입니다 — 아래 참고 |
| `question` | string | "Your specific question or search query. Be descriptive and include relevant keywords about what you're trying to accomplish." |

`technologies`는 자유 Text가 아닙니다. Schema 자체의 설명은 이렇게 말합니다: "Use specific
technology names like 'WindowsForms', 'XtraReports', 'OfficeFileAPI' etc. You
must choose from the allowed set." 허용된 값의 전체 목록:

```text
Angular              AspNet               AspNetBootstrap      AspNetCore
AspNetMvc            ASPxThemeBuilder     ASPxThemeDeployer    Blazor
CodedUIExtension     CoreLibraries        Dashboard            DesignSystem
DevExtremeAspNetMvc  eud                  eXpressAppFramework  GeneralInformation
jQuery               MAUI                 OfficeFileAPI        OfficeFileApiJava
React                ReportServer         SkinEditor           VCL
Vue                  WindowsForms         WPF                  WpfThemeDesigner
XPO                  XpoProfiler          XtraReports
```

서른한 개이고, 그 밖의 어떤 것도 받아들여지지 않습니다. 이 Stack이 그중 무엇을 쓰는지는
아래 "Routing Rule"에 있습니다.

#### `devexpress_docs_get_content`

URL로 도움말 Topic 전체를 내려받습니다. 그 설명은 다음과 같습니다:

> Get full document content by URL from DevExpress documentation. PREREQUISITE:
> ALWAYS call `devexpress_docs_search` before using this tool to get valid URLs.
> The URL parameter must be obtained from the results of the
> `devexpress_docs_search` tool.

필수 Property는 하나입니다:

| Property | Type | 비고 |
|---|---|---|
| `url` | string | "REQUIRED: This URL must be obtained from a previous call to `devexpress_docs_search` tool. **Do not construct URLs using your general knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`" |

### 기록해 두는 정정

이 문서의 이전 판은, 다른 곳에서 돌아다니던 Schema — `technologies` 배열에 필수
`question`을 더한 것 — 가 문서화된 Tool 이름과 **모순된다**고 적었고, 그것을 Schema가
아니라 미확인 항목으로 기록했습니다.

그것은 틀렸고, 측정이 그 점을 분명히 말해 줍니다. 그것은 정확히
`devexpress_docs_search`의 입력 Schema입니다. 돌아다니던 주장이 옳았고, 그것을 물리친
추론이 옳지 않았습니다.

잘못은 Fact 하나가 아니라 추론 한 단계였습니다. DevExpress 공식 문서는 Tool 이름을
공개하고 그 입력 Schema는 공개하지 않습니다. 문서에 없다는 것이 문서와 충돌한다는 것으로
읽혔고, 그 둘은 다른 것입니다. **"문서에 없음"은 "문서에 의해 반박됨"이 아닙니다.**
공개되지 않은 Schema에 붙일 올바른 딱지는 *unknown*이며, 그것은 측정을 부릅니다.
*contradicted*는 판정이고, 이 문서에는 그것을 내릴 Evidence가 없었습니다.

원래의 경계는 그 나름의 근거로 여전히 유효합니다. 아무도 호출해 본 적 없는 Tool에
그럴듯한 Schema를 써 주는 것은 이 Kit이 막으려고 존재하는 종류의 창작이고, 틀린 Schema는
Server가 고장 난 것처럼 읽히는 방식으로 호출 시점에 실패합니다. 확인되지 않은 Schema를
베끼기를 거절한 것은 옳았습니다. 그것을 거짓이라고 선언한 것은 옳지 않았습니다. 이 정정은
지워 없애지 않고 여기 남겨 둡니다. 삭제된 판본의 잘못은 아무에게도 아무것도 가르쳐 주지
않기 때문입니다.

### 미리 정의된 Prompt

Server는 Prompt를 하나 공개합니다: `mcp.dxdocs.devexpress_docs_query_workflow`.

### 2026-08-06 실행이 확립한 것과 확립하지 않은 것

Owner의 Machine에서 Windows Shell로 실행한 명령:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

성공적으로 응답했습니다. **확립된 것:**

- 이 Endpoint는 평범한 개발자 Machine에서 Streamable HTTP로 응답한다;
- **Credential을 요구하지 않는다.** 아무것도 제공하지 않았고 아무것도 요구받지 않았다;
- 정확히 두 개의 Tool을, 문서가 밝힌 이름 그대로 노출한다;
- 닫힌 `technologies` enum을 포함해, 위에 옮겨 적은 전체 입력 Schema.

**확립되지 않았고, 그렇게 암시해서도 안 되는 것:**

- **실제 `tools/call`은 실행되지 않았습니다.** `tools/list`는 전송, 도달 가능성, 형태를
  증명합니다. 검색이 쓸 만한 결과를, 아니 결과라는 것 자체를 돌려주는지는 증명하지
  않습니다. `docs/core/mcp-source-verification.md`에 `PASS`로 기록된 열네 Server는 실제
  인자를 넣은 실제 호출로 채점되었습니다. 이 Endpoint는 거기까지 가지 않았으므로 그
  판정을 가지지 않습니다. 여기서의 등급은 **Tool 목록은 냈으나 호출은 하지 않음**이며,
  적히는 곳마다 그렇게 적혀야 합니다.
- **`?v=24.2`는 따로 시험되지 않았습니다.** 이 실행은 고정되지 않은 URL만 다뤘습니다.
  Version 고정은 여전히 *문서상의* 사실로 남아 있으며 — 이 절의 앞 절반 전체가 기대고 있는
  구분입니다 — `dxdocs24_2`가 오직 그 이유만으로 `dxdocs`보다 약한 판정을 유지합니다.
- 답변 품질, 가동률, 기본 Version이 특정 Project의 설치 Version과 맞는지에 관해서는
  아무것도. 그것들은 애초에 범위에 없었습니다.

작성 환경에서의 이전 시도는 실패했고, 그 실패는 DevExpress에 관한 Evidence가 아니라
환경 문제로 옳게 읽혔습니다. 2026-08-05 실행에서 이미 `PASS`를 받아 둔 Endpoint 둘 —
`https://gitmcp.io/vuejs/docs`와 `https://mcp.deepwiki.com/mcp` — 이 같은 Session에서
똑같이 실패했기 때문입니다:

```json
{"code":"unreachable","cause":"invalid onRequestStart method"}
```

전에는 통과했는데 지금 실패하는 Endpoint가, 같은 방식으로 실패하는 새 Endpoint와 나란히
있다면 그것은 망가진 Client이거나 막힌 Network입니다. 그때 판정을 미룬 것은 옳았고,
정상 동작하는 Client에서 돌린 2026-08-06 실행이 이제 판정을 제공하며, 앞선 실패가 이
Server에 대해 아무 말도 하지 않았음을 확인해 줍니다.

## Routing Rule

- DevExpress Control, 그 View, Theme, MVVM Framework, Docking에 관한 질문은
  **`dxdocs`**로 갑니다.
- WPF, XAML, Binding, Dependency Property, Dispatcher, Resource, 그리고 .NET에 속한
  모든 것에 관한 질문은 `../../csharp-wpf/mcp/source-routing.md`에 따라
  **`microsoft-learn`** 또는 **`wpf-docs`**로 갑니다.
- **DevExpress API 질문에 `microsoft-learn`이나 `wpf-docs`나 기억으로 절대 답하지
  않습니다.** Microsoft는 이 Control들을 문서화하지 않으므로 앞의 둘은 다른 기술에 관한
  답을 내놓고, 기억은 대개 실제로도 존재하는 Member 이름을 내놓습니다. 그 말은 Compile된다는
  뜻이고, 그래서 잘못이 Build Log가 아니라 Production에 도달합니다.
- v24.2 Project에서는 최신 Endpoint가 아니라 **`dxdocs24_2`**를 씁니다. 최신 문서는 최신
  Release를 서술하며, 고정된 Project에 그것을 읽는 순간 이 Stack의 Version 규율 전체가
  무너집니다.
- 둘이 섞인 질문 — 이를테면 평범한 `Binding`으로 묶인 DevExpress Control — 은 조회 하나가
  아니라 둘입니다.

### Server 스스로 밝히는 Rule 둘

둘 다 `tools/list`가 돌려준 Tool 설명에서 나온 것입니다. 이 Kit의 취향이 아니라 Server
자신의 Rule이며, 이것을 무시하는 Agent는 자기가 부르고 있는 Tool과 말다툼하는 셈입니다:

- **한 요청 사슬에서 `devexpress_docs_get_content` 호출 전에는 언제나
  `devexpress_docs_search`를 먼저 부릅니다.** 검색은 Snippet만 돌려주고, Topic 전문은 두
  번째 호출이 필요합니다. `devexpress_docs_get_content`에서 시작하는 지원되는 경로는
  없습니다.
- **문서 URL을 기억으로 지어내지 않습니다.** `url` 인자는 앞선 검색이 돌려준 것이어야
  합니다 — *"Do not construct URLs using your general knowledge."* 추측한 URL이 실패하는
  방식은 둘인데 그중 안전한 것은 하나뿐입니다. 404가 나거나, 묻고 있는 것이 아닌 실제
  Topic으로 해석되거나입니다. 두 번째는 성공한 조회와 똑같이 읽힙니다.

### 이 Stack의 `technologies` 값

`technologies`는 닫힌 enum입니다. Agent는 Platform의 산문식 이름이 아니라 **enum 값**을
넘깁니다. `WPF`이고, `"DevExpress WPF"`나 `"wpf"`나 `".NET WPF"`가 아닙니다. 허용된 집합
밖의 값은 **Schema 검증 오류**입니다. 호출이 거부되지, 빈 결과로 돌아오지 않습니다. 그래서
아깝게 빗나간 값이 누군가 써 버릴 만한 빈약한 답으로 주저앉지 않습니다. 요란하게 실패하고,
이번만큼은 그것이 좋은 경우입니다.

| 무엇에 관한 질문인가 | 값 |
|---|---|
| DevExpress WPF Control, View, Theme, MVVM Framework, Docking | `WPF` |
| WPF Theme Designer 도구 | `WpfThemeDesigner` |
| DevExpress Platform 전반이 공유하는 Base Type | `CoreLibraries` |

이 Property는 `minItems: 1`인 배열이므로 둘 이상을 넘길 수 있습니다. 공유 Base Type까지
닿는 WPF 질문이라면 `["WPF", "CoreLibraries"]`가 합당합니다.

요구되는 두 단계 사슬을 구체적으로 쓰면:

```json
{
  "name": "devexpress_docs_search",
  "arguments": {
    "technologies": ["WPF"],
    "question": "How do I persist and restore a DockLayoutManager layout per user?"
  }
}
```

그다음, 오직 검색이 돌려준 URL에 대해서만:

```json
{
  "name": "devexpress_docs_get_content",
  "arguments": {
    "url": "<copied verbatim from a result of the search above>"
  }
}
```

여기에 URL을 하나도 적어 두지 않은 것은 의도입니다. 이 문서에 적힌 URL은 Agent가 검색 없이
복사할 수 있는 URL이고, 그것은 위 Rule이 자기 예시에 의해 무너지는 것입니다.

## 이 Source는 아닙니다

DevExpress 질문을 Package 문서 Server나 Microsoft Learn이나 일반 Web 검색으로 보내지
않습니다. 평범한 WPF 질문을 `dxdocs`로 보내지도 않습니다. 그것은 DevExpress를 문서화하며,
Vendor의 문서가 답한 Framework 질문은 그 Vendor가 Framework를 대체하려고 내놓은 것을
서술한 채 돌아옵니다.

질문을 엉뚱한 Server로 보내도 오류는 나지 않습니다. 다른 기술에 대한 확신에 찬 답이
나오고, 그게 더 나쁩니다.

## 우선순위

1. 이 Project의 Code, Manifest, 복원 출력.
2. Exit Code를 포함한 결정론적 Build 및 Test Evidence.
3. 위 표의 Server, 적힌 순서대로 — DevExpress에는 `dxdocs`, Framework에는
   `microsoft-learn`과 `wpf-docs`.
4. 공식 Release Notes, Version 사이에 달라진 동작에 대해.
5. Model의 기억 — Version에 민감한 Fact에는 절대 쓰지 않고, DevExpress에 관한 것에는
   아예 쓰지 않습니다.

## 실제로 호출하게 만들기

Server를 등록했다고 Model이 그것을 쓰는 것은 아닙니다. 다음 Rule은 이 File뿐 아니라
Project의 Agent 지침에도 들어가야 합니다.

- API, Version별 동작, 구성에 관한 질문을 학습 지식만으로 답하지 않습니다;
- 먼저 검색하고 그다음 본문 자체를 가져옵니다. `dxdocs`에서는 `devexpress_docs_search`를
  부른 뒤 검색이 돌려준 URL에 대해 `devexpress_docs_get_content`를 부르는 것이며, Server가
  그렇게 요구하므로 순서도 그대로입니다;
- `devexpress_docs_search`는 상위 다섯 건을 돌려줍니다(2026-06-16에 문서로 확인. 2026-08-06에
  측정한 Tool 설명은 Snippet을 돌려준다고만 하고 개수는 밝히지 않습니다). 다섯은 전수
  조사가 아닙니다. 그중 어느 것도 문제의 정확한 Control과 Version에 관한 것이 아니라면,
  가장 가까운 것으로 답하지 말고 그렇다고 말합니다;
- Endpoint의 기본 Version이 이 Project에 설치된 Version과 같다고 가정하지 않습니다. `?v=`가
  있는 이유가 그것입니다;
- 사용한 Topic URL과 Version을 밝힙니다;
- 검색해서 없었으면 없었다고 말합니다. 기억으로 메우지 않습니다.

## Version에 민감한 조회

기억하지 말고 항상 조회합니다:

- 어떤 Version에서 Control Member가 생기거나 바뀌었는지;
- Property의 정확한 철자, 그리고 그것이 어느 Type에 사는지 — 이 Stack에서는 Grid가 아니라
  Grid의 View인 경우가 가장 많습니다;
- 기본값 — 조용히 바뀌었을 가능성이 가장 높은 것.

## Fallback

Project의 Version과 Source가 서술하는 Version이 다르면 **멈추고 그 불일치를
보고합니다**. 해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

v24.2 미만의 Project는 이 상황을 곧바로 맞닥뜨리고 문서화된 탈출구가 없습니다. `?v=`는
거기까지 거슬러 닿지 않습니다. 최신 문서로 근사하지 말고 그 상황을 그대로 기록하십시오.

## 밖으로 내보내기 전에

이들은 **공개된 제3자 Endpoint**입니다. 호출 한 번에 Query, Agent가 조립한 Tool
인자, 그리고 함께 실어 보낸 Context가 나갑니다. 거기에는 비공개 Source, 고객 Data,
내부 Hostname, Credential, 공개되지 않은 Repository 이름, 가공되지 않은 운영 Log가
섞일 수 있습니다.

`dxdocs`는 인증을 받지 않습니다. 그래서 켜기가 쉬울 뿐, 그것이 사적이라는 뜻은 아닙니다.
그것은 Vendor의 Endpoint이고, Agent가 거기에 보내는 Query는 지금 무엇을 만들고 있는지를
서술합니다.

폐쇄망에서는 이들을 운영 의존성으로 삼지 마십시오. 공식 문서를 내부에 Mirroring하고,
Version을 고정하고, Index를 만든 뒤, 답변마다 Topic URL, Version, 조회 날짜를 함께
돌려주는 내부 읽기 전용 MCP를 제공하십시오. 공개 Endpoint는 공개 기술 조사에만 씁니다.

## 연결하기

이 문서 옆의 `mcp-profile.json.example`에 위 표의 Server가 그대로 들어 있습니다.
Agent가 읽는 Adapter 설정으로 복사하십시오.

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`; MCP는 Client에서 구성 |

DevExpress 항목 둘을 모두 등록해 둔 것은 의도입니다. `dxdocs`와 `dxdocs24_2`는 DevExpress가
문서화한 Server 이름이고, 둘 다 있어야 Query Parameter를 덧붙이는 것을 기억해 내는 대신
이름으로 고정된 쪽을 가리킬 수 있습니다. 이 Project가 쓰지 않는 Stack의 항목은 지우십시오.
그것은 정상적인 편집이지 기능 축소가 아닙니다. 그리고 폐쇄망에서 어느 하나라도 켜 둔 채로
두기 전에 위 절을 읽으십시오. 거기서는 내부 Mirror가 정답입니다.

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`.
중요한 값은 전송 방식과 URL 둘뿐입니다.

`stdio`만 되는 Client라면:

```json
{
  "mcpServers": {
    "dxdocs": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.devexpress.com/mcp/docs"]
    }
  }
}
```

## 다시 확인하기

위 Schema를 만들어 낸 명령입니다. 그것을 다시 돌려 보고 싶거나 Tool이 바뀌었다고 의심하는
사람을 위해:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

`devexpress_docs_search`와 `devexpress_docs_get_content`라는 이름의 Tool 두 개가, 위에 옮겨
적은 입력 Schema와 함께 나오는 것이 정상입니다. Tool 이름이나 필수 Property나 enum
Member가 바뀌었다면 그것은 사소한 사항이 아니라 Finding입니다. 위 Routing Rule이 특정 Tool을
지목하고 특정 enum 값을 넘기고 있으며, Server가 앞서 나가 버렸다면 둘 다 호출 시점에 조용히
깨지기 때문입니다.

아직 열려 있는 것은 한 단 위입니다. 이 Endpoint에 대한 실제 `tools/call`, 그리고
`?v=24.2`에 대한 같은 검사 둘입니다. 그것을 돌리는 사람은 결과를 날짜와 함께 여기 기록하고,
위 표의 판정은 실제로 실행한 만큼만 올리십시오.

실패를 믿기 전에, 같은 Session에서 정상임이 알려진 Endpoint에 같은 명령을 돌려 보십시오:

```bash
npx -y @modelcontextprotocol/inspector --cli https://learn.microsoft.com/api/mcp \
  --transport http --method tools/list --format json
```

둘 다 실패한다면 문제는 Client이거나 Network입니다. 작성 환경에서 정확히 그 일이 일어났고,
그래서 이 Endpoint가 2026-08-06까지 확인되지 않은 채로 남아 있었습니다.
