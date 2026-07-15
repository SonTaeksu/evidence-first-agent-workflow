# Capability Detection

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| shared-api-client | File/Import/Config Evidence | 기존 사용 | 승인된 Stack Adapter 사용 | 구현 차단 |
| generated-client | Generated Folder/Build Metadata | Generated Client 사용 | 승인된 Manual Contract | Contract 환각 차단 |
| authentication-provider | Config 및 Middleware Evidence | 기존 Provider 통합 | 승인된 Default | Security 변경 차단 |
| runtime-sdk-version | Manifest/Tool Output | Detection Version 사용 | 확인된 지원 Version 사용 | Version 민감 API 차단 |

Feature가 사용하는 모든 Capability는 Project Map에 기록하고 Gate Analysis에서 다시 출력합니다.
