# check-mirror-parity

언어 Mirror를 서로 대조하고, 문서가 적어둔 수치를 실측과 대조합니다.

```bash
python tools/check-mirror-parity/check_mirror_parity.py --root ..
python tools/check-mirror-parity/self_test.py
```

Mirror들을 담은 디렉터리에서 실행하거나 `--root`로 지정합니다.

| 검사 | 판정 |
|---|---|
| 모든 Mirror가 같은 상대 경로 집합을 가진다 | 고아 경로 발견 시 FAIL |
| 산문이 아닌 File(`.py`·`.sh`·`.ps1`·`.js`·`.cs`)이 Mirror 간 Byte 동일 | 차이 발견 시 FAIL |
| `mirrored_file_count`가 `mirrored_file_count_rule`이 지정한 규칙의 실측과 일치 | 모순 시 FAIL |
| 규칙이 기록되지 않은 수치 | WARN — 문서에 적히지 않은 규칙 아래에서는 맞을 수 있다 |
| Build 잔재(`__pycache__`·`.pyc`·`.pyo`) | 측정에서 제외, 있으면 WARN |

번역되는 것은 문서뿐이므로 Script에 차이가 있으면 같은 입력에 Mirror가 서로 다른 판정을 냅니다. 고아 경로는 한쪽 언어에서 Link 또는 문서화된 명령이 깨졌다는 뜻입니다.

Exit Code:

- `0`: Mirror가 일치하고 검사 가능한 수치가 전부 맞음
- `2`: 고아 경로, Shared Source 차이, 또는 실측과 모순되는 수치
- `1`: Tool 또는 File 오류

`--mirror <이름>`으로 Mirror를 선택하고 `--identical-suffix <확장자>`로 Byte 동일 대상을 넓힙니다. 근거는 [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §2.
