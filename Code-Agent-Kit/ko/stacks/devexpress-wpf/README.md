# DevExpress WPF (v24.2+)

WPF Application 안에서 동작하는 DevExpress WPF Control이며 v24.2 이상입니다.

**이 Profile은 [`../csharp-wpf`](../csharp-wpf)를 대체하는 것이 아니라 함께 쓰는
짝입니다.** 그 Profile의 내용은 모두 그대로 성립합니다. XAML은 BAML로 Compile되고,
실패한 Binding은 아무것도 던지지 않으며, UI Thread는 STA여야 하고, Dispatcher 밖에서
바뀐 Collection은 Exception이 아니라 Race입니다. 이 Profile은 평범한 WPF와 MVVM 위에
DevExpress가 바꾸는 것만 더합니다. 둘 다 읽으십시오. 평범한 WPF Fact를 두고 둘이
어긋나 보이면 맞는 쪽은 `csharp-wpf`입니다. 이 문서는 Framework에 대해 아무런 권위가
없습니다.

**적용 범위는 v24.2 이상이고, 그 경계는 임의로 정한 것이 아닙니다.** DevExpress 문서
MCP Server는 v24.2보다 이른 Version 고정을 지원하지 않으므로, 그 아래에서는 Project가
실제로 돌리는 Version에 맞춰 조회가 답하게 만들 문서화된 방법이 없습니다. 자기 문서를
고정하지 못하는 Profile은 기억으로 답하는 Profile이고, 그것이 바로 이 Kit이 막으려고
존재하는 것입니다.

**상태: `blocked`.** 고장 난 것이 아니라 대기 중입니다. `STACK-INPUTS.md`의 Owner
입력이 답변되지 않아 `check-stack-readiness`가 `blocked`를 도출하고, `tools/check-last`는
그 상태의 Stack을 의도적으로 건너뜁니다. Placeholder 때문에 매 실행마다 거짓 경보가
나지 않도록 하기 위해서입니다.

이미 들어 있고 쓸모 있는 것:

- `references/pitfalls.md` — 이 Stack에서 Error Message 없이 일어나는 실패;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 알아내는 방법;
- `mcp/source-routing.md` — 어떤 문서 Source가 권위 있고, 어떤 것을 참조하면 안 되며,
  DevExpress Server에 대해 무엇이 확인되지 *않았는지*.

`ready`에 도달하려면 실제로 존재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는
선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
