# MCP 지식 라우팅

> 어떤 서버가 존재하고, 어떤 것에 실제로 닿았고, 어떤 것은 이름만 적혔는지:
> [`mcp-source-verification.md`](mcp-source-verification.md). 스택 프로파일이
> 라우팅하는 모든 엔드포인트가 실제 `tools/call` 결과와 함께 거기 적혀 있고,
> 시험되지 않은 것은 분리해 표시했습니다. 아무도 연결해 본 적 없는 서버는 지어낸
> 것과 똑같이 읽히므로, 그 구분은 기억이 아니라 문서에 둡니다.

## 출처 우선순위

1. 현재 프로젝트 코드와 생성 산출물
2. 결정론적 빌드, 테스트, 실행 증거
3. MCP로 조회한 공식 문서
4. 공식 저장소와 릴리스 노트
5. 모델 내부 지식

## Microsoft 기술

다음 항목은 Microsoft Learn MCP를 사용합니다.

- ASP.NET Core
- C#
- .NET
- Dependency Injection
- Configuration과 Logging
- Authentication과 Authorization
- 이후 추가할 경우 Entity Framework Core

엔드포인트:

```text
https://learn.microsoft.com/api/mcp
```

## React 생태계

Context7을 사용합니다. React Core 요청은 다음 라이브러리 ID로 고정합니다.

```text
/facebook/react
```

다음 문서를 사용하기 전에 정확한 Context7 라이브러리 ID를 확인합니다.

- Vite
- Vitest
- React Testing Library
- Playwright
- 이후 추가할 경우 React Router

## 대체 정책

MCP를 사용할 수 없다면:

1. 로컬 프로젝트 코드와 Lock 파일을 확인합니다.
2. 공식 출처만 사용합니다.
3. 버전별 확인이 필요한 내용을 검증할 수 없다면 `knowledge unavailable`을 보고하고 중단합니다.
4. 공식 문서 조회를 모델 기억으로 몰래 대체하지 않습니다.
