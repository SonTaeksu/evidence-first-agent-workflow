# Source Routing — DevExpress WinForms

문서 Source가 둘이고, 그 둘을 가르는 것이 이 문서의 전부입니다. DevExpress 질문은
`dxdocs`로 갑니다. Windows Forms와 .NET 질문은 `microsoft-learn`으로 갑니다. 어느 쪽도 다른
쪽의 질문에 답하지 않으며, 여기서 라우팅을 틀려도 Error는 나지 않습니다 — 대신 다른 Control
Library에 대한 자신만만한 답이 나옵니다.

| Server | Endpoint | 판정 | Tool | 역할 |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **`tools/list` 응답 받음; `tools/call` 없음** (2026-08-06) | 2 | DevExpress 공식 문서, 최신 Release |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **문서에 근거함; 고정된 URL은 시험하지 않음** | 2 | v24.2에 고정한 같은 Server |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** (2026-08-05) | 3 | Windows Forms, C#, .NET, MSBuild — DevExpress가 아닌 모든 것 |

`microsoft-learn`의 판정은
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
기록된 Inspector 실행에서 나온 것입니다. DevExpress 두 행은 그와 다른, 더 약한 판정을
가지며 그 차이가 다음 절의 내용입니다.

## 검증 상태 — 이 표를 믿기 전에 읽을 것

Endpoint에는 이제 도달했고, 그것이 받은 등급은 특정한 등급입니다. `PASS`가 아니며, 그것을
`PASS`로 읽는 것이 이 절이 막으려고 존재하는 실수입니다.

**무엇을 측정했는가.** **2026-08-06**, Owner Machine의 Windows Shell에서
`@modelcontextprotocol/inspector`를 `https://api.devexpress.com/mcp/docs`에 대해
`--transport http --method tools/list --format json`으로 실행했습니다. **자격 증명 없이**
연결되었고, 문서에 적힌 이름 그대로 **Tool 두 개**를 반환했습니다. 아래 *두 Tool*의 Input
Schema는 문서를 읽은 것이 아니라 그 실행의 출력입니다.

**무엇을 측정하지 않았고, 판정이 왜 거기서 멈추는가.**

- **`tools/call`은 실행하지 않았습니다.** `docs/core/mcp-source-verification.md`의 열네 개
  Server가 `PASS`로 기록된 것은 각각이 실제 호출에 답했기 때문입니다. Server 자신의
  `inputSchema`로 인자를 만들고, 질의를 보내고, Error 없이 결과를 받았습니다. 이 Endpoint는
  거기까지 가지 않았습니다. `tools/list`가 확립하는 것은 Server가 거기 있고, Streamable
  HTTP를 쓰며, 자격 증명이 필요 없고, 이 Schema를 가진 이 두 Tool을 선언한다는 것입니다.
  검색이 쓸 만한 Topic을 반환하는지에 대해서는 아무것도 확립하지 않습니다. 이것에 `PASS`
  등급을 빌려 주지 말고, 호출이 응답하기 전까지 `docs/core/mcp-source-verification.md`에
  추가하지 마십시오.
- **`?v=24.2`는 따로 시험하지 않았습니다.** 고정된 URL은 실행하지 않았습니다. 표의 그 행은
  여전히 문서에만 기대고 있으며, 고정되지 않은 URL이 답한다는 사실은 고정된 쪽이 답한다는
  Evidence가 아닙니다.

이전 시도는 작성 환경 안에서 실패했는데, 그곳에서는 이미 `PASS`로 기록된 두 Endpoint —
`https://gitmcp.io/vuejs/docs`와 `https://mcp.deepwiki.com/mcp` — 도 똑같이
`{"code":"unreachable","cause":"invalid onRequestStart method"}`로 실패했습니다. Endpoint가
아니라 환경에 관한 Fact라는 그 해석은 이제 확인되었습니다. 외부 접속이 되는 Machine에서는
같은 Endpoint가 첫 시도에 응답했습니다.

