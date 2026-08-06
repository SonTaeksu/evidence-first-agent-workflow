# MCP 출처 검증

스택 프로파일이 어느 문서 서버로 라우팅하는지, 그것을 어떻게 확인했는지, 그리고
더 중요한 것 — **무엇을 확인하지 못했는지**.

- **검증일:** 2026-08-05, 22:05:08 – 22:09:30 KST
- **방법:** `@modelcontextprotocol/inspector`, CLI
- **범위:** 원격 엔드포인트, 무인증. 연결 · `tools/list` · 실제 `tools/call`
- **결과:** 16건 검사 — 15 `PASS`, 1 `PARTIAL`, 연결 실패 0, 인증 필요 0

## 이 문서가 있는 이유

아무도 연결해 본 적 없는 서버의 설정 항목은 지어낸 것과 구별되지 않습니다. 둘 다
지식처럼 보입니다. 그래서 스택 프로파일이 참조하는 모든 엔드포인트를 실제 호출
결과와 함께 여기 적고, **이름만 적히고 시험되지 않은** 서버는 따로 분리해 그렇게
표시합니다.

## "검증됨"의 정확한 의미

검사기가 연결하고, 도구 목록을 요청하고, 각 도구의 `inputSchema`를 읽어 인자를
만들고, 실제 질의로 search 또는 question 도구를 호출했습니다. `PASS`는 그 호출이
오류 없이 돌아왔다는 뜻입니다.

**답이 옳았다는 뜻은 아닙니다.** 내일도 서버가 살아있다는 뜻도 아니고, 저장소의
기본 브랜치가 어떤 프로젝트의 설치 버전과 같다는 뜻도 아닙니다. 그것들은 별개의
주장이고 어느 것도 시험되지 않았습니다.

## 검증된 서버

| 서버 | 엔드포인트 | 판정 | 도구 | 라우팅하는 스택 |
|---|---|---:|---:|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | **PASS** | 3 | csharp-wpf, csharp-wcf, csharp-asmx |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | **PASS** | 4 | csharp-wpf |
| `wcf-docs` | `https://gitmcp.io/dotnet/docs` | **PASS** | 4 | csharp-wcf |
| `asmx-docs` | `https://gitmcp.io/dotnet/AspNetDocs` | **PASS** | 4 | csharp-asmx |
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | **PASS** | 4 | vue |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | **PARTIAL** | 5 | vue (선택) |
| `nextjs-docs` | `https://gitmcp.io/vercel/next.js` | **PASS** | 4 | nextjs |
| `nodejs-docs` | `https://gitmcp.io/nodejs/node` | **PASS** | 4 | nodejs |
| `go-docs` | `https://gitmcp.io/golang/go` | **PASS** | 4 | go |
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | **PASS** | 4 | go-htmx |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | **PASS** | 3 | go-htmx |
| `rust-book` | `https://gitmcp.io/rust-lang/book` | **PASS** | 4 | rust |
| `rust-reference` | `https://gitmcp.io/rust-lang/reference` | **PASS** | 4 | rust |
| `elixir-docs` | `https://gitmcp.io/elixir-lang/elixir` | **PASS** | 4 | elixir |

`context7`은 킷 루트에 설정돼 있고 이번 실행 대상이 아닙니다. 이전부터 있었고
`check-agent-config`가 요구합니다.

### 유일한 PARTIAL

`https://mcp.vue-mcp.org/mcp`는 무인증 연결과 도구 5개 목록까지 성공했습니다.
`vue_docs_search` 호출이 `isError:true`를 반환했습니다. 실패는 전송이나 인증이
아니라 도구 내부이고, 요약에 서버 측 상세는 담기지 않았습니다.

따라서 `vue` 스택에서 **선택**이고, 통과한 `gitmcp.io/vuejs/docs`가 기본입니다.
의존하지 말아야 할 이유가 둘 더 있습니다 — 라이선스가 **FSL-1.1-ALv2**로 OSI
승인이 아니고, 단일 호스팅 엔드포인트 뒤에 유지관리자가 1인입니다.

