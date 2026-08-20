# MCP — 한 장으로

에이전트가 자기 기억 대신 실제 문서를 보게 만드는 데 필요한 것 전부입니다.
전에 `docs/core/`에 따로 있던 두 파일(`mcp-knowledge-routing.md`,
`mcp-result-compaction.md`)을 대신합니다.

여기 **일부러 넣지 않은** 것이 둘 있습니다.

- **증거.** 실제로 무엇에 접속했고, 무엇을 노출했고, 무엇은 이름만 있었는지는
  [`core/mcp-source-verification.md`](core/mcp-source-verification.md)에 있습니다.
  아무도 접속해 본 적 없는 서버는 지어낸 서버와 글로는 구별되지 않으므로, 그
  구분을 기억이 아니라 문서로 남깁니다.
- **스택별 라우팅.** `stacks/<스택>/mcp/source-routing.md`는 스택 안에 그대로
  둡니다. `install-kit.py`가 스택을 하나씩 설치하기 때문에, 이걸 여기로 옮기면
  설치받은 프로젝트는 반쪽짜리 스택을 갖게 됩니다.

## 무엇이 들어 있고, 전부 켜져 있습니다

킷의 설정에는 서버 17개가 전부 켜진 채로 들어 있습니다. 그중 14개는
**2026-08-05**에 MCP Inspector로 확인했습니다 — 인증 없이 접속했고, 도구
목록을 냈고, 실제 `tools/call`에 답했습니다. `context7`은 stdio이고 그 검사
이전부터 있었습니다. DevExpress 둘은 등급이 낮습니다 — 표 아래를 보십시오.

| 서버 | 엔드포인트 | 용도 |
|---|---|---|
| `microsoft-learn` | `https://learn.microsoft.com/api/mcp` | .NET, C#, ASP.NET Core, EF Core |
| `wpf-docs` | `https://gitmcp.io/dotnet/docs-desktop` | WPF |
| `wcf-docs` | `https://gitmcp.io/dotnet/docs` | WCF |
| `asmx-docs` | `https://gitmcp.io/dotnet/AspNetDocs` | ASMX / ASP.NET 웹 서비스 |
| `vue-docs` | `https://gitmcp.io/vuejs/docs` | Vue |
| `vue-docs-specialized` | `https://mcp.vue-mcp.org/mcp` | Vue 생태계 — **PARTIAL**, 아래 참고 |
| `nextjs-docs` | `https://gitmcp.io/vercel/next.js` | Next.js |
| `nodejs-docs` | `https://gitmcp.io/nodejs/node` | Node.js |
| `go-docs` | `https://gitmcp.io/golang/go` | Go |
| `go-htmx-docs` | `https://gitmcp.io/donseba/go-htmx` | Go + HTMX |
| `deepwiki` | `https://mcp.deepwiki.com/mcp` | 공개 저장소 전반, 서술형 |
| `rust-book` | `https://gitmcp.io/rust-lang/book` | Rust, Book |
| `rust-reference` | `https://gitmcp.io/rust-lang/reference` | Rust, Reference |
| `elixir-docs` | `https://gitmcp.io/elixir-lang/elixir` | Elixir |
| `context7` | stdio, `npx -y @upstash/context7-mcp` | React, Vite, Vitest, Playwright |
| `dxdocs` | `https://api.devexpress.com/mcp/docs` | DevExpress 컴포넌트 — **목록만 확인, 호출 안 함**, 아래 참고 |
| `dxdocs24_2` | `https://api.devexpress.com/mcp/docs?v=24.2` | 같은 서버, v24.2 고정 |

원격 서버의 전송 방식은 전부 **Streamable HTTP**입니다. 취향이 아닙니다 —
같은 검사를 SSE로 돌렸을 때 GitMCP 엔드포인트가 전부 `405`를 냈습니다.

### 믿고 쓰기 전에 읽어야 할 두 가지

