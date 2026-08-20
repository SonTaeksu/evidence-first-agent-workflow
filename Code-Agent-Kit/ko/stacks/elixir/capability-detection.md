# Capability Detection — Elixir

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이 확정적이지
않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다. 한 번의 잘못된 추측이
잠시 멈추는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| versions | `mix.exs`의 `elixir` 요구 Version, `mix.lock`, 그리고 Validation을 실행하는 Machine의 `elixir --version` | 그 범위 안에서 답변 | Owner에게 확인 | Version에 민감한 작업 차단 |
| phoenix-liveview | `mix.lock`의 `phoenix`와 `phoenix_live_view` 항목 | 그 Version 안에서 답변 | Owner에게 확인 | Lifecycle에 민감한 LiveView 작업 차단 |
| ecto | `ecto` 항목과 함께 Repo Module 및 Migration | 기존 Repo와 Migration 사용 | Owner에게 확인 | Data 접근 방식을 지어내는 것 차단 |
| project-shape | Umbrella를 뜻하는 `apps/` 디렉터리의 존재 여부 | 그 구조를 따름 | Owner에게 확인 | 구조 재편 차단 |
| asset-pipeline | `mix.exs`와 `config`에 설정된 Asset 도구 | 그것을 사용 | Owner에게 확인 | Bundler를 새로 들이는 것 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서 다시
언급되어야 합니다. 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수 있어야 하기 때문입니다.
