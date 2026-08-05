# Roadmap

[English](ROADMAP.md) | **한국어**

## 완료

- 거버넌스 코어: 5단계 Gate, 외부화 상태(current / append-only history / worklog), 결정론적 검사기.
- 기계 강제화: 커밋 + CI 게이트, 공개용 세척 게이트.
- 독립 복사 가능한 `Code-Agent-Kit/en`·`ko` 미러.
- 한 페이지 QUICKSTART, 선택적 에이전트 스탠스.
- React + ASP.NET Core 샘플 스택.
- .NET Framework 4.7.2+ C# Windows Forms 스택 — Rendered 문서를 만들지 않는 UI Framework를 위한 Rendered Output 경로 포함.
- 킷의 자기검사: `check-kit-selfcheck`가 문서화된 복사 원본을 킷 자신의 Validator에 돌리고, `check-mirror-parity`가 언어 Mirror와 문서가 적은 수치를 실측과 대조.
- `docs/core/gate-design-principles.md` — 새 검사가 무언가를 차단할 수 있게 되기 전에 만족해야 할 조건.
- 비용·위험을 명시한 입문자용 README, 전체 참조는 `OVERVIEW.md`로 분리.
- 모든 검사가 Python + PowerShell 쌍으로 출하되고, 그 쌍이 같다는 것이 *증명*됩니다. `check-script-parity`가 사례별로 판정 **과** finding 식별자를 비교하고 하나라도 어긋나면 실패합니다. 커밋 훅이 PowerShell로 넘어가므로 Python 없는 기계에서도 게이트가 걸립니다.
- 스택 readiness가 **선언이 아니라 측정**입니다. `check-stack-readiness`가 인용된 모든 증거 경로를 트리에서 해석합니다. 존재하지 않는 파일을 가리키는 매니페스트가 예전에는 `ready`로 통과했습니다.
- 스택 프로파일 12개: ready 2개, 그리고 소유자 입력을 기다리면서 그 기술의 제약·함정·capability 탐지 규칙·문서 라우팅을 담은 10개.
- 문서 출처를 나열이 아니라 검증으로. 공개 MCP 엔드포인트 14개를 실제로 연결해 호출까지 확인했고, `docs/core/mcp-source-verification.md`에 실행 기록·부분 성공 1건·검토 후 배제한 후보 1건, 그리고 그 검사가 증명하지 *못하는* 것을 적었습니다.
- 이 저장소에 자체 CI가 생겼습니다. 이전에는 없었고, 그래서 실패하는 self_test가 세 릴리스를 살아남았습니다.

## 다음

- blocked 상태인 10개 스택을 소유자가 버전·명령·규약을 주는 대로 채우기. 프로파일은 이미 작성돼 기다리고 있습니다.
- prewrite-token preflight 이식 — "통과 토큰 이후에만 소스 수정"을 권고가 아니라 하드 도구 게이트로.
- 스택별 아티팩트/바인딩 검사기, Artifact/Rendered/Runtime 결과 집계.
- 공개 릴리스를 작은 로컬 모델에서 끝까지 돌린 기록 — 관리자의 사내 버전 보고를 재현 가능한 것으로 교체.
- 관리자 장비 이외의 도입 보고 — README의 모든 주장을 제한하는 것이 이 공백입니다.

## 소유자 입력을 기다리는 스택

각 스택에는 그 기술의 제약, 조용히 실패하는 함정, 프로젝트가 무엇을 쓰는지 알아내는
방법, 어떤 문서 서버에 물어야 하는지가 이미 들어 있습니다. 빠진 것은 버전, 빌드·테스트
명령, 데이터 접근, 인증, 배포 — 킷이 추측을 거부하는 것들입니다.

- WPF (.NET Framework 4.7.2+) — skeleton 포함, 아직 어디서도 컴파일 검증 안 됨
- WCF (.NET Framework 4.7.2+)
- ASMX / ASP.NET XML Web Services (.NET Framework 4+)
- Vue.js
- Next.js
- Node.js
- Go
- Go + HTMX
- Rust
- Elixir