*문서가 말하는 것*에 있는 모든 내용은 **2026-06-16**에 가져온 공식 DevExpress 문서에서
나온 것이며, 2026-08-06 실행이 이후에 확인해 준 부분만 예외입니다. 문서는 여전히 실제로
응답한 호출보다 약한 등급의 Evidence입니다.

### 나머지를 정리하기

두 가지가 아직 열려 있습니다. 둘 다 외부 Network 접속이 되는 Machine에서 명령 하나씩이면
됩니다.

실제 `tools/call`입니다. 이것이 이 Endpoint를 나머지 열네 개와 같은 기준으로 `PASS`로 만들
것입니다:

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/call --tool-name devexpress_docs_search \
  --tool-arg 'technologies=["WindowsForms"]' \
  --tool-arg 'question=How do I hide a GridView column at runtime?' \
  --format json
```

그리고 아직 아무것에도 답한 적 없는 고정된 Endpoint입니다:

```bash
npx -y @modelcontextprotocol/inspector --cli "https://api.devexpress.com/mcp/docs?v=24.2" \
  --transport http --method tools/list --format json
```

어느 쪽 결과든 날짜와 함께 `references/verified-facts.md`에 기록합니다. 아래와 다른 Tool
이름이나 Schema는 사소한 부분이 아니라 Finding입니다 — 이 문서의 Routing 규칙은 특정 Tool을
지목하고 특정 인자를 넘기기 때문입니다.

## 문서가 말하는 것

- **인증 없음.** 이 Endpoint는 자격 증명을 받지 않습니다. *자격 증명 없이 연결된 2026-08-06
  실행으로 확인되었습니다.*
- **Streamable HTTP만.** SSE Transport도, 평범한 GET Interface도 없습니다. Browser에서 URL을
  열면 `405 Method Not Allowed`가 반환되며, 문서는 그것이 결함이 아니라 예상된 응답이라고
  밝히고 있습니다. Browser의 `405`를 장애로 읽지 말고 Health Check로도 쓰지 마십시오 —
  정상 동작하는 Server가 잘못된 Verb에 돌려주는 것입니다.
- **Version 고정은 `?v=`를 쓰며,** **v24.2보다 이전 Release에서는 지원되지 않습니다.**
  `https://api.devexpress.com/mcp/docs?v=24.2`가 문서에 있는 예시입니다. 더 오래된 Release를
  고정할 지원되는 방법이 없으므로, 24.2 이전 Project에서는 문서 Server를 Code에 맞출 수 없고
  모든 Control API 답변을 고정되지 않은 것으로 취급해야 합니다.
- **Tool은 두 개, 오직 두 개입니다.** *이 두 이름을 반환하고 그 외에는 반환하지 않은
  2026-08-06 `tools/list`로 확인되었습니다.*
- **미리 정의된 Prompt가 존재합니다:** `mcp.dxdocs.devexpress_docs_query_workflow`.
- **문서에 적힌 Server 이름:** 최신 Release용 `dxdocs`와 고정용 `dxdocs24_2`. 둘 다
  `mcp-profile.json.example`에 등록되어 있습니다. Project에는 고정된 쪽이 필요하고, 다른
  쪽의 명명 관례를 누구도 추측하게 만들면 안 되기 때문입니다.

## 두 Tool

아래 Schema는 문서를 바꿔 쓴 것이 아니라 2026-08-06 실행의 `tools/list` 출력입니다.

| Tool | 하는 일 | Parameter |
|---|---|---|
| `devexpress_docs_search` | 문서 전체에 대한 Semantic 검색. 상위 다섯 개 일치를 반환하며 **Snippet만** 준다 — Topic 전체에는 두 번째 호출이 필요하다 | `technologies` — array, `minItems: 1`, **required**; 각 항목은 아래 닫힌 enum의 값. `question` — string, **required** |
| `devexpress_docs_get_content` | URL로 도움말 Topic 전체를 내려받는다 | `url` — string, **required**; `devexpress_docs_search` 결과에서 온 것이어야 한다 |

