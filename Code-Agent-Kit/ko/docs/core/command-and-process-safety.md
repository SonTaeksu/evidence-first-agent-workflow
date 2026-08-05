# Command과 Process 안전

## 내가 시작한 것만 건드린다

시작한 모든 Process(dev 서버, build watcher, test runner, 컨테이너)의 PID와 Cleanup
계획을 기록한다. 완료 시 **그 PID만** 종료하고, 실제로 사라졌는지(예: 포트가 비었는지) 확인한다.

## 이미지 이름으로 일괄 종료 금지

금지 — 이는 에이전트가 의존하는 MCP 서버(context7 등 `npx`/node 실행)와 사용자의 다른
편집기·서버·빌드까지 죽인다:

```
taskkill /F /IM node.exe        # 금지
Get-Process node | Stop-Process # 금지
killall node                    # 금지
pkill -f npx                    # 금지
killall dotnet | killall java   # 금지
```

## 관리 러너를 쓴다 (규칙이 아니라 방법)

PID 추적을 손으로 짜지 말 것. 오래 도는 프로세스는 관리 러너로 시작/중지한다. PID+포트를
기록하고 **그 PID 트리만** 종료한 뒤 확인한다:

```bash
python tools/run-managed-service/run_service.py start --name frontend --port 5173 --cwd frontend -- npm run dev
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name frontend   # 포트가 비었는지 확인
```

떠도는 포트를 손으로 멈춰야 하면, 이미지 이름이 아니라 **그 포트의 소유 PID만** 노린다:

```powershell
# Windows: 포트 소유 PID를 찾아 그 PID 트리만 종료
$pid = (Get-NetTCPConnection -LocalPort 5173 -State Listen).OwningProcess
taskkill /PID $pid /T /F
```

## 포트

내가 바인딩한 포트만 비운다. 리스너가 내 것인지(PID) 먼저 확인한다.

## Shell과 경로

**첫 명령을 내리기 전에** OS와 Shell을 확정하고, 그 답을 Project Map에 기록해 다음 Session이
다시 탐색하지 않게 한다. cmd / PowerShell / bash 문법을 섞지 않는다.

### 두 Windows Shell의 구분자는 정반대다

```powershell
cd app; npm run build          # PowerShell 5.1 — && 는 구문 오류
```
```bat
cd app && npm run build        REM cmd — ; 는 구분자가 아님
```

cmd의 `cd`는 **줄의 나머지 전체**를 경로로 삼으므로, 같은 줄의 뒤 내용이 통째로 삼켜진다.

### 애초에 디렉터리를 바꾸지 않는 편이 낫다

쓸 만한 도구는 전부 디렉터리를 인자로 받는다. 그걸 쓰면 실패 유형 하나가 통째로 사라진다.

```bash
git -C "$ROOT" status
mvn -f "$ROOT/backend/pom.xml" test
npm --prefix "$ROOT/frontend" run build
python "$ROOT/tools/check-state-model/check_state_model.py" --project-docs "$DOCS"
```

### 경로는 항상 인용한다 — 공백이 반드시 들어오기 때문이다

`C:\Users\Name\My Projects\app` 같은 경로는 Windows에서 예외가 아니라 **기본값**이다. 인용하지
않으면 인자 두 개로 쪼개지고, 명령은 존재하지 않는 경로를 읽는다. 대개 "따옴표를 빠뜨렸다"가
아니라 엉뚱한 메시지를 낸다.

```bash
cd $ROOT            # NO  — 첫 공백에서 깨진다
cd "$ROOT"          # yes
cp $SRC $DEST       # NO
cp "$SRC" "$DEST"   # yes
```

PowerShell에서는 실패가 더 조용하고 더 나쁘다. `Test-Path`·`Resolve-Path`·`Get-Content`·
`Remove-Item`·`New-Item`과 그 계열은 위치 매개변수의 `[`·`]`·`*`·`?`를 **Wildcard로 해석**한다.
`project [old]` 같은 디렉터리는 오류를 내지 않고 **아무것도 매칭하지 않으며**, Script는 그 File이
없는 것처럼 그대로 진행한다.

```powershell
Test-Path $Image                      # NO  — Glob으로 해석된다
Test-Path -LiteralPath $Image         # yes
Get-Content -Raw -LiteralPath $File   # yes
```

### `.ps1`에는 UTF-8 BOM이 필요하고 `.sh`에는 있으면 안 된다

Windows PowerShell 5.1은 BOM 없는 File을 시스템 ANSI 코드페이지로 읽는다. 비ASCII Literal이
깨지고, 그것이 비교나 정규식에 쓰이면 표시만이 아니라 **판정 자체가 실패**한다. Shell Script나
git Hook에 BOM이 붙으면 그 바이트가 앞에 오므로 shebang을 잃는다.

복사·배포 과정에서 이것을 보존한다 — Resource Filtering, 인코딩 변환, 개행 정규화가 조용히
없앤다.

### 긴 외부 명령은 File로 뺀다

절대경로 4개가 필요하고 그중 둘에 공백이 있으며 루트가 서로 다른 명령은 반드시 잘못 타이핑된다.
`.bat` 또는 `.sh` Wrapper로 빼고, PC당 1회 생성하고, `.gitignore`에 넣고, **로그 파일명을 고정**해서
검사가 어떤 File을 읽을지 항상 알게 한다.

> `tools/check-shell-safety`가 강제한다: `.ps1` BOM, `.sh`·Hook의 BOM 부재, `-LiteralPath` 누락,
> 경로 자리의 미인용 Shell 변수. 발견 시 exit 2. 디렉터리를 바꾸지 않는 것은 권고이고 나머지는
> 검사된다.

## Evidence

Build/Test 원본 로그와 실제 Exit Code 보존; 실행 안 한 검사는 `PASS`가 아니라 `PENDING`.

> 강제 참고: 프로세스 정리는 행위적이라(커밋으로 검사 불가) **ADVISORY**. 관리 러너가
> 일괄 종료 없이 규칙을 지키는 방법이다.
