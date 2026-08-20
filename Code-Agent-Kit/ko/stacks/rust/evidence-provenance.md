# Evidence Provenance — Rust

이 Stack에서 쓰는 모든 Fact는 출처를 댈 수 있어야 합니다. 아래 순서는 주장을 얼마나
믿을 수 있는지를 기준으로 합니다.

1. **이 Project의 Code와 Manifest.** Version 범위가 아니라 Lock File.
2. **명령의 Exit Code.** 실행한 명령과 실행한 Machine을 함께 기록합니다.
3. **MCP를 통한 `context7`.** Version에 민감한 모든 것.
4. **공식 Release Notes.** Version 사이에 달라진 동작.
5. **Model의 기억** — 마지막이며, Version에 민감한 Fact에는 절대 쓰지 않습니다.

## Fact 기록하기

`references/verified-facts.md`의 항목은 Fact, 그것을 확인한 곳, 확인한 시점을
적습니다. 출처가 없는 항목은 기억이므로, 남기지 않고 지웁니다.

## Source가 서로 어긋날 때

멈추고 그 불일치를 보고합니다. 문서가 우연히 보여 준 Version을 대상으로 구현하지
않습니다. 해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
