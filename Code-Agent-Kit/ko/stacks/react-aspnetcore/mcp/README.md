# MCP 설정

## Codex 프로젝트 설정

저장소에는 `.codex/config.toml`이 포함돼 있습니다.

```toml
[mcp_servers.microsoft_learn]
url = "https://learn.microsoft.com/api/mcp"
enabled = true

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp"]
enabled = true
```

Codex는 신뢰한 프로젝트에서만 프로젝트 범위 설정을 읽습니다.

확인 명령:

```bash
codex mcp list
```

## 일반 MCP Client 예제

`mcp.json.example`을 참고하세요.

## 선택 사항: Context7 API Key

Context7은 API Key 없이도 낮은 사용 한도로 실행할 수 있습니다. 더 높은 한도가 필요하면 사용자 범위 설정이나 환경 변수에 API Key를 둡니다. 저장소에 커밋하지 않습니다.
