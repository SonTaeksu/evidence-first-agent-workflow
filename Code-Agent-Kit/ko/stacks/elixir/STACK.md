# Stack Profile — Elixir

Elixir Application이며 대개 Phoenix를 씁니다. Process와 Supervision 구조는 구현 세부가 아니라 설계의 일부입니다.

## Runtime과 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는
Machine의 Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고하십시오.

## 디렉터리 구조

- `mix.exs` — Application, Elixir 요구 Version, 의존성, 그리고 Release 설정.
- `mix.lock` — 해석된 Version에 대한 권위 있는 근거.
- `lib/<app>/`와 `lib/<app>_web/` — Domain과 Web을 나누는 Phoenix의 관례.
- `config/*.exs` — Compile 시점 설정과 Runtime 설정은 서로 다른 File이고, 무엇을 읽을 수 있는지도 다릅니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

이것들은 기술 자체의 속성이며 Project와 무관하게 성립합니다.

- Elixir, OTP, Phoenix, LiveView의 Version은 서로 별개인 네 가지 제약이며 어느 하나가 다른 하나를 함의하지 않습니다.
- `config/runtime.exs`는 Boot 시점에 실행되고, 나머지 Config File은 Compile 시점에 실행되어 Runtime 환경을 읽을 수 없습니다.
- LiveView의 State는 Server의 Socket에 있습니다. 모든 Assign은 그 Session이 사는 동안 붙들고 있는 메모리입니다.
- Supervision 전략이 하나의 Crash가 무엇까지 무너뜨리는지를 결정합니다. 겉으로 드러나는 동작을 가진 설계 결정입니다.
- Umbrella Project와 단일 Application은 의존성 해석 방식과 Release 배치가 다릅니다.
