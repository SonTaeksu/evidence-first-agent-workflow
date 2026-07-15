# 관리 실행 러너 (Managed service runner)

dev 서버(또는 오래 도는 프로세스)를 **기록된 PID + 포트로** 시작/중지한다. 그래서
에이전트가 이미지 이름으로 일괄 종료할 필요가 없다. 중지 시 포트가 실제로 비었는지 확인한다.

```bash
# 시작 (PID + 포트를 .agent-state/services.json에 기록)
python tools/run-managed-service/run_service.py start --name frontend --port 5173 \
  --cwd frontend -- npm run dev

# 떠 있나?
python tools/run-managed-service/run_service.py status

# 이 도구가 시작한 것만 중지하고 포트가 비었는지 확인
python tools/run-managed-service/run_service.py stop --name frontend
```

왜 필요한가: `Get-Process node | Stop-Process`, `killall node`, `pkill -f npx`,
`taskkill /IM node.exe`는 에이전트가 의존하는 MCP 서버(context7 등 npx/node로 실행)와
사용자의 다른 작업까지 죽인다. 절대 그러지 말 것. 이 도구는 기록된 PID의 프로세스 트리만
종료(Windows는 `taskkill /PID <pid> /T`, POSIX는 프로세스 그룹)하고 포트로 중지를 확인한다.
