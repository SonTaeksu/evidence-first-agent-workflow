# React 및 ASP.NET Core Capability Detection

| Capability | Sample Evidence | 상태 | 선택 경로 | Unknown Rule |
|---|---|---|---|---|
| frontend-shared-api-client | `frontend/src/api.ts` | present | 기존 Module 재사용 | 두 번째 Client 생성 금지 |
| generated-openapi-client | Sample에 Generated Client 없음 | absent | Typed Manual Adapter | Generated Ownership 환각 금지 |
| backend-style | `Program.cs`의 Minimal API Endpoint | present | Minimal API 유지 | Style 변환 차단 |
| data-access | In-memory Repository | present | Sample Repository 유지 | Database 도입 전 Owner 결정 필요 |
| authentication-provider | 공개 Sample에 Auth 없음 | not-applicable | Auth 변경 없음 | Auth 가정 차단 |
| design-system | Local CSS만 사용 | absent | Local Component 유지 | Library 추가 전 Owner 확인 |
| sdk-version | `global.json`, `package.json`, `.csproj` | present | Detection Version 사용 | File 불일치 시 Version 민감 API 차단 |

다른 Project에 적용할 때는 해당 Project Evidence로 Decision을 다시 생성해야 합니다.
