# 7 — Project에 설치된 킷 갱신

이미 킷이 깔린 Project에 더 새 Version이 있을 때 씁니다. 최초 설치용이 아닙니다 — 그건 언어 Mirror를 복사하고 `0-sync-and-orient.md`를 돌리면 됩니다.

## 왜 별도 절차인가

설치본이 뒤처지면 최신 Rule과 검사가 **그 Project에서 돌지 않고**, 그 사실을 아무도 알려주지 않습니다. 관측: Project가 두 Revision 뒤처진 상태로 있었고, 그 Project의 문서는 존재하지도 않는 검사를 설명하고 있었습니다. 그 검사들은 전부 조용히 꺼져 있었습니다.

실패 형태가 구체적이고, 실제로 일어났습니다. 갱신을 시도하고, Agent가 이미 있는 File을 보고, "이미 있음"을 "이미 최신"으로 취급해, 33개 중 6개만 쓰고 **설치 완료**라고 보고했습니다. Project는 혼합 상태로 남았고, 정상인 것과 구분할 방법이 없습니다.

## 1. 갱신이 필요한지 확인

Project가 가진 Version과 사용 가능한 Version을 대조합니다. 킷이 Version Banner를 기록한다면 그것을 읽고, 아니면 Manifest를 대조합니다.

```bash
python tools/check-kit-installation/check_kit_installation.py --root .
```

Version이 다르거나 필수 File이 없으면 갱신 대상입니다.

## 2. 복사한다 — 전사하지 않는다

```bash
python install-kit.py --target /path/to/your-project --mode core --stack <your-stack> --overwrite
```

> **Agent가 File을 하나씩 읽어 다시 쓰게 하지 마세요.** File 내용이 Context를 **두 번** 지나갑니다(읽을 때 + 쓸 때). 압축 임계를 넘으면 Agent가 그럴듯해 보이는 내용을 지어내기 시작합니다. 가정이 아닙니다 — 관측된 한 Session에서 **받은 적 없는 File 11개를 썼고**, 그중에는 exit 0을 내는 가짜 커밋 Hook이 있었으며, 완료 보고는 "모든 File이 정상적으로 페치되었다"였습니다.
>
> 복사는 File System 연산입니다. 모델을 지나가는 것이 없으니 지어낼 대상도 없습니다.

## 3. 킷은 덮어쓰고, 사람이 쓴 것은 절대 덮어쓰지 않는다

| 대상 | 규칙 |
|---|---|
| 킷 내용 — `prompts/`·`docs/core/`·`tools/`·`scripts/`·`stacks/_template/`·`AGENTS.md` | **무조건 덮어쓴다** |
| Project State — `docs/project-map.md`·`docs/features/*`·`docs/architecture/*`·`docs/worklogs/*` | **절대 덮어쓰지 않는다** — 없을 때만 생성 |
| 자기 Stack Pack | 손대지 않은 부분만 덮어쓴다. 먼저 diff |

> ⚠️ **"File이 이미 있다"는 건너뛸 근거가 아닙니다.** Version이 올랐다는 것은 기존 File의 **내용이 바뀌었다**는 뜻입니다. 그게 갱신의 목적 전부입니다.

## 4. 완료 판정은 보고가 아니라 개수로

```bash
python tools/check-kit-installation/check_kit_installation.py --root /path/to/your-project
python tools/check-last/check_last.py --root /path/to/your-project --all
```

숫자를 나란히 출력하고, **쓴 것과 건너뛴 것을 나눠 적습니다**.

```text
쓴 것 N개 / 이미 있어 건너뛴 것 M개 / 받지 않은 것 0개
```

건너뛴 File을 설치했다고 보고하는 것이 이 줄이 막으려는 실패입니다 — 관측된 한 실행은 손댄 적도 없는 문서 11개를 설치 목록에 올렸습니다. "N개 설치했다"는 Session 앞부분의 기억이 아니라 **Tree를 다시 나열해서 센 값**이어야 합니다.

갱신이 여러 Session으로 나뉘었다면 **마지막에 전체 개수 대조를 1회** 합니다. 부분 설치는 다음 Session에서 조용히 깨집니다.

## 5. 커밋 Hook을 다시 건다

File이 디스크에 있다고 Hook이 활성화되지 않습니다. git Hook은 `.git/hooks/`에 있고, 그건 clone 시 따라오지 않습니다.

```bash
git config core.hooksPath tools/enforce-agent-gates
```

저장소마다, clone마다 1회입니다. Agent가 가장 확실하게 건너뛰는 단계이므로 `git init`과 함께 사람이 처리하는 편이 낫습니다.

## 6. 검증한 뒤에 완료라고 말한다

```bash
python tools/check-last/check_last.py --root /path/to/your-project --all
```

exit 0이고 4단계의 개수가 기록돼 있어야 합니다. 그 전의 정직한 상태는 `complete`가 아니라 `verified, pending commit`입니다.
