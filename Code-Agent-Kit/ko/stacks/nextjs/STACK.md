# Stack Profile — Next.js

Next.js 위에서 동작하는 React Application입니다. Router Mode와 Server/Client 경계가 거의 모든 답을 좌우합니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

- `app/` 또는 `pages/` — 둘 중 어느 쪽이 있는지가 Routing과 Data Model을 결정합니다. 둘 다 있을 수도 있으며, 그때는 Route별로 동작이 달라집니다.
- `app/**/layout.*`, `page.*`, `route.*` — App Router의 Segment File이며 각각 규칙이 다릅니다.
- `next.config.*` — Output Mode, Redirect, Image, Bundler 설정.
- `middleware.*` — Node보다 API 표면이 좁은 제한된 Runtime에서 실행됩니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다.

- App Router에서는 Server Component가 기본입니다. `'use client'`가 경계를 표시하고, 그 아래는 전부 Client Code입니다.
- Server에서 Client 경계를 넘는 Props는 직렬화할 수 있어야 합니다. 함수나 Class Instance는 Render 시점에 실패합니다.
- Caching과 Revalidation 기본값은 Major Version마다 바뀌었습니다. 기준은 설치된 Version이며 기억에 의존하지 않습니다.
- `NEXT_PUBLIC_` 접두사가 붙은 환경 변수만 Browser에 도달합니다. 나머지는 빈 값이 아니라 undefined입니다.
- `output: 'export'`는 Server 기능을 전부 제거합니다. 개발 중에는 동작하던 Code가 Export에서 실패합니다.
