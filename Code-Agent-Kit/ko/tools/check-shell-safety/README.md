# check-shell-safety

리뷰를 통과하고 작성자 PC에서는 돌지만 남의 PC에서 깨지는 Script 결함을 잡습니다.

```bash
python tools/check-shell-safety/check_shell_safety.py --root .
python tools/check-shell-safety/self_test.py
```

| 발견 항목 | 왜 깨지나 |
|---|---|
| UTF-8 BOM 없는 `.ps1` | PowerShell 5.1이 시스템 ANSI 코드페이지로 읽습니다. 비ASCII Literal이 깨지고, 그것이 비교나 정규식에 쓰이면 표시만이 아니라 **판정이 실패**합니다 |
| BOM이 **붙은** `.sh`·git Hook | shebang이 File 선두가 아니게 되어 Interpreter가 선택되지 않습니다 |
| `-LiteralPath` 없는 PowerShell 경로 Cmdlet | `Test-Path`·`Resolve-Path`·`Get-Content`·`Remove-Item`·`New-Item` 계열이 위치 매개변수의 `[ ] * ?`를 Glob으로 해석합니다. `project [old]` 같은 디렉터리는 아무것도 매칭하지 않고, Script는 그 File이 없는 것처럼 진행합니다 |
| 경로 자리의 미인용 Shell 변수 | `cd $ROOT`는 첫 공백에서 쪼개지고, `My Projects` 아래의 Windows 체크아웃은 예외가 아니라 기본값입니다 |

Exit Code:

- `0`: 깨끗함
- `2`: 발견 1건 이상
- `1`: Tool 또는 File 오류

주석 줄은 건너뛰고, 다른 Switch 뒤의 `-LiteralPath`도 인식하며, 인용된 Literal 경로를 변수로 오인하지 않습니다. Self-test 11케이스 중 7개가 무언가를 **통과시켜야 한다**를 확인합니다 — 여기서 오탐이 나면 모든 Script가 깨진 것처럼 보이고 운영자가 검사를 그만 돌리게 되는데, 그 비용이 잡으려던 결함보다 큽니다. [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §2 참고.

규칙과 근거: [`../../docs/core/command-and-process-safety.md`](../../docs/core/command-and-process-safety.md).
