# WPF (.NET Framework 4.7.2+)

WPF 위에서 동작하는 Desktop UI이며 .NET Framework 4.7.2 이상을 Target합니다.

**상태: `blocked`.** 고장 난 것이 아니라 대기 중입니다. `STACK-INPUTS.md`의 Owner 입력이
답변되지 않아 `check-stack-readiness`가 `blocked`를 도출하고, `tools/check-last`는 그 상태의
Stack을 의도적으로 건너뜁니다. Placeholder 때문에 매 실행마다 거짓 경보가 나지 않도록
하기 위해서입니다.

이미 들어 있고 쓸모 있는 것:

- `references/pitfalls.md` — 이 Stack에서 Error Message 없이 일어나는 실패;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 알아내는 방법;
- `mcp/source-routing.md` — 어떤 문서 Source가 권위 있고 어떤 것을 참조하면 안 되는지.

`ready`에 도달하려면 실제로 존재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는
선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
