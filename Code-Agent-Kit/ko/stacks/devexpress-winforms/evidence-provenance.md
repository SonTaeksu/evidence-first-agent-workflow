# Evidence Provenance — DevExpress WinForms

이 Stack에서 쓰는 모든 Fact는 출처를 댈 수 있어야 합니다. 아래 순서는 주장을 얼마나
신뢰할 수 있는지에 따른 것입니다.

1. **이 Project의 Code, Project File, Package 또는 Lock File.** 참조된 범위가 아니라 해석된
   DevExpress Version입니다.
2. **명령의 Exit Code.** 실행한 명령과 그것을 실행한 Machine을 함께 기록하며, 이 Stack에서는
   *어느* Machine인지가 중요합니다. License가 개발자 Machine과 Build Agent 사이에서 다르기
   때문입니다.
3. **MCP를 통한 `dxdocs24_2`(또는 `dxdocs`).** DevExpress Type에 관한 모든 것에 사용합니다.
   당연해 보이는 것까지 포함해 언제나 그렇습니다.
4. **MCP를 통한 `microsoft-learn`.** 그 아래의 Windows Forms 및 .NET Layer에 사용하며,
   DevExpress에 대해서는 아무것에도 쓰지 않습니다.
5. **공식 DevExpress Release Note.** Version 사이에 바뀐 동작에 사용합니다.
6. **모델 기억** — 마지막이며, Version에 민감한 Fact나 Member 이름에는 절대 쓰지 않습니다.

## 답이 어느 Version에서 왔는지가 답의 일부입니다

Version이 없는 DevExpress Fact는 Fact가 아닙니다. 조회를 어느 Release에 고정했는지를 주장과
함께 기록합니다. 고정된 Project에서 고정되지 않은 Endpoint로 얻은 답은 그렇다고 기록합니다.
나중에 틀린 것으로 드러날 가능성이 가장 큰 경우이기 때문입니다.

## Fact 기록

`references/verified-facts.md`의 항목은 Fact, 그것을 확인한 곳, 확인한 시점을 밝힙니다.
Source가 없는 항목은 기억일 뿐이므로 남기지 않고 삭제합니다.

## Source가 서로 어긋날 때

멈추고 그 불일치를 보고합니다. 문서에 우연히 보이는 Version에 맞춰 구현하지 않으며, 같은
Server에 대한 두 서술이 충돌할 때 더 자세한 쪽을 골라 해결하지도 않습니다 — 그 실수를
거절한 실제 사례는 `mcp/source-routing.md`의 Tool Parameter 대목에 있습니다. 해결되지 않은
항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