## 전송 방식: Streamable HTTP, 취향이 아니라

같은 검사기의 첫 실행은 SSE를 썼고 모든 GitMCP 엔드포인트가 이렇게 답했습니다.

```text
SSE error: Non-200 status code (405)
```

Streamable HTTP로 바꾸자 전부 통과했습니다. GitMCP 클라이언트 예시 일부는 아직
SSE를 보여주므로 `http`를 우선하고, 그것을 못 하는 클라이언트에는 `mcp-remote`
브리지를 씁니다.

## 읽어서가 아니라 확인해서 나온 것 둘

### GitMCP의 랜딩 페이지는 아무것도 증명하지 않는다

`https://gitmcp.io/{owner}/{repo}`는 **존재하지 않는 저장소에도** 저장소 이름을
호명하고 클라이언트 설정 예시까지 담은 자신만만한 페이지를 줍니다. 실측:

```text
https://gitmcp.io/thisorgdoesnotexist99/norepohere99
  -> "GitMCP Documentation Server for thisorgdoesnotexist99/norepohere99"
```

페이지는 URL 경로만으로 생성됩니다. 브라우저로 열어보는 것은 아무것도
확립하지 않습니다. GitMCP 엔드포인트가 유의미한지 확인하려면 **저장소**를
`github.com`에서 보고(실재하면 페이지, 없으면 빈 응답) **서버**는 Inspector로
확인해야 합니다.

### 두 스택이 도구 이름을 공유한다 — 그리고 처음에 너무 강하게 적었다

GitMCP는 저장소 이름에서 도구 이름을 만듭니다. `dotnet/docs`와 `vuejs/docs`는
마지막 조각이 같아 둘 다 이것을 노출합니다.

```text
fetch_docs_documentation
search_docs_documentation
search_docs_code
```

처음에는 이것을 "둘을 함께 등록하면 안 되는 충돌"로 적었습니다. **그건
틀렸고**, 그 정정을 조용히 지우기보다 남겨 두는 편이 낫습니다.

대부분의 클라이언트는 도구를 서버로 한정합니다. Claude Code는
`mcp__<서버>__<도구>` 형태로 제시하므로
`mcp__wcf-docs__search_docs_documentation`과
`mcp__vue-docs__search_docs_documentation`은 서로 다른 식별자이고 충돌하지
않습니다. 특정 클라이언트가 이름을 평탄화하는지는 그 클라이언트의 사실이고
시험되지 않았습니다.

어떤 클라이언트에서든 남는 것은 더 약하지만 실재합니다 — 모델이 둘 중에서 고를
때, 기본 이름이 동일하고 목적이 "어느 저장소를 검색하는가"로만 다른 도구 둘을
봅니다. 각 도구의 *설명*이 저장소를 명시하는지는 실행에 기록되지 않았으므로,
모델이 얼마나 쉽게 구분하는지는 괜찮은 게 아니라 **모릅니다**.

정리하면 금지가 아니라 주의이고, 값싼 귀결이 둘입니다. 서버 이름을 구별되게
서술적으로 유지할 것 — 맨 `docs`가 아니라 `wcf-docs`, `vue-docs` — 이름공간을
분리하는 클라이언트에서는 그 이름이 두 도구를 가르는 유일한 것이니까요. 그리고
둘을 함께 등록했다면 요청에 어느 서버를 쓸지 적을 것, 추론에 맡기지 말 것.

## 이름만 적히고 검증되지 않은 것

원격 실행 대상 밖의 로컬 `stdio` 서버입니다. 다시 찾아 헤매지 않도록 이름을
남기고, 이름을 시험으로 오해하지 않도록 표시합니다.

