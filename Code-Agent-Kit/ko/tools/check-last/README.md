# check-last

바뀐 것에 해당하는 검사를 돌립니다. **인자를 받지 않으며**, 그게 이 도구의 전부입니다.

```bash
python tools/check-last/check_last.py
```

## 왜 인자가 없나

관측된 12세션 동안 검사 실행이 사실상 0회였습니다. 반대해서가 아니라, 검사를 돌리려면 **어떤 File을 넘길지** 먼저 정해야 했고, 그 결정이 하나의 단계였으며, 그 단계가 건너뛰어졌기 때문입니다.

검사가 요구하는 인자 하나하나가 그 검사가 실행되지 않게 되는 자리입니다. [`../../docs/core/gate-design-principles.md`](../../docs/core/gate-design-principles.md) §7 참고.

## 범위

| 실행 | 범위 |
|---|---|
| `check_last.py` | 마지막 실행 이후 수정된 File |
| `check_last.py --feature <이름>` | 그 기능의 `current.md`가 백틱으로 지명한 File |
| `check_last.py --all` | 전체 Tree |
| `check_last.py --mark` | 기준선만 재설정하고 아무것도 하지 않음 |

기준선은 `.evidence-first/last-check`의 mtime이고 **git 커밋이 아닙니다**. 실사용에서는 커밋이 드물어서, 커밋 기준선은 곧 "전체"로 벌어지고 도구가 느려져 회피 대상이 됩니다. `.gitignore`에 `.evidence-first/`를 넣으세요.

Marker는 출력 **이전에** 갱신됩니다. 실행이 끊겨도 기준선은 올바르게 남습니다.

## 무엇으로 라우팅하나

| 바뀐 것 | 검사 |
|---|---|
| `.ps1`·`.sh`·git Hook | `check-shell-safety` |
| `docs/` 아래 | `check-state-model` — `docs/project-map.md`가 있을 때만. 킷 Mirror를 Project State로 오판하지 않기 위해 |
| `stacks/<이름>/` 아래 | 그 Stack의 `check-stack-readiness` |

`blocked`를 **선언한** Stack은 건너뜁니다. Owner 입력이 의도적으로 미확인이므로 blocked로 판정되는 것이 정상이기 때문입니다. 이것을 표시하면 멀쩡한 Tree에서 운영자 앞에 거짓 경보가 뜨고, 거짓 경보 한 번이면 이 도구를 그만 돌리게 됩니다.

Exit Code:

- `0`: 해당하는 검사가 전부 통과했거나, 해당하는 변경이 없음
- `2`: 검사 1개 이상 실패
- `1`: Tool 오류

```bash
python tools/check-last/self_test.py
```
