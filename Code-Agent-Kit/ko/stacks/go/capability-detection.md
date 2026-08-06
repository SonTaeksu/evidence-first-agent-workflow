# Capability Detection — Go

Capability는 Repository에서 Detection하며, 절대 가정하지 않습니다. Detection이
분명하지 않을 때 적용되는 것이 Unknown Rule이고, 이 규칙은 추측하는 대신
차단합니다. 잘못된 추측 하나의 비용이 잠깐 멈추는 비용보다 큽니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| language-version | `go.mod`의 `go` Directive, 그리고 Validation 장비의 `go version` | 그 안에서 답을 찾음 | Owner에게 확인 | 1.22의 Loop 변수 변경에 민감한 모든 것을 차단 |
| http-router | `go.mod`의 Router Package, 또는 `net/http` 사용 | 그것을 사용 | 사유를 기록하고 `net/http` 사용 | Router 도입을 차단 |
| data-access | Driver나 Query Builder 요구사항과 그 연결 코드 | 기존 Layer를 사용 | Owner에게 확인 | Data Access를 지어내는 것을 차단 |
| logging | Logging Package, 또는 `log/slog` 사용 | 기존 Logger를 사용 | 사유를 기록하고 `log/slog` 사용 | Logger 도입을 차단 |

Feature가 의존하는 Capability는 모두 Project Map에 나타나야 하고 Gate Analysis에서
다시 언급해야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수
있습니다.
