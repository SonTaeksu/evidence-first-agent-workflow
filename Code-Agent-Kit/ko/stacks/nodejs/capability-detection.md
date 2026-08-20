# Capability Detection — Node.js

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결정적이지 않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다.
잘못된 추측 하나가 잠시 멈추는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| module-system | `package.json`의 `type`과 실제로 쓰는 확장자 | 일관되게 따름 | Owner에게 확인 | 다른 System의 Module 추가 차단 |
| runtime-version | Validation Machine의 `node --version`과 Lock File | 그 Version 안에서 답함 | Owner에게 확인 | Version 민감 API 사용 차단 |
| http-framework | Dependency에 있는 Framework와 그 배선 | 그것을 사용 | 사유를 기록하고 `node:http`를 직접 사용 | Framework 도입 차단 |
| test-runner | devDependencies의 Runner 또는 `node:test` 사용 | 설정된 Runner 실행 | 없다고 보고 | Test 통과 주장 차단 |
| typescript | `tsconfig`와 Build 또는 Loader 단계 | Type과 Build 단계 유지 | 순수 JavaScript | 혼합 언어 변경 차단 |

Feature가 의존하는 Capability는 모두 Project Map에 나타나고 Gate Analysis에서
반복되어야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 왜 골랐는지 볼 수 있습니다.
