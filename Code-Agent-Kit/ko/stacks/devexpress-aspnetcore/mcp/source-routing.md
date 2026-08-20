# Source Routing — DevExpress for ASP.NET Core

Source는 둘이며, 그 둘의 구분이 이 문서의 요점 전부입니다. DevExpress 질문은 `dxdocs`로
갑니다. ASP.NET Core, EF Core, .NET 질문은 `microsoft-learn`으로 갑니다. 어느 쪽도 다른
쪽의 질문에 답하지 않고, 어느 쪽도 기억을 꺼 두는 일의 대체물이 아닙니다.

| Server | Endpoint | 판정 | Tool | 역할 |
|---|---|---|---:|---|
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | **`tools/list` 측정됨, 2026-08-06 — 호출 없음** | 2 | DevExpress 문서, 최신 |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | **문서화됨, 별도로 검증되지 않음** | 2 | v24.2에 고정된 동일 Server |
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | ASP.NET Core, C#, .NET, EF Core |

`microsoft-learn`은 2026-08-05에 MCP Inspector로 확인되어
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)에
기록된 Endpoint 중 하나입니다. DevExpress 행들은 다르고 더 약한 등급을 가집니다. 이어지는
내용이 그것이 정확히 무엇을 뜻하는지 말합니다.

## DevExpress Server의 검증 상태

**Endpoint는 2026-08-06에 도달했습니다.** MCP Inspector, CLI, Owner 머신의 Windows Shell
에서 `https://api.devexpress.com/mcp/docs`를 상대로
`--transport http --method tools/list --format json`으로 실행했습니다. 자격 증명 없이
연결되어 응답했습니다. Tool은 둘이고, 문서가 제시하는 것과 정확히 같은 이름입니다.
`devexpress_docs_search`와 `devexpress_docs_get_content`. 그 Input Schema는 읽어 온 것이
아니라 그 출력에서 가져와 아래에 기록되어 있습니다.

**그것은 `PASS`가 아니며, `PASS`로 써서는 안 됩니다.**
[`docs/core/mcp-source-verification.md`](../../../docs/core/mcp-source-verification.md)의
14개 Server는 실제 `tools/call`이 Error 없이 응답했기 때문에 `PASS`로 기록되어 있습니다.
여기서는 `tools/call`을 실행하지 않았습니다. 확립된 것은 연결, 인증 없음, Tool 이름, Tool
Schema이며 — Server가 *질의*에 답한다는 것은 아직 측정되지 않았습니다. 다른 Server의 등급을
이것에 빌려 오는 일은 이 Kit이 막으려고 존재하는 바로 그 대체 행위일 것입니다.

`?v=24.2`는 **별도로 검증되지 않았습니다.** 고정된 행에 관한 모든 것은 여전히 문서일
뿐이며, 위의 측정은 그 Query Parameter가 존중되는지에 대해 아무것도 말하지 않습니다.

앞선 Inspector 시도는 작성 환경에서 다음과 함께 실패했습니다.

```json
{"code":"unreachable","cause":"invalid onRequestStart method"}
```

당시 그것은 DevExpress에 관한 사실이 아니라 환경에 관한 사실로 읽혔습니다. 이미 **PASS**로
기록된 두 Endpoint — `https://gitmcp.io/vuejs/docs`와 `https://mcp.deepwiki.com/mcp` — 가
같은 시도에서 똑같이 실패했기 때문입니다. 다른 머신에서 수행한 2026-08-06 실행이 그 읽기를
확인해 줍니다.

## `dxdocs` — 도달했고, 나열했고, 아직 호출하지 않음

Endpoint: `https://api.devexpress.com/mcp/docs`

- **인증 없음.** 문서는 자격 증명을 서술하지 않습니다.
- **Streamable HTTP만.** 브라우저에서 URL을 열면 `405 Method Not Allowed`가 돌아오고,
  문서는 이것이 결함이 아니라 예상된 것이라고 밝힙니다. 그 응답을 Server가 죽은 것으로
  다루지 않고, 브라우저 방문을 확인으로 다루지도 않습니다 — 그것은 어느 쪽으로도 아무것도
  확립하지 않습니다.
