# React 및 ASP.NET Core 검증 Pitfall

| 잘못된 가정 | 검증 Rule | Evidence | 실패 Stage |
|---|---|---|---|
| Frontend와 Backend Contract를 독립 변경 가능 | 두 Contract와 Test를 함께 갱신 | Sample API 및 Test | runtime |
| 두 번째 HTTP Client 추가는 무해 | Detection된 Project API Entry Point 재사용 | `frontend/src/api.ts` | architecture |
| Build PASS가 UI 충실도를 증명 | Screen, Color, E2E Gate 별도 실행 | Workflow Tool | rendered/runtime |
| Sample In-memory Repository가 Production Data Policy | Database 적용 전 Owner 확인 필요 | Capability Rule | architecture |
