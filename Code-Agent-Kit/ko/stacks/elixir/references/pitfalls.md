# Pitfall — Elixir

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

## Socket State에 쌓이는 Assign

LiveView Socket에 Assign한 것은 접속한 사용자마다 그대로 붙들려 있습니다. 큰 Assign은 메모리 누수이며, 동시 접속에서만 드러나고 개발 중에는 결코 보이지 않습니다.

## Compile 시점 설정과 Runtime 설정

`config/config.exs`에서 환경 변수를 읽으면 Build Machine의 값이 Release 안에 박힙니다. 개발 중에는 동작하고, 잘못된 값이 그대로 배포됩니다.

## Ecto의 Preload와 N+1

Load되지 않은 Association에 접근하면 Lazy Loading이 아니라 예외가 나며, 그것이 안전한 동작입니다. 하지만 Loop 안에서 Preload하면 행마다 Query 하나씩 나가면서 오류는 전혀 나지 않습니다.

## Changeset Validation은 Database 제약이 아니다

Changeset 검사는 동시에 들어오는 Insert가 유일성을 깨뜨리는 것을 막지 못합니다. 대응하는 Database 제약이 필요하고, 그 오류도 처리해야 합니다.

## 한계 없는 Mailbox

처리하는 속도보다 빠르게 받는 Process는 Node가 죽을 때까지 Mailbox를 키웁니다. 증상은 오류가 아니라 메모리입니다.
