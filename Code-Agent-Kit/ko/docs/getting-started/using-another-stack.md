# 다른 스택 쓰기

React + ASP.NET Core는 "지금 완성돼 있는 예시"일 뿐입니다. 꼭 이걸 쓸 필요 없어요.
킷은 공통 규칙(코어)은 그대로 두고, 기술별 **스택 팩**만 갈아끼우는 구조입니다.

## 지금 있는 스택

| 스택 | 상태 | 뜻 |
|---|---|---|
| `react-aspnetcore` | ready | 내용이 다 채워짐 → 바로 사용 |
| `csharp-winforms` | ready | 내용이 다 채워짐 → 바로 사용 (데스크톱, .NET Framework 4.7.2+) |
| 나머지 10개: `csharp-wpf`, `csharp-wcf`, `csharp-asmx`, `vue`, `nextjs`, `nodejs`, `go`, `go-htmx`, `rust`, `elixir` | blocked | 절반 채워져 있음 → 그 기술의 제약·함정·capability 탐지·문서 라우팅은 이미 있고, 여러분 프로젝트의 구체적인 값이 없음 |
| `_template` | — | 새 스택 만들 때 복사하는 빈 양식 |

`csharp-winforms`는 쓰지 않더라도 읽어둘 만합니다. Windows Forms에는 Rendered 문서가 없어서,
평소 경로가 존재하지 않을 때 Stack이 Rendered Output Layer를 어떻게 대신 확보하는지 보여줍니다 —
그 Stack의 `references/ui-evidence-contract.md` 참고.

