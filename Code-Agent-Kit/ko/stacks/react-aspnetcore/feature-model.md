# React 및 ASP.NET Core Feature Model

- Feature 단위: Frontend 동작, API Contract, Backend 구현, Test를 포함한 사용자 Visible Vertical Slice
- Create, List, Status Update, Approve, Reject가 같은 Domain State를 공유하면 한 Feature 안에 둠
- Ownership, Deployment, Security Boundary, 독립 Version Contract가 다르면 별도 Feature
- Feature State는 `docs/features/<feature>.current.md`, History, Active Worklog에 둠
