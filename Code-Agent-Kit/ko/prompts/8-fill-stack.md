# 스택 채우기 — 인터뷰

스택이 `blocked`인데 열고 싶을 때, 또는 새 스택을 추가할 때 쓰십니다. 질문에 답만
하시면 읽기·쓰기·검사는 에이전트가 합니다.

스택 10개가 절반 채워진 상태로 들어 있습니다. 그 기술의 제약, 조용히 실패하는 함정,
프로젝트가 무엇을 쓰는지 알아내는 방법, 어느 문서 서버에 물어야 하는지가 이미 있습니다.
빠진 것은 여러분만 아는 것뿐입니다.

## 이렇게 말하십시오

> `prompts/8-fill-stack.md`를 따라서 `vue` 스택을 채워줘.

`stacks/` 아래의 디렉터리 이름으로 바꿔 쓰십시오.

---

## 에이전트를 위한 규칙

이 부분이 이 프롬프트의 핵심입니다. 나머지는 절차입니다.

1. **묻기 전에 탐지하라.** 답의 대부분이 이미 저장소 안에 있습니다. 읽으십시오. 적는
   모든 값은 어느 파일에서 읽었는지 밝혀야 하고, 그 파일은 실제로 존재해야 합니다 —
   `check-stack-readiness`가 증거 경로를 해석하므로, 지어낸 경로는 빈칸보다 나쁩니다.
2. **기억으로 칸을 채우지 마라.** 버전도, 명령도, 프레임워크도. 읽을 수 없고 사용자가
   말하지도 않았다면 그 칸은 `unknown`으로 둡니다. blocked는 올바른 상태이고, 추측으로
   `ready`를 주장하는 것은 이제 도구가 잡아내는 거짓말입니다.
3. **조금씩 나눠 물어라.** 세넷 개씩 묻고, 알아낸 것을 적고, 다시 묻습니다. 30개 문항
   양식을 내놓지 마십시오.
4. **두 파일을 함께 쓰라.** `STACK-INPUTS.md`는 사람이 읽는 것이고
   `STACK-READINESS.json`은 검사기가 읽는 것입니다. 둘은 대조되고, 어긋나면 스택이
   실패합니다. 한쪽만 고치지 마십시오.
5. **검사기의 판정을 전하라. 스스로 판정하지 마라.** 돌리고, 나온 말을 그대로 붙이고,
   아직 blocked면 어떤 칸이 남았는지 말하십시오.

---

## 1단계 — 스택을 읽고, 이미 아는 것을 말한다

