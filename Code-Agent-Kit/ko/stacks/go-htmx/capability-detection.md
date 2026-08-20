# Capability Detection — Go + HTMX

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결론에 이르지 못할 때 적용되는 것이 Unknown Rule이고, 이 Rule은 추측하는 대신
차단합니다. 잘못된 추측 하나가 멈춰 서는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| language-version | `go.mod`의 `go` Directive와 `go version` | 그 안에서 해결 | Owner에게 확인 | Loop 변수에 민감한 작업 차단 |
| htmx-version | Script Tag 또는 Vendoring된 Asset | 그 안에서 해결 | Owner에게 확인 | Attribute 동작에 대한 가정 차단 |
| template-engine | `html/template` 사용 또는 `go.mod`의 다른 Engine | 그대로 사용 | Owner에게 확인 | Engine 도입 차단 |
| fragment-convention | `HX-Request`로 분기하는 기존 Handler | 이미 정착된 관례를 따름 | Owner에게 관례 확인 | Fragment Protocol을 새로 만드는 것 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서
다시 밝혀야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 택했고 왜 그랬는지 알 수
있습니다.