- **Tool은 둘이고 둘뿐**이며, `tools/list` 실행으로 문서가 제시하는 이름과 함께
  확인되었습니다.
  - `devexpress_docs_search` — 의미 검색. 문서는 상위 다섯 개 결과라고 말하고, Tool 자신의
    설명은 그 결과가 전체 내용이 아니라 Snippet이라고 말합니다.
  - `devexpress_docs_get_content` — URL로 완전한 도움말 항목을 내려받습니다.
- **미리 정의된 Prompt가 있습니다:** `mcp.dxdocs.devexpress_docs_query_workflow`.

용도: 모든 DevExpress 질문 — Component, tag helper, DevExtreme Widget, Reporting, Service
등록, 그리고 DevExpress Type이나 Member 이름이 들어간 모든 것.

### 측정된 Schema

2026-08-06의 `tools/list` 출력에서 가져왔습니다.

**`devexpress_docs_search`** — "Search DevExpress documentation for a given
technology and a question. If you want to search for multiple technologies, pass
them as a list. This tool returns only snippets/excerpts; full content requires a
follow-up `devexpress_docs_get_content` call on a chosen URL. ALWAYS call
`devexpress_docs_search` before ANY `devexpress_docs_get_content` call in a user
request chain."

두 Property 모두 **필수**입니다.

| Property | Type | 제약 |
|---|---|---|
| `technologies` | array | `minItems: 1`; 각 항목은 아래에 나열된 **닫힌 enum** |
| `question` | string | "Your specific question or search query. Be descriptive and include relevant keywords about what you're trying to accomplish." |

enum 자체의 설명: "Use specific technology names like 'WindowsForms',
'XtraReports', 'OfficeFileAPI' etc. You must choose from the allowed set." 허용된 집합
전체는 다음과 같습니다.

```text
Angular            AspNet              AspNetBootstrap    AspNetCore
AspNetMvc          ASPxThemeBuilder    ASPxThemeDeployer  Blazor
CodedUIExtension   CoreLibraries       Dashboard          DesignSystem
DevExtremeAspNetMvc  eud               eXpressAppFramework  GeneralInformation
jQuery             MAUI                OfficeFileAPI      OfficeFileApiJava
React              ReportServer        SkinEditor         VCL
Vue                WindowsForms        WPF                WpfThemeDesigner
XPO                XpoProfiler         XtraReports
```

**`devexpress_docs_get_content`** — "Get full document content by URL from
DevExpress documentation. PREREQUISITE: ALWAYS call `devexpress_docs_search`
before using this tool to get valid URLs. The URL parameter must be obtained from
the results of the `devexpress_docs_search` tool."

필수: `url`, string — "REQUIRED: This URL must be obtained from a previous
call to `devexpress_docs_search` tool. **Do not construct URLs using your general
knowledge.** Example: `https://docs.devexpress.com/CoreLibraries/405204`"

### 지우지 않고 남겨 둔 정정

이 문서는 이전에 `technologies`/`question` Schema를 지목하고 그것을 기각했습니다. "문서화된
것과 다른 이름의 Tool을 서술하므로 이 Server에 대한 서술이 아니다"라는 근거였습니다.
**그것은 틀렸습니다.** 측정된 출력은 그 Schema가 `devexpress_docs_search` 자신의 것임을
보여 줍니다.

그 오류를 만들어 낸 원인이 오류 자체보다 더 값집니다. 공식 문서는 두 Tool의 이름을 밝히지만
그 Input Schema를 공개하지 않는데, 공개된 Schema의 부재가 문서가 떠도는 Schema를
*반박한다*는 뜻으로 읽혔습니다. 문서는 그런 일을 전혀 하지 않았습니다. **"문서에 없음"은
"문서가 반박함"이 아닙니다.** 앞의 것은 공백이고, 공백은 측정으로 메웁니다. 뒤의 것은
충돌이고, 충돌은 기각의 근거입니다. 앞의 것을 뒤의 것으로 다루면 참인 사실을 거짓인 사실과
똑같은 확신으로 버리게 됩니다.

원래의 신중함은 한 가지에 대해서는 여전히 옳았고, 그래서 위 Schema에는 날짜가 붙어 있으며
다른 곳에서 찾은 페이지가 아니라 실행에 귀속되어 있습니다.

### 이 Stack이 넘기는 `technologies` 값

