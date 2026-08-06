# Stack Profile — Rust

Cargo로 만드는 Rust Service와 도구입니다. Async Runtime과 Error Model은 Code 전반에 스며드는 핵심 선택입니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

- `Cargo.toml` — edition, `rust-version`(MSRV), Feature, Workspace Member.
- `Cargo.lock` — Binary에 대해 해석된 Version의 유일한 권위.
- `src/lib.rs` / `src/main.rs` — Crate Root.
- `tests/` — 별도의 Crate로 Compile되는 통합 Test.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다.

- edition은 언어 규칙을 바꾸고, `rust-version`은 최소 Compiler를 선언합니다. 둘 다 Contract이며 어느 쪽도 설치된 Toolchain이 아닙니다.
- Async Runtime은 구현 세부 사항이 아닙니다. Spawn, Timer, IO Type이 모두 거기서 나오며, 두 Runtime을 일반적으로 섞을 수 없습니다.
- Cargo는 Workspace 전체에서 Feature를 통합하므로, 한 Member에서 Feature를 켜면 다른 Member가 Compile하는 내용이 달라질 수 있습니다.
- `Send`/`Sync` 제약은 호출 그래프를 타고 전파됩니다. `Send`가 아닌 값 하나가 Spawn 전체를 불가능하게 만들 수 있습니다.
