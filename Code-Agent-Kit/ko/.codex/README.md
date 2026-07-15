# Codex MCP 설정

## 구속 규칙

Codex는 관례상 프로젝트 루트의 `AGENTS.md`를 읽습니다 — 그것이 구속력 있는 규칙입니다: 정직이 완료보다 우선, 5단계 `prompts/GATE.md`, 그리고 워크로그·상태 동기화 없는 소스 변경을 차단하는 커밋 게이트(`docs/core/enforcement-matrix.md`). 아래 MCP 설정은 별개입니다.


Codex는 신뢰한 프로젝트에서 프로젝트 범위의 `.codex/config.toml`을 사용할 수 있습니다.

설정된 서버:

- `microsoft_learn`: Streamable HTTP를 통해 Microsoft Learn 공식 문서를 제공
- `context7`: 로컬 STDIO 프로세스를 통해 최신 React 및 JavaScript 라이브러리 문서를 제공

Codex에서 프로젝트를 연 뒤:

1. 프로젝트를 신뢰합니다.
2. MCP 설정을 변경했다면 Codex를 재시작합니다.
3. `/mcp` 또는 `codex mcp list`를 실행합니다.
4. 두 서버가 모두 연결됐는지 확인합니다.

Context7은 API 키 없이도 낮은 한도로 실행할 수 있습니다. 더 높은 사용량이 필요하면 사용자 범위 설정에 API 키를 추가하세요. API 키를 저장소에 커밋하면 안 됩니다.