`technologies` — Server 자신의 설명: *"Use specific technology names like 'WindowsForms',
'XtraReports', 'OfficeFileAPI' etc. You must choose from the allowed set."* 허용된 집합은
닫혀 있고, 아래가 전부입니다:

```
Angular, AspNet, AspNetBootstrap, AspNetCore, AspNetMvc, ASPxThemeBuilder,
ASPxThemeDeployer, Blazor, CodedUIExtension, CoreLibraries, Dashboard,
DesignSystem, DevExtremeAspNetMvc, eud, eXpressAppFramework, GeneralInformation,
jQuery, MAUI, OfficeFileAPI, OfficeFileApiJava, React, ReportServer, SkinEditor,
VCL, Vue, WindowsForms, WPF, WpfThemeDesigner, XPO, XpoProfiler, XtraReports
```

`question` — *"Your specific question or search query. Be descriptive and include
relevant keywords about what you're trying to accomplish."*

`url` — *"REQUIRED: This URL must be obtained from a previous call to
`devexpress_docs_search` tool. **Do not construct URLs using your general
knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`"*

### 기록된 정정

이 절에는 전에 Parameter 열을 *의도적으로 비워 두었다*고 적혀 있었습니다. 다른 곳에서
돌아다니는 `technologies`/`question` Schema가 "위에 문서화된 두 Tool과 이름이 맞지 않는
Tool을 서술한다"는 근거, 그리고 같은 Server에 대한 두 서술이 서로 모순되면 어느 쪽도 기록하지
않을 이유가 된다는 근거에서였습니다.

**그 근거는 틀렸고, 그것을 보여 준 것은 측정입니다.** `technologies`/`question` Schema는
`devexpress_docs_search` 자신의 Input Schema이며, Server가 바로 그 Tool 이름으로 반환한
것입니다. 모순된 것은 아무것도 없었습니다. 공식 문서가 Input Schema를 싣지 않을 뿐인데,
문서에 Schema가 없다는 사실을 문서가 그 Schema와 어긋난다는 뜻으로 읽은 것입니다.

이 교훈은 지우지 않고 여기 남겨 둡니다. **"문서에 없다"는 "문서가 반박한다"와 같지
않습니다.** 앞의 것은 공백이고 측정으로 해결됩니다. 뒤의 것은 충돌이고 판정이 필요합니다.
앞의 것을 뒤의 것으로 취급한 탓에 처음부터 구할 수 있던 Schema를 붙들어 두었고, Agent에게
인자 이름이 필요한 자리에 `⟨확인 필요⟩`를 남겨 두었습니다.

## Routing 규칙

- DevExpress Control, Property, Event, Service, Namespace에 관한 질문은 `dxdocs`로 갑니다.
  언제나 그렇습니다. "뻔한" 것에 대한 예외는 없습니다 — 이만큼 큰 Control Library야말로
  기억이 가장 믿을 수 없는 영역입니다.
- Windows Forms, C#, .NET, MSBuild, 구성 Schema에 관한 질문은 `microsoft-learn`으로 갑니다.
- **DevExpress API 질문에 `microsoft-learn`으로 절대 답하지 않습니다.** Microsoft Learn은
  서드파티 Control Library를 문서화하지 않습니다. `GridControl`에 대해 물으면 `DataGridView`를
  찾아 그것에 대해 답할 것이고, 그것은 Member가 다른 별개의 Type이며 그렇다고 알려 줄 Error
  Message도 없습니다.
- **DevExpress API 질문에 기억으로 절대 답하지 않습니다.** Property 이름도, Enumeration
  Member도, Namespace도, 어느 Release가 그것을 도입했는지도 마찬가지입니다.
- **v24.2 Project에서는 `dxdocs24_2`를 씁니다.** 고정되지 않은 `dxdocs`는 최신 Release에서
  답하며, v24.2 이후에 추가된 Member를 마치 사용 가능한 것처럼 서술합니다. 그 실패는 잘해야
  Compile 시점까지, 최악의 경우 Runtime까지 조용합니다.
- DevExpress 질문을 일반 Package 문서 Server로 라우팅하지도 않습니다. 문서는 제품 자신의
  것이며, Repository Mirror는 그것이 아닙니다.

### Server 자신의 두 규칙

이것은 이 Kit의 취향이 아닙니다. 둘 다 Server가 반환하는 Tool 설명에 적혀 있으므로 Server
자신의 Contract입니다:

- **모든 `devexpress_docs_get_content`보다 `devexpress_docs_search`를 먼저 호출합니다.**
  검색 설명이 그렇게 말 그대로 적고 있고, 이유는 Schema에 있습니다. 검색은 Snippet과
  발췌만 반환하므로 Topic 전체는 언제나 두 번째 호출을 요구합니다. 같은 요청 사슬 안에서
  검색이 선행하지 않은 `get_content`는 Contract 밖입니다.
- **문서 URL을 기억으로 조립하지 않습니다.** `url` Parameter 자신의 설명이 *do not construct
  URLs using your general knowledge*라고 말합니다 — 그 값은 `devexpress_docs_search` 결과가
  반환한 것이어야 합니다. 기억으로 조립한 그럴듯한
  `https://docs.devexpress.com/WindowsForms/…`가 바로 이 규칙이 지목하는 실패이고, 틀렸지만
  형식은 맞는 URL은 Routing Error가 아니라 Fetch 실패로 나타납니다.

