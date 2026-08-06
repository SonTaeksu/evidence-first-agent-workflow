# Pitfalls — Node.js

아래는 모두 기술 자체의 성질이고 어떤 Project와도 무관하게 검증할 수 있습니다. 한 가지
특징을 공유하기 때문에 모아 두었습니다. **실패가 조용하거나, Error Message가 원인이 아닌
다른 것을 가리킨다는 점입니다.** 실패가 스스로 드러나는 Stack이라면 이런 목록이
필요 없습니다.

## Module System 불일치

ESM 전용 Dependency는 `require`할 수 없고, Error는 원인이 아니라 File 이름을 가리킵니다. 다른 무엇보다 먼저 Module System을 확정하십시오.

## Interop 기본 동작

`import x from 'cjs-package'`는 `module.exports` 객체를 주는데, 기대한 Named Export가 거기에 없을 수 있습니다. CommonJS에서의 Named Import는 정적으로 해석되며 Load 시점에 실패할 수 있습니다.

## `exports`가 실제 File을 가림

`exports`가 선언되고 그 경로가 목록에 없으면, Disk에 있는 경로라도 Import에 실패합니다.

## Handler를 빠져나가는 Async Error

동기 Callback이 와야 할 자리에 넘긴 `async` Callback은 아무 데도 아닌 곳으로 Reject됩니다. Version에 따라 요청이 멈춰 있거나 Process가 종료됩니다.

## 설치 시점과 Runtime 사이의 Version Drift

`engines`는 강제하지 않는 한 권고일 뿐입니다. Manifest의 범위가 아니라 Validation을 실행한 Machine의 실제 `node --version`을 기록하십시오.