| 서버 | 스택 | 왜 여기 있고, 무엇이 미지인가 |
|---|---|---|
| `next-devtools` | nextjs | Vercel 공식. 문서를 읽는 게 아니라 *돌고 있는* 프로젝트를 진단합니다. 여기서 미시험. |
| `gopls mcp` | go | Go 공식 언어 서버의 실험적 MCP 모드, *현재* 프로젝트 분석용. gopls v0.20 이상 필요. 여기서 미시험. |
| `hexdocs-mcp` | elixir | Hex 문서 의미 검색. 로컬에 Node 22 · Elixir · OTP · Ollama 필요. 자기 문서는 v0.6.0을 서술하는데 안정 릴리스는 v0.5.0. 여기서 미시험. |
| `nodejs-api-docs` | nodejs | **권장하지 않습니다.** 여기서 미시험이고 저장소가 방치로 읽힙니다 — 별 9, 커밋 36, 릴리스 0, 열린 PR 42 대 열린 이슈 0. 아무도 병합하지 않는 저장소에 의존성 봇이 쌓이는 모양입니다. `snyk-labs`는 실험 조직이고 지원 제품군이 아닙니다. |

## 이 어느 것도 덮지 않는 것

- **답의 정확성.** `PASS`는 돌아온 호출이지 옳았던 호출이 아닙니다.
- **시간에 걸친 가용성.** 서드파티 엔드포인트 14개는 사라질 수 있는 것 14개입니다.
  가정하지 말고 검사기를 다시 돌리십시오.
- **브랜치 대 설치 버전.** 모든 GitMCP 엔드포인트는 기본 브랜치를 검색합니다. 그건
  이 프로젝트의 버전이 아니고, 같다고 취급하는 것이 이 프로파일들이 막으려는
  실수입니다.

## 밖으로 무엇이든 보내기 전에

위의 모든 엔드포인트는 공개 서드파티입니다. 호출은 질의, 에이전트가 구성한 도구
인자, 그리고 함께 붙인 컨텍스트를 전송합니다 — 비공개 소스, 고객 정보, 내부
호스트명, 인증 정보, 공개되지 않은 저장소 이름, 운영 로그 원문이 실릴 수 있습니다.

그럼에도 킷의 루트 설정은 14개를 전부 담고, 전부 켜 둡니다. 이것은 일반적인 권고가
아니라 *이 킷*에 한정된 결정입니다. 공개본이고, 아무도 찾지 못하는 엔드포인트는
출처가 아니기 때문입니다. 이 킷이 갈라져 나온 비공개 계열에서는 프로필을 복사하는
행위를 동의로 취급하며, 폐쇄망에서는 여전히 그쪽이 맞습니다 — 아래를 보십시오.

따라오는 것이 둘이고, 둘 다 저희가 정할 것이 아니라 운영자가 저울질할 몫입니다.
14개를 전부 등록하면 시작할 때마다 도구 스키마가 컨텍스트를 차지하고, 이름이 비슷한
`search_*` 도구가 여럿 생겨 모델이 고를 여지가 늘어납니다 — 검증 가이드는 쓰는 스택만
남기라고 권합니다. 그리고 켜 둔 서버는 하나하나가 유출 경로이므로, 바로 위 문단은
형식적인 문구가 아닙니다.

폐쇄망에서는 이것들을 운영 의존성으로 두지 마십시오. 공식 저장소를 내부에
미러링하고, 커밋을 고정하고, 색인해서, 응답마다 저장소·경로·커밋·수집일을
돌려주는 내부 읽기 전용 MCP를 제공하십시오.

## 재검증

```bash
npx -y @modelcontextprotocol/inspector --cli <엔드포인트> \
  --transport http --method tools/list --format json

npx -y @modelcontextprotocol/inspector --cli <엔드포인트> \
  --transport http --method tools/call \
  --tool-name <search 도구> --tool-arg "query=..." --format json
```

확인 순서: 종료 코드 → 응답 파싱 여부 → 도구 수 → 기대 도구 이름 존재 여부 →
호출의 종료 코드 → 원본 출력. **도구 이름이 바뀐 것은 결함입니다** — 스택별 라우팅
문서가 특정 도구를 지목하고 있어서, 개명은 그것을 조용히 깨뜨립니다.

브랜치나 릴리스가 바뀔 때, 그리고 엔드포인트가 다르게 답하기 시작할 때 다시
돌리십시오.
