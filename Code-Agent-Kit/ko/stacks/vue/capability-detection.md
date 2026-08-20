# Capability Detection — Vue.js

Capability는 Repository에서 Detection하며 가정하지 않습니다. Detection이 불확실하면 Unknown Rule이
적용되어 추측 대신 차단합니다. 잘못된 추측 하나의 비용이 잠시 멈추는 비용보다 큽니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| major-version | Lock File의 `vue` Entry — 범위를 적을 수 있는 `package.json`이 아님 | 그 Version의 규칙 안에서 답한다 | Owner에게 확인한다 | Version 민감 API 사용을 모두 차단 |
| build-tool | Bundler Config File과 Package Script | 설정된 Build를 사용한다 | Owner에게 확인한다 | Build 구성 변경을 차단 |
| state-management | 의존성의 Store Package와 Store 디렉터리 | 기존 Store를 사용한다 | Component 지역 State | Store Library 도입을 차단 |
| test-runner | devDependencies의 Runner와 Test Script | 설정된 Runner를 실행한다 | Runner가 없다고 보고한다 | Test 통과 주장을 차단 |
| typescript | `tsconfig`와 Component의 `lang="ts"` | Type을 유지한다 | 평범한 JavaScript를 유지한다 | 언어가 섞이는 변경을 차단 |

Feature가 의존하는 Capability는 Project Map에 나타나고 Gate Analysis에서 반복되어야 합니다. 나중에
읽는 사람이 어느 갈래를 왜 택했는지 알 수 있어야 합니다.
