# Stack Profile — Node.js

Node에서 도는 Server-side 또는 CLI JavaScript입니다. 가장 먼저 확정할 것은 Module System이고, 이것이 대부분의 질문에 대한 답을 바꿉니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을
실행하는 Machine의 Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 보십시오.

## 디렉터리 구조

- `package.json` — `type`, `engines`, `exports`, `scripts`는 모두 Contract입니다.
- `src/` 또는 `main`/`exports`가 가리키는 Entry — Module Graph의 Root입니다.
- Lock File — 설치된 Version에 대한 유일한 권위입니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

아래는 기술 자체의 성질이며 Project와 무관하게 성립합니다.

- `"type": "module"`은 Package 전체를 ESM으로 바꿉니다. 이것이 없으면 `.js`는 CommonJS이고 `import` 구문은 Parse Error입니다.
- ESM에는 `__dirname`과 `__filename`이 없습니다. `import.meta.url`이 그 자리를 대신합니다.
- Top-level `await`는 ESM에서만 쓸 수 있습니다.
- `exports` Field는 한번 존재하는 순간, File이 Disk에 실제로 있어도 Deep Import를 실패하게 만듭니다.
- 처리되지 않은 Promise Rejection의 동작, 그리고 어떤 API가 안정적인지는 둘 다 Major Version에 달려 있습니다. `engines` Field는 의도를 적은 것이지 Fact가 아닙니다.
