# Capability Detection — WCF (.NET Framework 4.7.2+)

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결론에 이르지 못할 때 적용되는 것이 Unknown Rule이고, 이 Rule은 추측하는 대신
차단합니다. 잘못된 추측 하나가 멈춰 서는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| transport-binding | Service 구성의 `<bindings>` | 구성된 binding을 그대로 사용 | binding을 추가하기 전에 Owner에게 확인 | endpoint 변경 차단 |
| security-mode | binding의 `security` Element와 Credential 구성 | 구성된 Mode를 유지 | Owner에게 Escalation | Authentication이나 전송 보안을 건드리는 모든 변경 차단 |
| generated-proxy | Service Reference 폴더 또는 Build 안의 `svcutil` 호출 | 다시 생성하고 Wrapper에서 조정 | 이유를 기록한 수기 작성 Contract Client | Contract를 새로 지어내는 것 차단 |
| hosting-model | `.svc` File과 IIS 구성, 또는 Self-host 진입점 | 기존 Model을 따름 | Owner에게 확인 | Hosting 변경 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서
다시 밝혀야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 택했고 왜 그랬는지 알 수
있습니다.
