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

## 포트와 Shell

내가 바인딩한 포트만 비운다; 리스너가 내 것인지(PID) 먼저 확인. 명령 실행 전 OS/Shell을
확정하고 cmd / PowerShell / bash 문법을 섞지 않는다.

## Evidence

Build/Test 원본 로그와 실제 Exit Code 보존; 실행 안 한 검사는 `PASS`가 아니라 `PENDING`.

> 강제 참고: 프로세스 정리는 행위적이라(커밋으로 검사 불가) **ADVISORY**. 관리 러너가
> 일괄 종료 없이 규칙을 지키는 방법이다.
