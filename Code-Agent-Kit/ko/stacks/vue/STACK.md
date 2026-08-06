# Stack Profile — Vue.js

Vue로 만드는 Single-page UI 또는 내장 UI. Major Version이 곧 단단한 경계입니다.

## Runtime 및 Framework Version

`⟨확인 필요: exact versions, read from this project's manifests and
from the toolchain on the machine that runs validation⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참조하십시오.

## 디렉터리 구조

- `src/main.*` — Application 진입점과 Plugin 등록.
- `src/components/*.vue` — Single-file Component: Template, Script, Style.
- `src/router`, `src/stores` — 해당 Capability가 present일 때만 존재합니다.
- `vite.config.*` 또는 설정된 Bundler의 Config — Build Contract.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 성질이며 Project와 무관하게 성립합니다.

- Vue 2와 Vue 3는 Reactivity 구현, Component API, Template 규칙이 다릅니다. 모든 답을 Major Version이 좌우합니다.
- Vue 3의 Reactivity는 Proxy 기반이라 Proxy 객체에 대한 Property 접근을 추적합니다. Proxy 밖으로 꺼낸 값은 더 이상 Reactive하지 않습니다.
- `<script setup>`은 `setup()`과 다르게 Compile됩니다 — Binding이 자동으로 노출되고 File의 Top-level 규칙도 다릅니다.
- Scoped Style은 Attribute Selector로 Compile되며, 자식 Component 내부까지 격리하지는 않습니다.