이 부분이 답이 올바른 말뭉치에서 오는지를 결정하는 Schema의 부분이고, 가장 틀리기 쉬운
부분입니다. 틀렸지만 유효한 값은 Error가 아니라 결과를 돌려주기 때문입니다.

| 질문의 주제 | 넘길 값 |
|---|---|
| ASP.NET Core용 DevExpress Component, tag helper, Service 등록 | `AspNetCore` |
| DevExpress Reporting — Viewer, Designer, Report 정의, Storage | `XtraReports` |
| DevExtreme 기반 MVC Wrapper | `DevExtremeAspNetMvc` |
| 고전 ASP.NET MVC 5 | `AspNetMvc` |

**Reporting은 별개의 enum 값입니다.** `XtraReports`는 `AspNetCore` 안에 있지 않습니다.
`AspNetCore` 하나로 라우팅된 Reporting 질문은 Component 말뭉치를 검색해 Component 항목을
돌려줍니다 — 그럴듯하고, 브랜드에 맞고, 다른 것에 관한 것입니다. 질문이 ASP.NET Core에
Hosting되는 Reporting에 관한 것일 때는 두 값을 함께 넘깁니다. 이 Stack에서는 대부분이
그렇습니다.

**어느 MVC 값이 적용되는지는 추측이 아니라 Project의 사실입니다.**
`DevExtremeAspNetMvc`와 `AspNetMvc`는 서로 다른 제품의 서로 다른 말뭉치이며, 값을 고르기
전에 Project가 어느 것을 쓰는지 확립해야 합니다. 그것이 `capability-detection.md`의
`ui-component-layer` Capability이고, 무엇보다 이 이유로 차단합니다.

`Blazor`는 허용 집합에 있습니다. 그것은 **이 Stack의 범위 밖**입니다 — Blazor 질문은 이
Profile이 아니라 다른 Profile입니다.

enum이 닫혀 있다는 데서 따라 나오는 결과가 두 가지 더 있습니다.

- **산문 형태의 플랫폼 이름이 아니라 enum 값을 넘깁니다.** "ASP.NET Core MVC with
  DevExpress"는 집합의 원소가 아니고, `AspNetCore`가 원소입니다. Tool은 식별자를 받고, 그
  식별자가 곧 라우팅 결정입니다.
- **집합 밖의 값은 빈 결과가 아니라 Schema Error입니다.** `aspnetcore`, `ASP.NET Core`,
  `Reporting`, `DevExpressReporting`은 아무것도 돌려주지 않는 것이 아니라 — 호출이 Schema에
  대해 거부됩니다. 그런 실패는 문서에 그 항목이 없다는 뜻이 아니라 인자가 틀렸다는 뜻으로
  읽습니다.

Component 질문:

```json
{
  "technologies": ["AspNetCore"],
  "question": "register the DevExpress GridView tag helper in Startup"
}
```

두 값을 함께 실은 Reporting 질문:

```json
{
  "technologies": ["AspNetCore", "XtraReports"],
  "question": "host the Web Document Viewer in an ASP.NET Core application and register its services"
}
```

## `dxdocs24_2` — 고정된 Server

Endpoint: `https://api.devexpress.com/mcp/docs?v=24.2`

Version 고정은 `?v=` Query Parameter를 사용하며,
`https://api.devexpress.com/mcp/docs?v=24.2`가 문서화된 예시입니다. Server에 관한 나머지 —
Transport, 인증, 두 Tool — 는 모두 같은 Server입니다. Parameter는 어느 문서 Version에서
답할지를 고릅니다.

**v24.2 Project에서는 최신 Endpoint 대신 `dxdocs24_2`를 사용합니다.** 고정이 존재하는 이유
자체가, 최신 문서는 이 Project가 실행하고 있지 않은 제품을 서술하고 거기서 나온 답은 올바른
답과 똑같아 보이기 때문입니다.

> **주의.** 고정은 **v24.2보다 이르게는** 지원되지 않습니다. v16.x나 그 밖의 24.2 이전
> 릴리스를 고정할 지원 방법은 없습니다. 그런 Project에서 유일하게 얻을 수 있는 답은 현행
> 문서에서 나온 것이고 그것은 이 Project의 Version이 아닙니다 — 그렇게 얻은 사실은 답으로
> 다루는 대신 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

