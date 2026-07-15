# Rust 스택 프로필 — 계획

Rust는 다음 실험 스택의 우선 후보입니다.

후보 기준선:

- Axum
- Tokio
- SQLx
- SQLite 또는 PostgreSQL
- 선택적으로 HTMX 또는 React Frontend

Rust는 다음과 같은 강한 결정론적 게이트를 제공하므로 이 워크플로우와 잘 맞을 가능성이 있습니다.

```bash
cargo fmt --check
cargo check
cargo clippy -- -D warnings
cargo test
```

React + ASP.NET Core 샘플에서 공개 피드백을 확보할 때까지 이 디렉터리는 계획용 Placeholder로 유지합니다.
