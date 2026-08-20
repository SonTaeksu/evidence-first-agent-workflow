# Evidence Provenance — Vue.js

이 Stack의 모든 Fact는 출처를 댈 수 있어야 합니다. 아래 순서는 주장의 신뢰도 순입니다.

1. **이 Project의 Code와 Manifest.** Version 범위가 아니라 Lock File.
2. **명령의 Exit Code.** 명령과 실행 장비를 함께 기록합니다.
3. **MCP를 통한 `context7`.** Version 민감 항목 전부.
4. **공식 Release Notes.** Version 사이에 달라진 동작.
5. **Model Memory** — 마지막이며, Version 민감 Fact에는 쓰지 않습니다.

## Fact 기록

`references/verified-facts.md`의 항목은 Fact, 검증 위치, 시점을 적습니다. 출처 없는 항목은 기억이며
보관하지 않고 삭제합니다.

## Source가 어긋날 때

멈추고 불일치를 보고합니다. 문서가 우연히 보여 준 Version을 대상으로 구현하지 않습니다. 미해결
항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
