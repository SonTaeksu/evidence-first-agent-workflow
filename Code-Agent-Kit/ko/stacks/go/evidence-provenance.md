# Evidence Provenance — Go

이 Stack에서 쓰는 모든 사실은 Source를 댈 수 있어야 합니다. 아래 순서는 그 주장을
얼마나 믿을 수 있는지에 따른 것입니다.

1. **이 Project의 코드와 Manifest.** Version 범위가 아니라 Lock File.
2. **명령의 exit code.** 명령과 실행한 장비를 함께 기록합니다.
3. **MCP를 통한 `context7`.** Version에 민감한 모든 것에 사용합니다.
4. **공식 Release Note.** Version 사이에 동작이 바뀐 경우에 사용합니다.
5. **모델 기억** — 마지막이며, Version에 민감한 사실에는 절대 쓰지 않습니다.

## 사실 기록하기

`references/verified-facts.md`의 항목은 사실이 무엇인지, 어디서 확인했는지,
언제 확인했는지를 적습니다. Source가 없는 항목은 기억일 뿐이므로 남기지 않고
지웁니다.

## Source가 서로 다를 때

멈추고 그 불일치를 보고합니다. 문서에 우연히 보인 Version에 맞춰 구현하지 않습니다.
해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
