# Node.js

Node에서 도는 Server-side 또는 CLI JavaScript입니다. 가장 먼저 확정할 것은 Module System이고, 이것이 대부분의 질문에 대한 답을 바꿉니다.

**상태: `blocked`.** 고장난 것이 아니라 기다리는 중입니다. `STACK-INPUTS.md`의 Owner
입력이 답변되지 않아 `check-stack-readiness`가 `blocked`를 도출하고,
`tools/check-last`는 그 상태의 Stack을 의도적으로 건너뜁니다. Placeholder 하나 때문에
실행할 때마다 잘못된 경보가 뜨지 않게 하려는 것입니다.

이미 들어 있고 지금 바로 쓸모 있는 것:

- `references/pitfalls.md` — 이 Stack에서 Error Message 없이 나는 실패;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 알아내는 방법;
- `mcp/source-routing.md` — 어떤 문서 Source가 정본이고 어떤 것을 참조하면 안 되는지.

`ready`에 도달하려면 실재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는
선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
