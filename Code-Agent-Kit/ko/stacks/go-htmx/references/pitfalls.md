# Pitfall — Go + HTMX

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

## Swap 대상 불일치는 조용하다

`hx-target` Selector가 틀렸거나 Fragment의 Root Element id가 다르면 Console 오류도 Server 오류도 나지 않습니다. Page가 그냥 갱신되지 않습니다. 200이 아니라 Rendering된 Fragment를 Assert하십시오.

## Fragment Request에 전체 Page를 반환하기

문서 전체가 `div` 안으로 Swap됩니다. 대개 얼추 맞아 보이는데, 그것이 실패보다 더 나쁩니다.

## HTMX가 특별하게 다루는 응답 Code

일부 Status Code는 Swap 자체를 막습니다. Code로 오류를 알리면서 Markup도 함께 반환하는 Handler는 그 Markup이 버려질 수 있습니다.

## hx-post의 CSRF

HTMX Request도 평범한 Request이며 Form Post와 똑같은 Token이 필요합니다. 빠뜨리면 Middleware에서 실패하는데, 사용자에게는 아무것도 알려 주지 않습니다.

## HTMX Version은 Client측에 고정된다

Attribute 동작은 HTMX Major Version 사이에 다르고, 그 Version은 `go.mod`가 아니라 Script Tag에 있습니다. Asset에서 읽으십시오.
