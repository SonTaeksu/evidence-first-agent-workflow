# Pitfall — Next.js

여기 있는 것은 모두 기술 자체의 속성이며 어떤 Project와도 무관하게 검증할 수 있습니다.
한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, Error Message가 원인이 아닌
다른 것을 가리킨다는 점입니다.** 실패가 스스로 드러나는 Stack에는 이런 목록이 필요 없습니다.

## Client 경계는 전이된다

`'use client'`는 그 Module과 그것이 Import하는 모든 것에 적용됩니다. Directive 하나가 큰 하위 Tree를 Client Bundle로 끌어올 수 있고, 유일한 증상은 Bundle 크기입니다.

## 직렬화되지 않는 Props

Server Component에서 Client Component로 Callback을 넘기면 Render 시점에 실패하는데, Message는 Callback이 아니라 직렬화를 이야기합니다.

## Caching 기본값은 Version마다 다르다

`fetch`가 기본으로 Caching되는지, Route가 Static인지 Dynamic인지 판정하는 방식은 Major Version 사이에 바뀌었습니다. 잘못된 Version의 문서에서 얻은 답은 오직 Production에서만 조용히 틀립니다.

## Client Code의 환경 변수

접두사가 없는 변수를 Browser에서 읽으면 `undefined`입니다. 이를 Falsy한 설정 값으로 취급하는 Code는 조용히 잘못된 분기를 탑니다.

## Middleware Runtime

Node API가 Middleware에서 전부 쓸 수 있는 것은 아닙니다. 실패는 Build가 아니라 Deploy 시점이나 요청 시점에 나타납니다.