**`vue-docs-specialized`는 PARTIAL입니다.** 접속과 도구 목록(5개)까지는 됐지만
실제 `vue_docs_search` 호출이 `isError:true`를 냈습니다. `vue-docs`를 우선
쓰십시오. 켜서 넣어 둔 것은 직접 다시 시험해 보시라는 뜻이지, 동작한다는 뜻이
아닙니다.

**DevExpress 둘은 나머지와 등급이 다릅니다.** **2026-08-06**에 인증 없이
접속해 `tools/list`가 도구 두 개(`devexpress_docs_search`,
`devexpress_docs_get_content`)를 돌려줬습니다. 실제 `tools/call`은 하지
않았고 고정 URL도 따로 시험하지 않았으므로, 둘 다 `PASS`로 기록하지 않습니다.

규칙 둘은 이 킷의 취향이 아니라 **서버가 자기 도구 설명에 적어 둔 것**입니다.
`devexpress_docs_get_content` 앞에는 반드시 `devexpress_docs_search`를 먼저
불러야 합니다 — 검색은 발췌만 돌려주기 때문입니다. 그리고 `get_content`에
넘기는 URL은 검색 결과에서 얻은 것이어야 하며, 스키마가 "일반 지식으로 URL을
만들지 말라"고 명시합니다. `devexpress_docs_search`는 닫힌 enum에서 고른
`technologies` 배열도 필수입니다(`WindowsForms`, `WPF`, `AspNetCore`,
`XtraReports`, `Blazor`, `VCL`, `XPO` 등). 그래서 산문으로 쓴 플랫폼 이름은
빈 결과가 아니라 **스키마 오류**가 됩니다. `?v=` 버전 고정은 **v24.2
이상만** 지원하고, 그보다 이전 릴리스를 고정하는 공식적인 방법은 없습니다.

**17개를 다 켜 두는 데는 대가가 있습니다.** 검증 가이드의 권고는 오히려 반대입니다
— 프로젝트가 실제로 쓰는 스택만 등록하면 "도구 라우팅 오류와 불필요한 도구 스키마
컨텍스트를 줄일 수 있다"고 적혀 있습니다. 서버 하나하나가 시작할 때마다 스키마로
컨텍스트를 먹고, 이름이 비슷한 `search_*`·`fetch_*` 도구가 여럿 생겨 모델이 고를
여지가 늘어납니다. **안 쓰는 스택의 항목을 지우는 것은 정상적인 편집이지 기능
축소가 아닙니다.**

## 출처 우선순위

1. 이 프로젝트의 코드, 매니페스트, lock 파일, 생성된 산출물.
2. 결정적인 빌드·테스트·런타임 증거와 종료 코드.
3. MCP로 가져온 공식 문서.
4. 공식 저장소와 릴리스 노트.
5. 모델의 기억 — 버전에 민감한 사실에는 **절대** 쓰지 않습니다.

## 기술별 라우팅

| 무엇을 물을 때 | 어디로 |
|---|---|
| .NET, C#, ASP.NET Core, DI, 설정, 로깅, 인증/인가, EF Core | `microsoft-learn` |
| React 코어 | `context7`, `/facebook/react`로 고정 |
| Vite, Vitest, React Testing Library, Playwright, React Router | `context7` — 라이브러리 ID를 먼저 확인 |
| 스택 프로파일이 있는 것 전부 | 그 스택의 `mcp/source-routing.md` |

질문을 엉뚱한 서버로 보내도 오류는 나지 않습니다. 다른 기술에 대한 확신에 찬
답이 나옵니다. 그게 더 나쁩니다.

## 서버를 등록했다고 모델이 쓰는 것은 아닙니다

이 규칙은 여기뿐 아니라 프로젝트의 에이전트 지침에 들어가야 합니다.

- API, 버전별 동작, 설정에 관한 질문을 학습 지식만으로 답하지 않습니다.
- `search_*`를 먼저 부르고, 본문은 `fetch_*`로 가져옵니다.
- 문서와 구현이 어긋날 수 있으면 `search_*_code`로 교차 확인합니다.
- 저장소의 기본 브랜치가 이 프로젝트에 설치된 버전과 같다고 가정하지 않습니다.
- 사용한 저장소, 경로, 버전 또는 커밋을 밝힙니다.
- 검색해서 없었으면 없었다고 말합니다. 기억으로 메우지 않습니다.

