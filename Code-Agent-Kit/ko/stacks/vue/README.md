# Vue.js

Vue 기반 Single-page UI 또는 내장 UI. Major Version이 단단한 경계입니다.

**상태: `blocked`.** 고장이 아니라 대기입니다. `STACK-INPUTS.md`의 Owner 입력이 비어 있어
`check-stack-readiness`가 `blocked`을 도출하고, `tools/check-last`는 그 상태의 Stack을 의도적으로
건너뜁니다. Placeholder 하나로 매번 거짓 경보가 뜨지 않게 하려는 것입니다.

이미 들어 있고 쓸모 있는 것:

- `references/pitfalls.md` — Error Message를 남기지 않는 이 Stack의 실패;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 판별하는 방법;
- `mcp/source-routing.md` — 어떤 문서 Source가 Authoritative이고 어떤 것을 참조하면 안 되는지.

`ready`로 가려면 실재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는 선언이 아니라
측정입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
