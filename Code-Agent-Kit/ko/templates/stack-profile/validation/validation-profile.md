# Validation 프로필

## 검증 명령 (필수)

모든 Stack Pack은 이 표를 반드시 채웁니다. 각 행은 **복붙 가능한** 명령과 명시적
Exit Code/마커 합격 기준입니다. 이 명령들이 통과하기 전에는 완료(`prompts/GATE.md` §5)가
아니며, 자기신고는 대체가 되지 않습니다. 요약 줄만 믿지 말고 실제 오류 마커·Artifact를
직접 검사합니다("실패 0" 요약이 오류를 숨길 수 있음). 경로는 `{PLACEHOLDER}`로 두고
벤더/SDK 절대경로를 커밋하지 않습니다(세척 Gate 참조).

| Gate | 명령 (복붙) | 합격 기준 |
|---|---|---|
| 정적/Lint | `` | exit 0 |
| Build/Compile | `` | exit 0 **및** Log에 오류 마커 없음 |
| Unit/Integration | `` | exit 0, 대상 Test 전부 통과 |
| Artifact 완전성 | `` | 빈/Placeholder 블록 없음 |

## Long-running 프로세스

dev 서버·watcher 등 오래 도는 프로세스는 **관리 러너**로 시작/중지합니다 — 이미지 이름
일괄 종료 금지(`Get-Process node | Stop-Process`, `killall node`, `pkill -f npx`); 이는
에이전트 자신의 MCP 서버까지 죽입니다. `docs/core/command-and-process-safety.md` 참고.
이 스택의 실행 명령과 포트를 채웁니다:

```bash
python tools/run-managed-service/run_service.py start --name {svc} --port {PORT} --cwd {dir} -- {이 스택의 실행 명령}
python tools/run-managed-service/run_service.py status
python tools/run-managed-service/run_service.py stop  --name {svc}
```

## Format / Lint

-

## Build

-

## Tests

-

## Artifact 검사

-