기억하지 말고 반드시 찾아볼 것: 어떤 버전에서 API가 생기거나 바뀌었는지, 설정
키의 정확한 철자, 그리고 기본값 — 마지막 것이 조용히 바뀌었을 가능성이 가장
높습니다.

## MCP를 못 쓸 때

1. 로컬 프로젝트 코드와 lock 파일을 봅니다.
2. 공식 출처만 씁니다.
3. 확인할 수 없는 버전 민감 동작은 멈추고 `knowledge unavailable`로 보고합니다.
4. 공식 출처 조회를 모델 기억으로 조용히 바꿔치기하지 않습니다.

프로젝트의 버전과 출처가 설명하는 버전이 다르면 **멈추고 그 불일치를 보고**하며,
`⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

## 돌아온 결과를 압축하기

MCP는 검색 수고를 줄여 주지만 컨텍스트 한도를 없애 주지는 않습니다.

1. 그 작업에 필요한 사실만 뽑습니다.
2. 출처, 버전, 확인 방법을 기록합니다.
3. 압축한 사실을 워크로그나 스택의 `evidence-provenance.md`에 넣습니다.
4. 허용되면 링크나 식별자를 남깁니다.
5. 조회 결과 전문을 현재 상태 문서에 복사하지 않습니다.
6. 다음 세션에 전문을 다시 밀어 넣지 않습니다.

현재 상태 문서는 검증된 결정을 적는 곳이지 조회 기록을 쌓는 곳이 아닙니다.

## 연결하기

킷에 이미 설정돼 있습니다. 에이전트별 파일은 이렇습니다.

| 에이전트 | 파일 |
|---|---|
| Claude Code | `.mcp.json` |
| Codex | `.codex/config.toml` |
| Roo / Zoo | `.roo/mcp.json` |
| Cline | `agent-configs/cline/mcp.example.json`을 클라이언트로 복사 |

클라이언트마다 필드 이름이 다릅니다 — `mcpServers`, `servers`, `serverUrl`,
`httpUrl`. 중요한 값은 전송 방식과 URL 둘뿐입니다.

`.codex/config.toml`은 키에 밑줄을 씁니다(`vue_docs`). 그 파일이 원래 그렇게
쓰고 있었기 때문이고, 그래서 Codex가 보여 주는 서버 이름이 다른 곳에서 쓰는
하이픈 이름(`vue-docs`)과 다를 수 있습니다. ⟨확인 필요: Codex가
하이픈 키를 받는지 — 시험하지 않았습니다.⟩

`stdio`만 되는 클라이언트라면:

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

## 밖으로 내보내기 전에

이것들은 **공개된 제3자 엔드포인트**입니다. 호출 한 번에 질의, 에이전트가 만든
도구 인자, 그리고 함께 실린 컨텍스트가 나갑니다 — 비공개 소스, 고객 정보, 내부
호스트명, 인증 정보, 공개되지 않은 저장소 이름, 운영 로그 원문이 실릴 수
있습니다.

폐쇄망에서는 이것들을 운영 의존물로 삼지 마십시오. 공식 저장소를 내부에
미러링하고, 커밋을 고정하고, 색인해서, 답변마다 저장소·경로·커밋·조회 일시를
돌려주는 내부 읽기 전용 MCP를 세우십시오. 공개 엔드포인트는 공개 기술 조사에만
쓰십시오.

## 다시 확인하기

```bash
npx -y @modelcontextprotocol/inspector --cli https://gitmcp.io/vuejs/docs \
  --transport http --method tools/list --format json
```

도구 이름이 바뀌었다면 그건 사소한 사항이 아니라 발견 사항입니다. 위의 라우팅
규칙이 특정 도구 이름을 지목하고 있기 때문입니다.