상태 확인:

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<이름>
```

## 누가 무엇을 하나 (이게 핵심)

**당신이 하는 것**
1. 쓸 스택을 고른다.
2. 그 스택이 `blocked`면(비어 있으면) 필요한 정보를 채운다 — 버전·실행/빌드/테스트 명령·규칙처럼 **당신(또는 팀)만 아는 결정**.
3. 작업을 시작할 때 에이전트에게 **"이 스택(예: go-htmx)으로 해줘"** 라고 한 번 말한다.

**에이전트가 자동으로 하는 것**
- 당신이 말한 스택을 `docs/project-map.md`에 기록한다. → **당신이 손으로 고칠 필요 없음.**
- 이후 그 스택의 `SKILL.md`·레퍼런스·검증 프로필을 알아서 찾아 쓴다.
- 스택이 `blocked`면 게이트가 막아, 준비 안 된 스택 위에 함부로 코드를 짓지 못한다.

> 즉 "에이전트에게 스택 알려주기"는 당신 숙제가 아닙니다. 스택 이름 한 번 말하면 끝.

## 지식은 어디서 가져오나 (md 파일 vs MCP)

스택 지식의 출처는 크게 둘이고, **둘 다 "증거"로 취급**합니다 — 다른 건 언제 쓰느냐뿐입니다.

- **번들 md 레퍼런스**(`references/verified-facts.md`·`pitfalls.md`) — 잘 안 바뀌는·사내·버전 고정·니치 사실. 한 번 정리해두면 오프라인/폐쇄망에서도 되고 호출 비용 0. **스택 고유 지식의 1순위.**
- **MCP**(Context7, Microsoft Learn) — 자주 바뀌는 공식 라이브러리 사실. 작업 중 조회하고, **필요한 사실 + 출처만 요약해** 레퍼런스나 worklog에 남깁니다(전체 덤프는 버림).
- **모델 기억** — 버전·니치 사실엔 쓰지 않습니다(마지막 수단).

어느 출처든 **어디서 왔는지 기록**합니다(무슨 주장을, 어디서, 어떤 버전, 언제 — `../../stacks/<스택>/evidence-provenance.md`). 어떤 MCP를 어떤 주제에 쓸지는 스택의 `mcp/source-routing.md`, 일반 규칙은 `../core/mcp-knowledge-routing.md`, 큰 결과 요약은 `../core/mcp-result-compaction.md`.

한 줄 기준: **안 바뀌고 우리만 아는 건 md에 굽고, 바뀌는 공식 사실은 MCP로 그때그때 확인 후 요약해 남긴다.**

### 어떻게 지정하나 (실제 예제)

**MCP 지정 — 2단계.**
① MCP 서버를 프로젝트 루트 `.mcp.json`에 등록합니다(Codex는 `.codex/config.toml`, Roo는 `.roo/mcp.json`도 동일):

```json
{
  "mcpServers": {
    "microsoft-learn": { "type": "http", "url": "https://learn.microsoft.com/api/mcp" },
    "context7": { "type": "stdio", "command": "npx", "args": ["-y", "@upstash/context7-mcp"] }
  }
}
```

② "어떤 주제에 어떤 MCP를 쓸지"는 스택의 `mcp/source-routing.md`에 적습니다:

```markdown
## ASP.NET Core · C# · .NET  → Microsoft Learn MCP 사용
## React · JS 라이브러리      → Context7 사용 (핵심 라이브러리 고정: /facebook/react)
## 우선순위: 코드/검증 > 공식 MCP > 공식 저장소 > 모델 기억
```

**md 지정 — 파일에 직접 적습니다.**
사실은 `references/verified-facts.md`에 **표로**(출처·버전·날짜 포함):

```markdown
| Fact | Scope | Evidence | Last Verified |
|---|---|---|---|
| 샘플은 React 19.2.7 사용 | sample only | `package.json` | 2026-07-14 |
```

함정은 `references/pitfalls.md`(✗ 흔한 잘못 → ✓ 이 스택 방식), 화면/코드 뼈대는 `skeletons/`에 둡니다.

> 즉 **MCP = `.mcp.json`(연결) + `source-routing.md`(어디에 쓸지)**, **md = `references/`에 직접 기록**. 에이전트는 이 둘을 읽어 알아서 골라 씁니다.

## 쉬운 길: 에이전트가 인터뷰하게 한다

```text
prompts/8-fill-stack.md를 따라서 vue 스택을 채워줘.
```

에이전트가 매니페스트와 lock 파일을 읽어 탐지할 수 있는 것을 탐지하고, 읽을 수 없는
것만 물어보고, `STACK-INPUTS.md`와 `STACK-READINESS.json`을 **함께** 쓰고, 검사기를
돌려 나온 말을 그대로 전합니다. 두 파일을 손으로 고쳐도 되고 이 페이지의 나머지가 그
방법이지만 — 이제 둘이 대조되고 어긋나면 스택이 실패하므로, 손으로 맞춰 두는 일이야말로
넘겨 둘 만한 부분입니다.

## 스택 손으로 채우기 (blocked거나 새로 만들 때만)

- **이미 있는 빈 스택(go/rust/elixir)** → 그 폴더의 파일을 채운다.
- **완전히 새 스택(예: 데스크톱·사내 UI)** → 양식을 복사한다: `cp -r stacks/_template stacks/<내스택>`

채울 것(결정은 당신이 주고, 초안 작성은 에이전트에게 시켜도 됩니다 — 단 "검증됨"은 근거로 확인된 것만):
- `STACK-INPUTS.md` — 버전·프레임워크·실행/빌드/테스트 명령·규칙
- `references/` , `skeletons/` — 공식 문서·실제 코드에서(기억으로 지어내지 않음)
- `validation/validation-profile.md` — 검증 명령(+ dev 서버는 `run_service.py`)

그다음 `check-stack-readiness`가 **ready**라고 할 때까지 채우면, 그 스택도 react처럼 바로 쓸 수 있습니다.

> 빈 양식 자체가 여전히 통과하는지 확인하세요: `python tools/check-kit-selfcheck/check_kit_selfcheck.py --root .`
> 킷 자신의 검사를 통과하지 못하는 Template은 `--no-verify` 말고는 출구를 남기지 않습니다.

## AI로 채우기 (직접 다 쓰지 않아도 됨)

빈 스택을 손으로 다 쓸 필요 없습니다. **결정은 당신이, 초안은 에이전트가** 채우게 하면 됩니다.
단 킷의 정직 규칙이 그대로 적용돼서, 에이전트는 **근거 없이(기억으로) 채우지 못하고** 사실마다 출처를 답니다.

역할 나눔:
- **당신이 준다** — 당신만 아는 결정(고정할 버전, 사내 규칙, 실행/빌드/테스트 명령, 인증 방식) + **믿을 출처를 가리켜 줌**(공식 문서 MCP, 설치된 SDK 경로, 기존 동작 코드, 참고 저장소).
- **에이전트가 초안** — `verified-facts`(출처·버전·날짜 붙여), `pitfalls`(공식 문서 + 함정), `skeletons`(**실제 파일 복사**, 지어내지 않음), `validation-profile` 명령, `capability-detection`.
- **당신이 확인** — 각 사실의 출처가 진짜인지(모델 기억 아님) 보고, `check-stack-readiness`가 ready 될 때까지.

예시 지시(그대로 붙여 써도 됨):

```text
stacks/<스택>/references/verified-facts.md를 채워줘.
각 사실은 Microsoft Learn / Context7 MCP로 조회하거나 설치된 SDK·이 저장소 코드로 확인하고,
표에 Evidence·버전·날짜를 적어. 확인 못 하는 건 지어내지 말고 ⟨확인 필요⟩로 남겨.
```

```text
stacks/<스택>/skeletons/ 를 <실제 파일 경로>의 최소 예제를 복사해서 만들어줘. 기억으로 쓰지 마.
```

```text
stacks/<스택>/validation/validation-profile.md에 이 스택의 실제 실행/빌드/테스트 명령과
합격 기준(Exit Code)을 채워줘. 오래 도는 서버는 run_service.py로.
```

**왜 안전한가** — `verified-facts`는 Evidence 칸이 비면 안 되고(= 기억으로 못 채움), 확인 안 된 건 `⟨확인 필요⟩`, 뼈대는 실제 파일 복사. 그래서 AI가 채워도 "출처 있는 것만" 남습니다. 마지막에 사람이 `check-stack-readiness`로 통과를 확인합니다.

자세한 절차: `stack-input-requirements.md`, `../core/stack-extension.md`.
