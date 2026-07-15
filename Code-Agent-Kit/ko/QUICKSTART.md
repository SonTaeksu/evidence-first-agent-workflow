# 빠른 시작

성격 급하세요? 이 페이지 하나면 됩니다. 나머지 문서는 나중에 봐도 돼요.

## 한 줄 설명

AI 코딩 에이전트를 정직하게 만드는 **규칙 + 자동 검사기**. 에이전트는 프로젝트 지도를 읽고,
정해진 단계로 작업하고, 결과를 **증명**해야 합니다. 안 하면 커밋이 막힙니다.

## 30초 개념

- **지도 먼저, 추측 금지** — 코드 건드리기 전에 `docs/project-map.md`와 기능 `current.md`를 읽음.
- **감이 아니라 단계** — 모든 작업이 5단계 Gate(분석 → Task → Todo → 체크리스트 → 검증)를 거침.
- **약속이 아니라 증거** — git 커밋 게이트가 워크로그·상태 갱신 없는 소스 변경을 거부.

## 설치

1. **이 폴더의 내용**을 프로젝트 루트에 복사.
2. 프로젝트가 **git 저장소**인지, **Python**이 깔렸는지 확인(`python --version`).
3. 커밋 게이트 켜기 — 스크립트 없이 한 줄:

   ```bash
   git config core.hooksPath tools/enforce-agent-gates
   ```

4. 아래 **첫 초기화**를 한 번 하고, AI 에이전트에게: **"AGENTS.md 따라서 `<원하는 기능>` 추가해줘."**

## 첫 실행: 킷을 내 프로젝트에 맞추기 (최초 1회)

킷은 프로젝트의 **상태 문서**(`docs/project-map.md`, `docs/features/<기능>.current.md`)로
작업을 관리합니다. 새 프로젝트엔 이게 없으니 **한 번 만들어야** 합니다 — 안 그러면 에이전트가
찾을 수 있는 아무 상태 문서(예: 번들된 샘플)로 흘러갑니다.

1. **데모가 필요 없으면 지웁니다.** 이 킷엔 `samples/react-aspnetcore-taskflow/` 샘플이
   자기 상태 문서와 "priority field" 예시 과제를 갖고 들어있습니다. 그대로 두면 에이전트가
   **손님 앱이 아니라 샘플**을 작업할 수 있습니다. 실제 프로젝트면 `samples/`를 삭제하세요
   (`core` 설치 모드는 샘플을 제외합니다).
2. **경로를 고르고 부트스트랩 프롬프트를 실행** — 에이전트에게
   *"AGENTS.md 따르고 `prompts/<파일>` 실행해"*:
   - **신규/빈 프로젝트** → [`prompts/2-bootstrap-new-project.md`](prompts/2-bootstrap-new-project.md)
   - **기존 코드베이스**(이미 `.sln`·`package.json`·소스 있음) → [`prompts/1-analyze-existing-project.md`](prompts/1-analyze-existing-project.md)

   이것이 **손님 코드**에 대한 `docs/project-map.md` + 기능 `current.md`를 만들고 **스택 결정**을
   명시적으로 기록합니다. (git은 먼저 `git init` 해도 되고, 기존 저장소에 얹어도 됩니다.)
3. 이후 모든 작업은 [`prompts/0-sync-and-orient.md`](prompts/0-sync-and-orient.md)로 시작하며,
   "AGENTS.md 따라줘"라고 하면 에이전트가 자동으로 이걸 수행합니다.

> 기준: **이미 코드가 있으면 `1-analyze-existing-project`, 비었으면 `2-bootstrap-new-project`.** 둘 다 끝나면 샘플이 아니라 손님 코드를 가리키는 상태 문서가 생깁니다.

## Windows 첫 실행 (실증됨)

Windows에서는 `.ps1`/`.sh` 설치기가 자주 실패합니다(PowerShell 서명 정책, WSL `bash` 없음).
**그건 건너뛰고 위 3번 git 한 줄을 쓰세요.** 훅은 Git for Windows로 잘 돕니다. PowerShell 기준
프로젝트 루트에서 깨끗한 첫 실행:

```powershell
git init                                             # 아직 저장소가 아니면
git config core.hooksPath tools/enforce-agent-gates  # 게이트 켜기

# IDE/빌드 산출물 제외 (".vs 권한 거부" 해결)
@'
bin/
obj/
.vs/
node_modules/
__pycache__/
*.pyc
'@ | Set-Content -Encoding UTF8 .gitignore

git add .
git commit -m "chore: initial import" --no-verify    # 최초 임포트는 기능 작업이 아님
```

커밋 신원도 설정(회사 이메일 노출 방지):
`git config --global user.email "you@example.com"` (GitHub는 `@users.noreply.github.com` 권장).

## 검증 절차는 이렇게 돕니다

"완료" = 결정론적 게이트가 **실제 명령과 Exit Code로** 통과한 것 — 자기신고 "PASS"가 아닙니다.
React + ASP.NET Core 스택이면 전체 실행은 예를 들어:

```
dotnet test                          # 백엔드
npm run test                         # 프론트 단위
npm run build                        # 프론트 빌드
npm run e2e                          # 브라우저 E2E
npm run color:static / e2e:color     # 참조 스크린샷 대비 색 충실도
```

각 항목은 worklog §5에 Exit Code와 함께 기록됩니다. 명령·Exit 인용 없는 PASS는 `PENDING`으로
간주되고 커밋 게이트가 거부합니다. 오래 도는 서버는 `tools/run-managed-service/run_service.py`로
시작/종료합니다(`node` 일괄 종료 금지). 다른 스택은 `stacks/<스택>/validation/`에 자기 명령을 채웁니다.

## 게이트 우회

게이트는 git pre-commit 훅이라 git 기본 우회가 적용됩니다:

```bash
git commit -m "..." --no-verify
```

`--no-verify`는 **그 한 번의 커밋만** 훅을 건너뜁니다. 아껴 쓰세요: 최초 임포트, 곧 정규화할
긴급 핫픽스, 게이트 오판 정도. 명시적이고 눈에 보이는 선택이며, CI를 걸어두면 같은 검사가 PR에서
다시 돕니다. 완전히 끄려면(비권장): `git config --unset core.hooksPath`.

## 무엇을 보게 되나

- `docs/worklogs/`에 5단계와 증거가 담긴 **워크로그**.
- **코드 변경** + 갱신된 `current.md` / `history.md`.
- 작업을 건너뛰면 커밋이 `result: BLOCKED` + `FAIL` 사유로 멈춤.

## FAQ

- **문서 다 읽어야 하나요?** 아니요. 이 페이지 + "AGENTS.md 따라줘"면 됩니다.
- **커밋이 막혔는데 고장?** 아니요. 단계를 건너뛴 겁니다. "게이트에 막혔어, 절차대로 하고 고쳐줘".
- **공개하려는데요?** 먼저 `python tools/check-sanitization/check_sanitization.py --root .` 실행.

React + ASP.NET Core 말고 다른 스택을 쓰려면? [`docs/getting-started/using-another-stack.md`](docs/getting-started/using-another-stack.md) 참고.

더 보기: `README.md`, `AGENTS.md`, `prompts/GATE.md`, `docs/persona.md`, `docs/core/command-and-process-safety.md`, `docs/core/enforcement-matrix.md`.
