# Pitfalls — Go

여기 있는 항목은 모두 기술 자체의 성질이며, 어떤 Project와도 무관하게 확인할 수
있습니다. 한데 모은 이유는 한 가지 공통점 때문입니다. **실패가 조용하거나, Error
메시지가 원인이 아닌 다른 것을 가리킵니다.** 실패가 스스로 드러나는 Stack이라면
이런 목록은 필요 없습니다.

## 1.22 이전의 Loop 변수 Capture

Loop 변수를 Closure로 잡은 Goroutine은 `go` Directive가 1.22 미만이면 마지막 값을 보고, 1.22부터는 반복마다 복사된 값을 봅니다. 같은 소스가 두 가지로 동작하고, 어느 쪽인지는 Directive가 정합니다.

## nil Interface와 nil Pointer

nil인 `*T`를 `error`로 반환하면 `err != nil`이 참이 됩니다. 검사 코드는 멀쩡해 보이고 언제나 통과합니다.

## append에서의 Slice Aliasing

`append`는 Backing Array를 재사용할 수 있어서, 두 Slice가 저장 공간을 공유하며 서로를 바꿔 놓을 수 있습니다. Error는 없고, 값이 어딘가에서 바뀔 뿐입니다.

## 전파되지 않는 Context 취소

Context를 무시하는 호출은 Caller가 포기한 뒤에도 계속 돌아갑니다. 증상은 실패가 아니라 부하입니다.

## Error Wrapping

`%w` 없는 `fmt.Errorf`는 `errors.Is`와 `errors.As`를 깨뜨립니다. Chain이 거기서 조용히 끊깁니다.
