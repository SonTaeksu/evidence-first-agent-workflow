# Stack Profile — Go + HTMX

Go에서 Server가 HTML을 Rendering하고, 부분 갱신은 HTMX가 맡습니다. Go Profile의 내용이 그대로 적용되며, 여기에 Fragment Contract가 더해집니다.

## Runtime과 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는
Machine의 Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고하십시오.

## 디렉터리 구조

- Template — 전체 Page용 한 벌과 Fragment용 한 벌. Handler가 어느 쪽을 반환하느냐가 핵심 결정입니다.
- Handler — 하나의 Route가 Request에 따라 Page를 반환할 수도 Fragment를 반환할 수도 있습니다.
- 정적 Asset — HTMX Script 자체, Version을 고정한 상태로 둡니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

이것들은 기술 자체의 속성이며 Project와 무관하게 성립합니다.

- `go` Directive Rule을 포함해 Go Stack Profile의 모든 내용이 그대로 적용됩니다.
- Handler는 Page인지 Fragment인지 결정해야 합니다. HTMX는 `HX-Request` Header로 자신을 알립니다.
- Swap 대상은 Client가 지정합니다. 아무것과도 맞지 않는 대상은 **아무 변화도, 아무 오류도 내지 않습니다**.
- `html/template`은 Context에 따라 Escape합니다. Escape는 선택이 아니며 Fragment가 담을 수 있는 내용을 바꿉니다.
