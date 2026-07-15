# Enforcement Matrix — Markdown 규칙의 기계 강제화 (최대치)

이 문서는 `AGENTS.md`, `prompts/GATE.md`, `docs/core/*`에 **산문으로 적힌 규칙**을 하나씩 나열하고, 각 규칙을 어디까지 **기계적으로 강제**했는지 정직하게 표기한다.

강제 등급:

- **BLOCK** — 결정론적으로 검사 가능. 위반 시 커밋(pre-commit)·병합(CI)에서 즉시 차단. `enforce_gates.py`가 담당.
- **EVIDENCE** — 규칙 자체는 인지적이라 직접 검사 불가하지만, 규칙이 남겨야 할 **산출물(워크로그 섹션·상태 문서)** 을 강제한다. 단계를 건너뛰면 산출물이 비어 BLOCK으로 잡힌다. (간접 강제)
- **TOOL** — 기존 킷 도구가 이미 결정론적으로 검사(자체 실행). CI/훅에서 호출.
- **ADVISORY** — 원리상 커밋 산출물만으로는 검증 불가. 강제 불가능한 잔여분(사유 명시).

---

## AGENTS.md

| 규칙 | 등급 | 강제 방법 |
|---|---|---|
| Password/Secret/Key를 소스·설정에 평문 저장 금지 | **BLOCK** | `gate_secret_scan` — 스테이징 소스/설정 diff에서 자격증명 패턴 탐지, 위반 시 exit 2 |
| 소스 작업은 워크로그(체크포인트)를 남겨야 함 | **EVIDENCE** | `gate_worklog_and_gate_sections` — 소스 변경 시 `docs/worklogs/*.md` 산출 강제 |
| 완료: current/history/Project Map 동기화 | **BLOCK / WARN** | `gate_state_sync` — current+history 필수(BLOCK); project-map은 "영향 검토"라 미갱신 시 WARN |
| 완료: 최종 Git Diff 검토, PENDING 정직 보고 | ADVISORY | diff 사실은 검사하나 "검토했는지·정직한지"는 인지적. §5 Verification 존재로 부분 유도 |
| 시작 순서: Project Map → current → related 먼저 읽기 | ADVISORY / EVIDENCE | "읽었는지"는 관측 불가. 워크로그 §1 Analysis 라우팅 필드 요구로 간접 유도 |
| Unknown은 `⟨확인 필요⟩`로, 추측 금지 | ADVISORY | 추측 여부 판별 불가. (선택) placeholder 토큰 검사로 부분 차단 가능 |
| 절차 무조건 준수; 사용자가 빠뜨린 입력은 받아낼 때까지 조르기 | ADVISORY / EVIDENCE | 조르는 건 행위적. 빠진 입력은 이후 Gate 실패로 드러남 |

## prompts/GATE.md

| 규칙 | 등급 | 강제 방법 |
|---|---|---|
| 5개 헤더(1 Analysis→5 Verification) 이름·순서 유지, 누락 금지 | **BLOCK** | `gate_worklog_and_gate_sections` — 5개 섹션 헤더 존재 검사, 누락 시 exit 2 |
| Expected Files에 구체 항목 1개 이상 | **BLOCK** | Expected Files 아래 `- [ ] path` 항목 존재 검사 |
| 스테이징 소스는 Expected Files에 선언돼야 함 | **BLOCK(옵션)** | `gate_unexpected_files` — `--strict-scope`면 미선언 소스 차단, 기본은 WARN |
| Prewrite Boundary(토큰 후에만 수정) | ADVISORY → TOOL | v0.1.6엔 토큰 도구 없음. 신버전 `check-workflow-preflight` 이식 시 TOOL로 승격 |
| Analysis 중 구현하지 않음 | ADVISORY | 인지적 순서. 검사 불가 |

## docs/core/state-and-memory-model.md

| 규칙 | 등급 | 강제 방법 |
|---|---|---|
| current/history/worklog 역할 분리, worklog가 current 대체 금지 | **TOOL** | 기존 `check-state-model` self-test·검사 (CI 실행) |
| history는 append-only | ADVISORY | diff로 부분 확인 가능하나 완전 강제는 아님 |

## docs/core (기타) 및 스택

| 규칙 | 등급 | 강제 방법 |
|---|---|---|
| Git Scope: 무관한 변경 없음 | **TOOL** | 기존 `check-git-scope` (CI/훅) |
| 어댑터 설정 정합성(.mcp.json 등) | **TOOL** | 기존 `check-agent-config` (Python ≥3.11 필요) |
| Build/Test Exit Code 보존, 자기신고 불가 | **TOOL** | 기존 `check-build-log` self-test |
| UI 색 대비 / 빈 Visual Block | **TOOL** | 기존 `ui-color-gate`, `spa-screen-extractor` |
| 포터블 킷 경로/링크 패리티(en=ko) | **TOOL** | 기존 `check-portable-kit` |
| 스택 준비도(capability 확인 전 사용 금지) | **TOOL(부분)** | 기존 `check-stack-readiness`. 실제 API 사용 차단은 ADVISORY 잔존 |
| 공개 트리에 조직·독점 명칭 없음 | **BLOCK** | `check-sanitization` (CI + 릴리스 전); 매치 시 exit 2 |

---

## 도달한 최대치와 정직한 경계

**강제됨(BLOCK/EVIDENCE/TOOL):** 자격증명 노출, 워크로그+5섹션, 상태 동기화, Expected Files,
세척, 그리고 기존 도구(state-model·git-scope·build-log·color·portable-parity)를 CI/훅에서
호출. 커밋·CI에서 자동 실행되어 위반물이 저장소에 착지하지 못한다.

**강제 못 함(ADVISORY):** "먼저 읽었는지", "추측 안 했는지", "근거 우선순위 지켰는지" 같은
인지·판단 규칙. 커밋 산출물로 검증 불가 → 대신 그 규칙이 남겨야 할 산출물(워크로그 섹션·상태
문서)을 강제해 우회 시 흔적이 남게 한다. 현재 기술로 가능한 최대치다.

**쓰기 시점 차단(A):** 절차 없이 파일 수정하는 순간 자체 차단은 플랫폼의 write-hook/권한
API가 필요하다. 커밋 차단(B)+CI 차단(C)이 그 대체 방어선이며 "위반 후 정상인 척 완료"를
불가능하게 한다.
