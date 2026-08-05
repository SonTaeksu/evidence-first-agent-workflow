# check-kit-selfcheck

킷 자신의 Seed 산출물을 킷 자신의 Validation에 돌립니다. 킷이 복사하라고 지시한 Template은 수정 없이 통과해야 하며, 통과하지 못하면 유일한 출구가 Gate 우회입니다.

```bash
python tools/check-kit-selfcheck/check_kit_selfcheck.py --root .
python tools/check-kit-selfcheck/self_test.py
```

두 가지를 확인합니다.

- **Seed Template**: 문서가 지시한 복사 원본을 지시된 대로 복사해 Validation합니다. 빈 Seed는 입력이 의도적으로 unknown이므로 `blocked`가 나오는 것이 **정상**이고, 따라서 미확인 Input·Capability는 무시합니다. 구조적 실패만 셉니다 — 필수 문서 누락·빈 File, 잘못된 배열 Type, 선언 상태와 도출 상태의 불일치.
- **배포된 Stack**: Manifest가 `ready`를 선언한 Stack은 실제로 ready로 Validation돼야 합니다.

Exit Code:

- `0`: 킷이 자기 검사를 통과
- `2`: Seed 또는 배포된 Stack이 킷 자신의 Validation에 막힘
- `1`: Tool 또는 File 오류

`--seed <경로>`로 기본 복사 원본을 바꿀 수 있습니다. 근거는 [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §4.
