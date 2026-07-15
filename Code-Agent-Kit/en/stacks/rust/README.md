# Rust Stack Profile — Planned

Rust is the preferred next experimental profile.

Candidate baseline:

- Axum
- Tokio
- SQLx
- SQLite or PostgreSQL
- optional HTMX or React frontend

Strong deterministic gates make Rust attractive for this workflow:

```bash
cargo fmt --check
cargo check
cargo clippy -- -D warnings
cargo test
```

This directory intentionally remains a placeholder until the React + ASP.NET Core sample produces public feedback.
