# WCF (.NET Framework 4.7.2+)

WCF 위에서 동작하는 SOAP 및 net.tcp Service이며, .NET Framework 4.7.2 이상을
Target합니다.

**상태: `blocked`.** 고장난 것이 아니라 기다리는 중입니다. `STACK-INPUTS.md`의
Owner 입력이 아직 답변되지 않아 `check-stack-readiness`가 `blocked`를 도출하고,
`tools/check-last`는 그 상태의 Stack을 일부러 건너뜁니다. Placeholder가 매번
거짓 경보를 내지 않도록 하기 위해서입니다.

이미 들어 있고 바로 쓸 수 있는 것:

- `references/pitfalls.md` — 오류 Message를 전혀 남기지 않는 이 Stack의 실패들;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 확인하는 방법;
- `mcp/source-routing.md` — 어떤 문서 Source가 정본이고 어떤 Source를 봐서는 안
  되는지.

`ready`에 도달하려면 실제로 존재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다.
Evidence는 선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
