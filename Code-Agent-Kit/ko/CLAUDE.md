# Claude Code Adapter

@AGENTS.md

위에서 임포트된 `AGENTS.md` 내용이 **구속력 있는 규칙**입니다. 이 어댑터는 아무것도
더하지 않고 규칙을 다시 정의하지도 않습니다. 특히: 정직이 완료보다 우선(자기 실수를
보고하고, 불확실하면 추측 대신 멈추며, "완료"는 검증 통과한 것만), 그리고 파일을 바꾸는
모든 작업은 `prompts/GATE.md`를 거칩니다.

이는 커밋 게이트가 강제합니다: 워크로그·5단계 Gate·상태 동기화 없이 프로젝트 소스를
바꾼 커밋은 **차단**됩니다(`docs/core/enforcement-matrix.md` 참고). 절차를 건너뛰면
잡히며, 시간이 절약되지 않습니다.

라우팅: `prompts/0-sync-and-orient.md` → 상황별 Prompt → 가장 가까운 Stack `SKILL.md`
→ Project `.mcp.json`. 선택적 스탠스: `docs/persona.md`.
