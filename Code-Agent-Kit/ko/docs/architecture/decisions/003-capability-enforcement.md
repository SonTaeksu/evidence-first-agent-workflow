# ADR-003: 3층 Capability 강제

- 상태: accepted

## 결정

구현 방식을 바꾸는 Capability는 Project Map에 기록하고, Gate Analysis에서 다시 출력하며, Stack 금지 규칙으로 강제합니다.

## 버린 대안

문서 한 곳의 수동 안내.

## 이유

소형 모델은 한 지시를 놓칠 수 있습니다. 세 Checkpoint는 사용할 수 없는 Shared Library, Generated Client, SDK 기능, Runtime 경로를 실수로 사용하는 것을 줄입니다.
