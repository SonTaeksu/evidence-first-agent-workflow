# Pitfall — Rust

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

## Runtime 불일치

한 Runtime을 위해 쓰인 Library를 다른 Runtime 아래에서 쓰면 Compile은 되고, 첫 IO에서 Reactor가 없다는 Message와 함께 Panic이 납니다. Code 오류가 아니라 의존성 선택 오류입니다.

## Feature 통합이 부르는 뜻밖의 결과

Workspace Build는 Feature의 합집합을 켭니다. Member 하나만 Build할 때와 Workspace를 Build할 때 동작이 달라지고, 그래서 간헐적인 문제처럼 보입니다.

## Async 안에서의 Blocking

Async Task 안의 동기 호출은 Executor Thread를 멈춰 세웁니다. 오류 하나 없이 처리량이 무너집니다.

## 일관되지 않게 고른 Error Model

경계를 사이에 두고 Type이 있는 Error Crate와 동적인 Error Crate를 섞으면, Caller가 분기하는 데 필요했던 Type 정보가 사라집니다.

## MSRV는 설치된 Toolchain이 아니다

Local에서 Compile되는 Code가 최소 지원 Version에서는 실패할 수 있습니다. 선언된 MSRV가 Contract이고, Local Compiler는 아닙니다.
