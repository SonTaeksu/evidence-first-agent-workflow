# DevExpress WinForms

Windows Forms Desktop Application 위의 DevExpress Control이며, **v24.2 이상**이 대상입니다.

## `csharp-winforms`의 대체가 아니라 동반 Profile

[`../csharp-winforms`](../csharp-winforms/)의 내용은 전부 그대로 유효합니다. DevExpress
Form도 Windows Forms Form입니다. Designer가 Layout File을 소유하고, Control은 자신을 만든
Thread에 속하며, DPI는 그 Profile이 지정한 곳에서 구성되고, Project Format이 여전히 Build
명령을 결정합니다. 그 Profile을 먼저 읽고 계속 열어 둡니다.

이 Profile은 DevExpress가 그 위에 더하는 것만 담습니다 — Behaviour와 Data가 서로 다른
Object에 사는 Control 계층, Form의 Menu Strip이 아닌 Command 표면, 좌표를 무시하는 Layout
Container, Application 전역 Skin Layer, License File, 그리고 Microsoft Learn이 다루지 않는
문서 Source입니다.

## 왜 v24.2 이상인가

DevExpress 문서 MCP Server는 `?v=` Query Parameter를 통한 Version 고정을 **v24.2**보다
이전 Release에서는 지원하지 않습니다. 그보다 오래된 Release에서는 Project가 실제로 쓰는
Version에 문서 Server를 맞출 지원되는 방법이 없으므로, 모든 Control API 답변이 그때그때의
최신 Release에서 나오게 됩니다 — 이 Kit이 막으려고 존재하는, 자신만만하면서 Version이
어긋난 답변이 바로 그것입니다. 이 Profile의 규칙은 더 오래된 Project에서도 읽을 수 있지만,
Evidence 경로는 거기에 없습니다.

## 상태: `blocked`

고장 난 것이 아니라 대기 중입니다. `STACK-INPUTS.md`의 Owner 입력이 답변되지 않아
`check-stack-readiness`가 `blocked`를 도출하고, `tools/check-last`는 그 상태의 Stack을
의도적으로 건너뜁니다. Placeholder 때문에 매 실행마다 거짓 경보가 나지 않도록 하기
위해서입니다.

이미 들어 있고 쓸모 있는 것:

- `mcp/source-routing.md` — DevExpress 문서 Server, 그것에 관해 문서화된 내용, 그리고 이
  환경에서 **검증하지 않은** 것;
- `references/pitfalls.md` — 이 Stack에서 Error Message 없이 일어나는 실패;
- `references/verified-facts.md` — 문서화된 Endpoint Fact와 그 날짜;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 알아내는 방법.

`ready`에 도달하려면 실제로 존재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는
선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
