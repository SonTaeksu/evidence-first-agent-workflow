# Capability Detection — Next.js

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이 확정적이지
않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다. 한 번의 잘못된 추측이
잠시 멈추는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| router-mode | `app/`와 `pages/`의 존재 여부 | 해당 Mode의 규칙을 따름 | Owner에게 확인 | Routing 또는 Data Fetching 작업 차단 |
| major-version | Lock File의 `next` 항목 | 그 Version 안에서 답변 | Owner에게 확인 | Caching이나 Rendering 기본값을 건드리는 모든 작업 차단 |
| rendering-strategy | Route Segment 설정과 `next.config`의 Output Mode | 기존 전략 유지 | Owner에게 확인 | Static/Dynamic 동작을 바꾸는 변경 차단 |
| data-layer | 존재하는 Data 또는 ORM Package와 Server 전용 Module | 기존 Layer 사용 | Owner에게 확인 | Data 접근 방식을 지어내는 것 차단 |
| auth | Auth Package와 그 Route Handler 또는 Middleware | 그것과 통합 | Owner에게 Escalation | 보안 관련 변경 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서 다시
언급되어야 합니다. 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수 있어야 하기 때문입니다.