### 이 Stack의 `technologies` 값

`technologies`는 닫힌 enum이고, Agent는 산문체의 Platform 이름이 아니라 enum 값을 넘겨야
합니다. `"DevExpress WinForms"`, `"WinForms"`, `"Windows Forms"`는 그 집합의 구성원이
아니며, 그중 하나를 넘기면 빈 결과 집합이 아니라 **Schema Validation Error**가 납니다.
답에서 조용히가 아니라 호출에서 요란하게 실패합니다 — 아무도 또 다른 지어낸 철자로
재시도하지 않는다면, 그쪽이 좋은 경우입니다.

- DevExpress WinForms 질문 — `WindowsForms`.
- 이 Stack의 자료가 Reporting에 닿는 곳 — `XtraReports`.
- 공유 Base Type, 공통 Enumeration, 제품을 가로지르는 기반 — `CoreLibraries`.

둘 이상을 넘길 수 있습니다. 이 Parameter는 `minItems: 1`인 array입니다. 인쇄나 Export
경로로 끝나는 Grid 질문은 `["WindowsForms", "XtraReports"]`가 타당합니다.

구체적인 호출:

```json
{
  "name": "devexpress_docs_search",
  "arguments": {
    "technologies": ["WindowsForms"],
    "question": "How do I hide a GridView column at runtime without removing it from the columns collection?"
  }
}
```

그리고 그다음에야, 그 결과에서 가져온 URL로:

```json
{
  "name": "devexpress_docs_get_content",
  "arguments": { "url": "https://docs.devexpress.com/CoreLibraries/405204" }
}
```

## 우선순위

1. 이 Project의 Code, Project File, Package 또는 Lock File.
2. Exit Code를 갖춘 결정론적 Build 및 Test Evidence.
3. `dxdocs24_2` — 또는 Project가 정말로 최신 Release일 때는 `dxdocs`.
4. 그 아래의 Windows Forms 및 .NET Layer에는 `microsoft-learn`.
5. Version 사이에 바뀐 동작에는 공식 DevExpress Release Note.
6. 모델 기억 — Version에 민감한 Fact에는 절대 쓰지 않고, DevExpress Member 이름에도 절대
   쓰지 않습니다.

## 애초에 호출하게 만들기

Server를 등록한다고 모델이 그것을 쓰지는 않습니다. 다음 규칙은 여기만이 아니라 Project의
Agent 지침에 들어가야 합니다.

- API, Version 동작, 설정에 관한 질문을 학습 지식만으로 답하지 않는다;
- 먼저 검색하고 그다음에 Topic 자체를 가져온다 — `devexpress_docs_search`는 상위 다섯 개
  일치를 Snippet으로 반환하는데 그것은 답이 아니라 후보 목록이고, 대목을 실제로 가져오는
  것은 `devexpress_docs_get_content`이다. 이 순서는 Server 자신이 밝히고 있다. 위의
  *Server 자신의 두 규칙*을 참고한다;
