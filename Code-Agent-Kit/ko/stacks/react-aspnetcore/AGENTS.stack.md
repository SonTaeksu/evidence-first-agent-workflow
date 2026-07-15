# React 및 ASP.NET Core Agent Rule

Root `AGENTS.md`를 확장합니다.

- 다른 Project에 이 Profile을 적용하기 전에 Stack Readiness Validation을 실행합니다.
- Detection된 Frontend API Module을 재사용하고 두 번째 Client를 만들지 않습니다.
- Project Map에 다른 Backend Style이 확인되지 않으면 Minimal API를 유지합니다.
- Frontend와 Backend Contract를 동기화합니다.
- Database, Authentication, Generated Client, State Library, Design System Capability가 Unknown이면 도입하지 않습니다.
- Version 민감 .NET 동작은 Microsoft Learn, React 동작은 공식 Source Routing으로 확인합니다.
- Artifact, Rendered Output, Runtime, Color/Accessibility Gate를 별도로 실행합니다.
