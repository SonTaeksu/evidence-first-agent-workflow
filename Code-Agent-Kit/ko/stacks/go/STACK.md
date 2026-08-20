# Stack Profile — Go

표준 Toolchain으로 만드는 Go Service와 Command-line Tool.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을
실행하는 장비의 Toolchain에서 읽습니다⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## Directory 구조

- `go.mod` — Module 경로와 `go` Directive. 둘 다 Contract입니다.
- `cmd/*` — 관례상 Binary 하나당 Directory 하나.
- `internal/*` — 이 Module 안에서만 Import할 수 있고, Compiler가 강제합니다.
- `*_test.go` — 표준 Test Tooling. Runner를 고를 필요가 없습니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 성질이므로 Project와 무관하게 성립합니다.

- `go.mod`의 `go` Directive가 언어 의미론을 선택하며, 그중 하나는 1.22에서 눈에 보이게 바뀌었습니다(Loop 변수 Scope).
- `internal/`은 관례가 아니라 Compiler가 강제하는 경계입니다.
- Build Tag와 `GOOS`/`GOARCH`는 서로 다른 Compilation Unit을 만듭니다. 어떤 File은 Build에서 빠진 채 한 번도 검사되지 않을 수 있습니다.
- nil Pointer를 담은 Interface 값은 nil이 아닙니다. 이것은 Bug가 아니라 언어 규칙입니다.