두 Server를 모두 등록합니다. 최신 Endpoint는 Project가 옮겨 갈 수도 있는 Version에 대해
읽는 데 계속 유용하고, 고정된 쪽은 구현이 그것을 대상으로 작성되는 것입니다.

## `microsoft-learn`

Endpoint: `https://learn.microsoft.com/api/mcp`  (Streamable HTTP)

용도: ASP.NET Core Hosting, Routing, MVC와 Razor Pages, Dependency Injection,
Configuration, 정적 파일, Logging, Authentication과 Authorization, Test, C#과 .NET, 그리고
Entity Framework Core.

## 이 Source가 아닌 것

- **DevExpress API 질문에 `microsoft-learn`으로 답하지 않습니다.** 그것은 답할 것입니다 —
  그 아래 Framework에 대해 유창하게 — 그리고 그 답은 질문을 다룬 것처럼 읽힐 것입니다.
  질문을 잘못된 Server로 라우팅하는 것은 Error를 내지 않습니다. 다른 기술에 관한 자신 있는
  답을 내놓고, 그편이 더 나쁩니다.
- **DevExpress API 질문에 기억으로 답하지 않습니다.** Component 이름, Property 이름, tag
  helper 이름, 등록 호출은 Version에 민감하고, 지어내면 전부 그럴듯해 보입니다.
- 평범한 ASP.NET Core 질문에 `dxdocs`로 답하지 않습니다. 그 말뭉치는 DevExpress 문서이며,
  거기서 Framework 질문은 Framework를 언급하는 DevExpress 항목을 돌려줍니다.
- Server-side Control에 대한 답을 DevExtreme의 Client-side Widget을 쓰는 Project로 가져가지
  않고, 그 반대도 하지 않습니다.
- WinForms나 WPF Reporting 답을 이 Web Host로 가져오지 않습니다. 이 Stack은 Report의 Web
  Hosting만 다룹니다.

## 우선순위

1. 이 Project의 Code, Project File, 해석된 Package Version.
2. Exit Code를 갖춘 결정론적 Build와 Test Evidence.
3. DevExpress에 대해서는 `dxdocs` — v24.2 Project에서는 고정된 것.
4. ASP.NET Core, EF Core, .NET에 대해서는 `microsoft-learn`.
5. Version 사이에 바뀐 동작에 대해서는 공식 릴리스 노트.
6. 모델 기억 — Version에 민감한 사실에는 절대 쓰지 않습니다.

## 실제로 호출하기

Server를 등록한다고 모델이 그것을 사용하지는 않습니다. 여기뿐 아니라 Project의 Agent
지시문에 들어가야 할 규칙:

- API, Version 동작, 설정에 관한 질문에 학습 지식만으로 답하지 않습니다;
- **모든 `devexpress_docs_get_content` 호출 전에 항상 `devexpress_docs_search`를
  호출합니다.** 이것은 이 Kit의 선호가 아니라 두 Tool 설명 모두에 명시된 Server 자신의
  규칙입니다. 검색은 Snippet을 돌려주고, 전체 내용은 검색이 고른 URL에 대한 후속 호출을
  필요로 합니다. 다섯 개의 Snippet은 답이 아니라 후보 목록입니다;
- **문서 URL을 기억으로 지어내지 않습니다.** `url` 인자는 검색 결과에서 와야 합니다 —
  "Do not construct URLs using your general knowledge", 역시 Server 자신의 표현입니다.
  지어낸 `docs.devexpress.com` URL은 지어낸 Property 이름과 같은 실패이며, 다른 것에 관한
  실제 페이지로 해석될 수 있다는 성질까지 더해집니다;
- 질문이 실제로 속하는 `technologies` enum 값을 넘기고, Reporting에 관한 모든 것에는
  `AspNetCore`와 함께 `XtraReports`를 넘깁니다;
- 어느 Server가 답했는지, 그리고 도움말 항목 URL을 밝힙니다. URL이 주장을 다시 확인
  가능하게 만들고, 나중에 읽는 사람에게 필요한 것입니다;
- 문서의 기본 Version이 이 Project의 설치 Version과 일치한다고 절대 가정하지 않습니다;
- 검색이 아무것도 찾지 못했으면 그렇다고 말합니다. 그 공백을 기억으로 메우지 않습니다.

## Version에 민감한 조회

