# Cline 설정

Cline은 다음을 자동으로 읽습니다.

- Root `AGENTS.md`
- `.clinerules/` 아래 Workspace Rule
- `.clineignore`

Cline IDE의 MCP 설정은 저장소 고정 파일이 아니라 MCP Servers 설정 화면에서 관리됩니다. `mcp.example.json` 내용을 복사하거나 등록하세요.

Cline CLI는 사용자 범위 `~/.cline/mcp.json`을 사용합니다.

설정 후 확인:

- Microsoft Learn MCP 연결
- Context7 MCP 연결
- 최초 평가 중에는 도구 자동 승인 사용 안 함
- UI 색상 변경 시 `npm run e2e:color` 실행
