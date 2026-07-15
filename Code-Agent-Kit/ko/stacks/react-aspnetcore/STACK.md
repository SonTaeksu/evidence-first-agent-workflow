# React + ASP.NET Core 스택

## 지원 기준선

- React: 19.2.x
- Vite: 8.x
- TypeScript: 7.x
- Node.js: 22.12 이상
- .NET SDK: 10.x LTS

첫 실행에서 외부 데이터베이스가 필요하지 않도록 샘플은 의도적으로 인메모리 백엔드 Repository를 사용합니다. 영속성은 이후 기능 실험으로 추가할 수 있습니다.

## 아키텍처

```text
frontend/
  React 화면과 API Client

backend/
  ASP.NET Core Minimal API
  Domain Model
  Request DTO
  Repository 추상화

docs/
  current.md
  history.md
  project-map.md
  designs/
  evidence/
```

## 명령

프런트엔드:

```bash
npm install
npm run lint
npm run test
npm run build
npm run e2e
```

백엔드:

```bash
dotnet restore
dotnet build
dotnet test
dotnet run
```