기억하지 말고 항상 조회할 것:

- 이 Project의 Version에 그 Component나 Member가 존재하기는 하는지;
- Property, tag helper, 등록 호출의 정확한 철자;
- 기본값. 조용히 바뀌었을 가능성이 가장 큰 것입니다;
- 문서화된 Sample이 두 Component 제품군 중 어느 쪽에 속하는지.

## Fallback

Project의 Version이 Source가 서술하는 Version과 어긋나면 **멈추고 그 불일치를 보고합니다.**
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 무엇이든 밖으로 보내기 전에

이것들은 **공개된 서드파티 Endpoint**입니다. 호출은 질의, Agent가 조립한 Tool 인자, 그리고
그것이 포함시킨 Context를 함께 보냅니다. 거기에는 비공개 Source, 고객 Data, 내부 Hostname,
자격 증명, 공개되지 않은 Repository 이름, 원시 운영 Log가 실릴 수 있습니다.

이 Stack에는 특별히 짚어 둘 것이 두 가지 있습니다. 검색창에 붙여 넣기 가장 쉬운 것들이기
때문입니다. **DevExpress 라이선스 키 또는 Feed 자격 증명**, 그리고 흔히 실제 Schema의 연결
정보와 열 이름을 담고 있는 **Report 정의**입니다. 어느 쪽도 질의에 들어가서는 안 됩니다.

폐쇄망에서는 이것들을 운영 의존성으로 삼지 않습니다. 문서를 내부에 Mirror하고, Index를
만들고, 모든 답과 함께 항목·Version·조회 날짜를 돌려주는 내부 읽기 전용 MCP를 제공합니다.
공개 Endpoint는 공개 기술 조사에만 사용합니다.

## 연결하기

이 문서 옆의 `mcp-profile.json.example`이 표에 있는 Server를 그대로 담고 있습니다. Agent가
읽는 Adapter 설정으로 복사합니다.

| Adapter | 파일 |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo | `.roo/mcp.json` |
| Cline | 규칙은 `.clinerules/`; MCP는 Client에서 설정 |

Client마다 Field 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`, `httpUrl`. 중요한
값은 Transport와 URL 둘입니다.

Project가 실제로 쓰는 Stack만 등록하면 Tool 라우팅 오류와 불필요한 Tool Schema Context가
줄어드므로, 이 Project가 쓰지 않는 Stack의 항목은 지웁니다 — 그것은 격하가 아니라 정상적인
편집입니다.

`stdio`만 지원하는 Client의 경우:

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

## 무엇이 실행되었고, 무엇이 아직 열려 있는가

다음이 2026-08-06에 실행된 명령이며, 위 행이 기록하는 것입니다.

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/list --format json
```

그것이 해결하지 못한 것이 두 가지입니다. 전혀 검증되지 않은 고정 Server:

```bash
npx -y @modelcontextprotocol/inspector --cli "https://api.devexpress.com/mcp/docs?v=24.2" \
  --transport http --method tools/list --format json
```

그리고 `PASS`와 "연결되었다"를 가르는 실제 호출. 인자는 더 이상 Unknown이 아니며, 측정된
Schema가 그것을 채워 줍니다.

```bash
npx -y @modelcontextprotocol/inspector --cli https://api.devexpress.com/mcp/docs \
  --transport http --method tools/call --tool-name devexpress_docs_search \
  --tool-arg 'technologies=["AspNetCore","XtraReports"]' \
  --tool-arg "question=host the Web Document Viewer in an ASP.NET Core application" \
  --format json
```

다음 순서로 확인합니다. Exit Code, 응답이 Parsing되었는지, Tool 개수, 문서화된 두 Tool
이름이 있는지, 그다음 호출의 Exit Code, 그다음 원시 출력. 바뀐 Tool 이름은 사소한 사항이
아니라 발견 사항입니다. 위 라우팅 규칙이 특정 Tool을 지목하고 있기 때문입니다. 바뀐 enum도
마찬가지입니다 — 이 문서의 값은 상수가 아니라 날짜가 붙은 측정입니다.

결과는 이미 거기 있는 14개 Endpoint와 같은 형태로 `docs/core/mcp-source-verification.md`에
기록합니다. 실패도 포함합니다. 실패는 부재보다 더 유용합니다.
