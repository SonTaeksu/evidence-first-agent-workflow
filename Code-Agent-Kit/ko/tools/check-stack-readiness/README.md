# check-stack-readiness

Stack 의존 구현 전에 필요한 문서, Evidence, 사용자 확인, Capability Decision이 존재하는지 검사합니다.

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/react-aspnetcore
```

Exit Code:

- `0`: ready 또는 `--allow-provisional`로 허용된 provisional
- `2`: blocked, 필수 입력 미확인 또는 허용하지 않은 provisional
- `1`: Tool 또는 File 오류

이 Tool은 완전성을 검사하지 Truth를 증명하지는 않습니다. Truth는 Evidence Provenance와 Owner Review로 확인합니다.
