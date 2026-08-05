# check-script-parity

각 `.py` 검사와 그 `.ps1` 양벌이 **같은 판정**을 내는지 증명합니다. 파이썬 없는 PC가 다른 모든 PC와 같게 판정되도록 하기 위한 것입니다.

```bash
python tools/check-script-parity/check_script_parity.py --root .
python tools/check-script-parity/check_script_parity.py --root . --status
python tools/check-script-parity/check_script_parity.py --root . --tool check-shell-safety
```

## 무엇을 대조하나

Exit Code만으로는 부족합니다 — 두 구현이 **서로 다른 이유로** 각각 `2`를 내도 동일해 보입니다. 케이스마다 쌍으로 대조합니다.

```text
(Exit Code, 출력된 finding 식별자 집합)
```

식별자는 `<도구>:<finding-id>`이고 Tool이 직접 출력합니다. [`../../docs/core/finding-identifiers.md`](../../docs/core/finding-identifiers.md) 참고.

## 일치만으로도 부족하다

두 양벌이 **같은 방식으로 틀려도** 일치합니다. 그래서 케이스마다 규약이 요구하는 Exit Code를 못박습니다.

| 판정 | Exit |
|---|---|
| 통과 | `0` |
| Validation 실패 | `2` |
| Tool 오류 | `1` |

양벌은 일치하는데 둘 다 `expect`와 어긋나면 `CONV`(규약 위반)로 보고하고, Parity 불일치와 따로 세며, Exit는 `2`입니다. 이로써 Exit Code 규약이 문서상의 의도가 아니라 **기계 판정**이 됩니다.

## 요구사항

PowerShell이 `PATH`에 있어야 합니다 — `pwsh` 우선, `powershell` 허용. **없으면 이 Tool은 `0`이 아니라 `1`로 끝납니다.** 검증되지 않은 양벌을 검증된 것으로 기록하는 것이, 검증 안 됐다고 기록하는 것보다 나쁩니다.

`pwsh` 7이면 충분합니다. Windows PowerShell 5.1은 Linux에 설치할 수 없으므로 양벌은 5.1의 부분집합으로 작성합니다 — `&&`·`??`·삼항연산자·`-Parallel` 금지. 5.1 고유 동작은 Windows에서 확인합니다.

## Fixture

이 하네스가 소유하며 각 Tool의 `self_test`에서 빌려오지 않습니다. Tool 내부를 읽는 하네스는 그 Tool을 Refactoring할 때마다 깨지고, 그러면 아무도 돌리지 않게 됩니다.

Fixture가 Tool의 요구 목록을 만족해야 하는 경우에는 그 목록을 **복사하지 않고 Tool에서 import**합니다. 둘이 어긋날 수 없게 하기 위해서입니다.

File System이 아니라 git을 읽는 케이스는 `"git": True`를 지정하고, 하네스가 `main`에 커밋 1개를 가진 실제 저장소를 만듭니다. git 출력의 개행과 경로 구분자는 두 구현이 실제로 갈리는 지점이고, 실제 저장소만이 그것을 시험합니다.

## Status 보고 읽기

```text
  OK  check-shell-safety      twinned            11 case(s)
  --  check-git-scope         not started        -
  --  check-last              identifiers only   -

  twinned 6 / 19 tools, 47 case(s) total
  remaining: check-agent-config, check-git-scope, ...
```

`--status`는 Tree를 걸어서 답하므로 "어디까지 됐나"를 기억이 아니라 **실측**으로 답합니다. 손으로 쓴 진행 목록보다 이것을 신뢰하세요.

Exit Code:

- `0`: 모든 케이스가 일치하고 못박은 기대값도 전부 맞음
- `2`: Parity 불일치 또는 규약 위반
- `1`: Tool 오류. PowerShell 부재 포함
