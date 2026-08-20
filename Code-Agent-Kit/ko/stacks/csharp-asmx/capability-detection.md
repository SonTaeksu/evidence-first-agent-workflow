# Capability Detection — ASMX Web Service 2.0 (.NET Framework 4+)

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결론에 이르지 못할 때 적용되는 것이 Unknown Rule이고, 이 Rule은 추측하는 대신
차단합니다. 잘못된 추측 하나가 멈춰 서는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| soap-version | `Web.config`의 Protocol 구성과 생성된 WSDL | 구성된 Version을 유지 | Owner에게 확인 | Contract 표면 변경 차단 |
| proxy-generation | `wsdl.exe` 단계 또는 Web Reference 폴더 | 다시 생성하고 Wrapper에서 조정 | 이유를 기록한 손으로 쓴 Client | Contract를 새로 만드는 것 차단 |
| authentication | IIS와 `Web.config`의 인증 구성 | 구성된 방식에 맞춰 통합 | Owner에게 Escalation | 보안 관련 변경 차단 |
| external-consumers | Owner의 진술, 그리고 공개된 WSDL | Contract를 동결된 것으로 보고 추가 방식으로 Version을 올림 | Owner가 Consumer 없음을 확인하면 그 자리에서 변경 | 모든 Breaking Change 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서
다시 밝혀야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 택했고 왜 그랬는지 알 수
있습니다.