```bash
cat stacks/<name>/STACK.md
cat stacks/<name>/STACK-INPUTS.md
cat stacks/<name>/capability-detection.md
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

`capability-detection.md`가 중요합니다. 각 capability를 저장소에서 *어떻게* 탐지하는지
적혀 있으니, 추측하지 말고 그대로 따르십시오.

보고할 것:

- `unknown`인 칸이 무엇인지
- 그중 탐지할 수 있다고 보는 것과, 어느 파일에서 할 것인지
- 사용자만 답할 수 있는 것이 무엇인지

## 2단계 — 탐지할 수 있는 것을 탐지한다

프로젝트를 읽습니다. 스택 계열별로 볼 곳:

| 스택 | 읽을 것 |
|---|---|
| WPF, WCF, ASMX | `*.csproj`(`TargetFramework` / `TargetFrameworkVersion`), `App.config` / `Web.config`, `packages.config` 또는 `PackageReference` |
| Vue, Next.js, Node.js | `package.json` **과 lock 파일** — 권위는 lock 파일입니다. `package.json`은 범위를 적을 수 있습니다 |
| Go, Go + HTMX | `go.mod`(module 경로와 `go` directive), 그리고 검증을 돌릴 기계의 `go version` |
| Rust | `Cargo.toml`(`edition`, `rust-version`), `Cargo.lock`, `rustc --version` |
| Elixir | `mix.exs`, `mix.lock`, `elixir --version`과 OTP 릴리스 |

테스트 디렉터리나 테스트 스크립트, lint 설정, CI 워크플로도 찾아보십시오 — 보통 검증
관련 질문을 묻지 않고도 답해 줍니다.

찾은 것마다 **읽어 온 파일 경로**를 기록하십시오. 그 경로가 증거가 되고, 실제로
존재해야 합니다.

## 3단계 — 남은 것만 묻는다

보통 이런 것들이고, 진짜로 사용자가 답할 몫입니다.

- **여기서 기능 하나는 무엇인가?** 한 기능이 무엇까지 건드려도 되고, 무엇이 공유물인가?
- **정확한 빌드·테스트 명령**과 실패가 어떻게 보이는가. 아무도 돌려본 적 없는 명령은
  검증 프로파일이 아닙니다.
- **데이터 접근과 인증** — 어떤 라이브러리, 어떤 패턴, 아니면 없음.
- **배포** — 빌드가 무엇을 만들어야 하고 어디로 가는가.
- **기밀 분류** — 이 스택 자재가 공개 저장소에 나와도 되는가?

한 번에 세넷 개씩. 사용자가 "모른다"고 하면 그 칸은 `unknown`으로 남고 스택은 blocked로
남습니다. 인터뷰의 실패가 아니라 올바른 결과입니다.

## 4단계 — 두 파일을 함께 쓴다

`STACK-INPUTS.md`에서 `Value or Path`, `Evidence`, `Status` 칸을 채우십시오. `Key`
열은 건드리지 마십시오 — 그 표와 매니페스트를 잇는 것이 그 열입니다.

`STACK-READINESS.json`에서 같은 key의 `status`와 `evidence`를 맞춰 넣습니다.

```json
{
  "key": "runtime-sdk-versions",
  "required": true,
  "source": "auto",
  "status": "detected",
  "evidence": ["frontend/package.json", "frontend/package-lock.json"],
  "notes": "package.json의 범위가 아니라 lock 파일에서 읽음."
}
```

status 값은 이 넷뿐입니다.

| 값 | 뜻 |
|---|---|
| `detected` | 파일에서 읽었고, 그 파일이 `evidence`에 적혀 있음 |
| `confirmed` | 사용자가 말했고, `evidence`가 그것이 적힌 곳을 가리킴 |
| `not-applicable` | 여기엔 정말 해당 없음 — 이유를 `notes`에 |
| `unknown` | 확립되지 않음. 정직한 기본값 |

capability의 `present`와 `absent`는 둘 다 `evidence`**와** `selected_path`가
필요합니다. *absent*를 증명하는 데 산문은 필요 없습니다 — 탐색 기록을
`capability-detection.md`에 남기고 그 파일을 인용하십시오.

`declared_state`는 아직 건드리지 마십시오.

## 5단계 — 상태는 검사기가 정한다

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

`READY`, `PROVISIONAL`, `BLOCKED` 중 하나를 출력합니다. `declared_state`를 **출력된
그대로** 적고 한 번 더 돌리십시오 — 선언이 도출과 맞는지도 검사하므로, 잘못 적으면 즉시
실패합니다.

출력을 답변에 그대로 붙이십시오. blocked면 남은 칸을 나열하고 멈추십시오. 판정을 예쁘게
만들려고 무엇도 조정하지 마십시오.

## 6단계 — 기록한다

- `docs/project-map.md`의 환경 절에 스택을 추가합니다.
- 기능 작업의 일부였다면, 워크로그 Analysis 절에 스택 이름과 내린 capability 결정을
  함께 적습니다.

---

## 검사기가 지적할 것들

| Finding | 무슨 일이 있었는가 |
|---|---|
| `input-unresolved` | 필수 칸이 아직 `unknown` |
| `input-without-evidence` | 해소됐다고 적었는데 `evidence`가 비어 있음 |
| `evidence-not-found` | 인용한 경로가 하나도 존재하지 않음. 위조 방지 장치입니다 |
| `inputs-document-drift` | 표와 매니페스트가 어긋남. 뒤처진 쪽을 고치십시오 |
| `declared-state-mismatch` | `declared_state`가 도출된 것과 다름 |
| `capability-without-path` | capability가 `present`인데 `selected_path`가 없음 |

전부 어느 칸인지 이름을 말해 줍니다. 무엇이 틀렸는지 추측할 필요가 없습니다.

## 문서 조회는 어디로 가는가

`stacks/<name>/mcp/source-routing.md`에 이 스택에 권위 있는 서버와 그렇지 않은 서버가,
그리고 시험했을 때 각 서버가 실제로 노출한 도구 이름이 적혀 있습니다. 그 서버들은 **기본
꺼져 있습니다** — 켜기 전에, 특히 폐쇄망이라면
[`docs/core/mcp-source-verification.md`](../docs/core/mcp-source-verification.md)를
먼저 보십시오.