- 반환된 Topic의 제목이 아니라 본문을 읽는다. 검색 결과는 후보다;
- Topic URL과 답이 나온 Version을 밝힌다;
- 검색으로 아무것도 찾지 못했으면 그렇다고 말한다. 그 빈자리를 기억으로 채우지 않는다.

## Version에 민감한 조회

기억하지 말고 항상 조회합니다:

- 어떤 Release가 Member를 도입했거나 바꿨는지;
- Property, Enumeration Member, Namespace의 정확한 철자;
- 어떤 설정이 Control 소속인지 그 View 소속인지;
- 기본값. 조용히 바뀌었을 가능성이 가장 큰 것입니다.

## Fallback

Project의 DevExpress Version이 Source가 서술하는 Version과 다르면 **멈추고 불일치를
보고합니다**. 문서에 우연히 보이는 Version에 맞춰 구현하지 않습니다. 해결되지 않은 항목은
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 밖으로 무엇이든 내보내기 전에

`api.devexpress.com`과 `learn.microsoft.com`은 **공개된 서드파티 Endpoint**입니다. 호출 한
번에 질의, Agent가 조립한 Tool 인자, 그리고 함께 실린 Context가 전송됩니다. 거기에는 비공개
Source, 고객 데이터, 내부 Hostname, 자격 증명, 공개되지 않은 Repository 이름, 가공되지 않은
운영 Log가 실릴 수 있습니다. "왜 *우리* 정산 화면의 주문 Grid가 예외를 던지는가"라고 표현된
질문은 Grid에 대한 질문보다 더 많은 것을 실어 나릅니다.

폐쇄망에서는 이것들을 운영 의존성으로 삼지 않습니다. 문서를 내부에 Mirroring하고, Release를
고정하고, 색인한 다음, 모든 답에 Topic, Version, 조회 날짜를 함께 반환하는 내부 읽기 전용
MCP를 제공합니다. 공개 Endpoint는 공개 기술 조사에만 씁니다.

## 연결

이 문서 옆의 `mcp-profile.json.example`에 위 표의 Server가 그대로 들어 있습니다. Agent가
읽는 Adapter 설정으로 복사합니다:

| Adapter | File |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | Rule은 `.clinerules/`; MCP는 Client에서 설정 |

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. 중요한
값은 Transport와 URL 두 가지이고, 여기서 Transport는 선택 사항이 아닙니다: **Streamable
HTTP**. SSE로 구성된 Client는 연결되지 않습니다.

이 Project에 필요 없는 Endpoint는 지웁니다 — Server를 적게 등록할수록 Tool Routing Error와
불필요한 Tool Schema Context가 줄고, v24.2 Project에는 DevExpress 항목 둘 다가 아니라
`dxdocs24_2`가 필요합니다. 그리고 폐쇄망에서 어느 하나라도 켜 둔 채로 두기 전에 위 절을
읽으십시오. 거기서 옳은 답은 이 Endpoint들이 아니라 내부 Mirror입니다.

`stdio`만 쓰는 Client라면:

```json
{
  "mcpServers": {
    "dxdocs24_2": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.devexpress.com/mcp/docs?v=24.2"]
    }
  }
}
```

`⟨확인 필요: mcp-remote Bridge가 이 Endpoint에 도달하는지 — Inspector를 쓰지 못한 것과 같은
이유로 여기서는 시도하지 않았다⟩`

## 재검사

DevExpress Release가 바뀔 때, Project가 다른 Version으로 옮길 때, 그리고 Server가 다르게
답하기 시작할 때마다 위의 `tools/list` 명령을 다시 실행합니다. 바뀐 Tool 이름은 사소한
부분이 아니라 Finding입니다. 위 Routing 규칙이 특정 Tool 이름을 지목하고 있기 때문입니다.
