# Evidence Provenance — DevExpress WPF (v24.2+)

이 Stack에서 쓰는 모든 Fact는 출처를 댈 수 있어야 합니다. 아래 순서는 주장을 얼마나
신뢰할 수 있는지에 따른 것입니다.

1. **이 Project의 Code와 Manifest.** Version 범위도 아니고 Machine에 설치된 것도 아닌,
   복원이 해석한 DevExpress Version입니다.
2. **명령의 Exit Code.** 실행한 명령과 실행한 Machine을 함께 기록합니다.
3. **MCP를 통한 `dxdocs`.** DevExpress에 관한 모든 것에 사용하며, Project가 고정 가능한
   Release에 있다면 그 Version에 고정합니다.
4. **MCP를 통한 `microsoft-learn` 또는 `wpf-docs`.** 평범한 WPF, XAML, .NET에 관한 것에
   사용합니다. DevExpress Control에는 절대 쓰지 않습니다.
5. **공식 Release Note.** Version 사이에 바뀐 동작에 사용합니다.
6. **모델 기억** — 마지막이며, 어떤 종류의 DevExpress Fact에도 절대 쓰지 않습니다.

기억을 끌어내리는 정도가 `../csharp-wpf`보다 여기서 더 엄격하고, 이유는 구체적입니다.
기억으로 떠올린 DevExpress Member 이름은 대개 실제로도 존재하므로 Code가 Compile되고
잘못은 Review를 통과해 살아남습니다. 기억으로 떠올린 WPF Fact는 요란하게 실패하는 편입니다.
Compile되는 것은 Evidence가 아닙니다.

## Fact 기록

`references/verified-facts.md`의 항목은 Fact, 그것을 확인한 곳, 확인한 시점을 밝힙니다.
DevExpress 항목은 어떤 Version에 대해 확인했는지도 함께 밝힙니다. 그것이 이 Fact들이
달라지는 축이기 때문입니다. 출처가 없는 항목은 기억일 뿐이므로 남기지 않고 삭제합니다.

## Source가 서로 어긋날 때

멈추고 그 불일치를 보고합니다. 문서에 우연히 보이는 Version에 맞춰 구현하지 않습니다.
해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
