# React 및 ASP.NET Core Communication Contract

- Frontend Server Call은 `frontend/src/api.ts`를 통합니다.
- Request/Response TypeScript Type은 Backend DTO 또는 Endpoint Payload와 동기화합니다.
- 공개 Sample은 JSON REST를 사용합니다.
- Backend Validation Error는 기존 Endpoint Error Shape를 사용합니다.
- Contract 변경 시 Frontend Type, Backend Payload, Component Test, API Test, E2E를 함께 갱신합니다.
- Generated Client는 Capability Detection으로 Ownership와 Regeneration 명령을 확인한 경우에만 Manual Adapter를 대체합니다.
