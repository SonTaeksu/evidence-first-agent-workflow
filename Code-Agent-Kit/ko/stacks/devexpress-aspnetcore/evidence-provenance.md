# Evidence Provenance — DevExpress for ASP.NET Core

이 Stack에서 사용하는 모든 사실은 출처를 밝힐 수 있어야 합니다. 아래 순서는 주장을 얼마나
신뢰할 수 있는지에 따른 것입니다.

1. **이 Project의 Code, Project File, Restore 출력.** Project File의 범위가 아니라 해석된
   Package Version입니다.
2. **명령의 Exit Code**, 그 명령과 그것을 실행한 머신을 함께 기록합니다.
3. DevExpress Component나 Reporting에 관한 모든 것에 대해 **MCP를 통한 `dxdocs`**. v24.2
   Project에서는 최신 Endpoint 대신 고정된 Server를 사용하며, 이유는
   `mcp/source-routing.md`가 설명합니다.
4. ASP.NET Core, EF Core, .NET에 대해 **MCP를 통한 `microsoft-learn`** — 그리고 DevExpress에
   대해서는 사용하지 않습니다.
5. Version 사이에 바뀐 동작에 대해서는 **공식 릴리스 노트**.
6. **모델 기억** — 마지막이며, Version에 민감한 사실에는 절대 쓰지 않습니다.

3과 4의 구분은 선호가 아닙니다. Microsoft Learn에서 답한 DevExpress 질문은 그 아래
Framework에 대한 유창한 답을 내놓고, 그것은 질문에 답한 것처럼 읽히지만 답한 것이
아닙니다.

## 사실 기록하기

`references/verified-facts.md`의 항목은 사실, 어디서 확인되었는지, 그리고 언제인지를
밝힙니다. Source가 없는 항목은 기억이며, 보관하는 대신 제거합니다.

DevExpress 사실의 Source는 도움말 항목입니다. URL을 기록합니다.
`devexpress_docs_get_content`가 URL을 받으므로 나중에 읽는 사람이 동일한 페이지를 다시
가져올 수 있기 때문입니다. 그 항목이 서술한 Version도 기록합니다. 이 Project와 다를
가능성이 가장 큰 것이 바로 그것이기 때문입니다.

## Source가 서로 어긋날 때

멈추고 그 불일치를 보고합니다. 문서가 마침 보여 준 Version에 맞춰 구현하지 않습니다.
해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.

여기서 예상되는 구체적인 불일치는 문서의 현행 Version과 이 Project의 고정 Version
사이입니다. Endpoint는 고정할 수 있지만 v24.2 이상에서만 가능하므로, 더 오래된 Project
에서는 비교할 고정 Source가 없고 Version에 민감한 모든 답은 근사치가 되는 대신 미해결로
남습니다.
