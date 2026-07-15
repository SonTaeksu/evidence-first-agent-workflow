# check-agent-config

다음 코딩 에이전트의 저장소 지침과 MCP 설정을 검사합니다.

- Codex
- Roo Code
- Zoo Code
- Cline
- Claude Code

필수 파일, JSON/TOML 구문, MCP 서버 이름, Transport 표기, 공개 알파에서 MCP Tool 자동 승인이 비활성화됐는지 검사합니다.

```bash
python tools/check-agent-config/check_agent_config.py --root .
```
