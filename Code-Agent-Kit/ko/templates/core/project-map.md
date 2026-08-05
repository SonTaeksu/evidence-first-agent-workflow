# Project Map

## Project Summary

- Repository:
- Default Branch:
- Primary Stack Profile:
- Project Current Summary:
- Last Map Verification:

## Features

| Feature Key | Current | History | Active Worklog | Entry Points | Stack |
|---|---|---|---|---|---|
| | | | | | |

## Architecture State

| 영역 | Current | History | Owner |
|---|---|---|---|
| System | `architecture/system.current.md` | `architecture/system.history.md` | |
| Database | `architecture/database.current.md` | `architecture/database.history.md` | |

## Environment Record

Bootstrap 때 1회 채웁니다. 이게 없으면 모든 Agent와 모든 Session이 같은 사실을 시행착오로 다시
찾아내고, 다시 찾을 때마다 틀릴 기회가 생깁니다.

| 항목 | 값 | 왜 중요한가 |
|---|---|---|
| OS와 Shell | | 명령 구분자가 PowerShell은 `;`, cmd는 `&&`로 정반대 |
| Shell Version | | PowerShell 5.1에는 `&&`·`??`·삼항연산자가 없다 |
| 저장소 경로에 공백이 있는가 | | 있으면 모든 경로를 인용해야 하고 `cd`를 피해야 한다 |
| Python 설치 여부와 실행 이름 | | `python3` / `python` / `py` / 없음 — Python이 없으면 `.ps1` 검사가 유일한 Gate다 |
| Node / Package Manager | | |
| Build Tool과 루트 File 위치 | | Backend가 별도 루트면 `mvn -f` 같은 지정이 필요하다 |
| SDK / Toolchain 경로 | | 기록해 둔다. 다시 타이핑하지 않는다 |
| 긴 명령 Wrapper | | 생성된 `.bat` 또는 `.sh`. gitignore 대상이고 PC당 1개 |
| 고정 로그 파일명 | | 검사가 어떤 File을 읽을지 항상 알 수 있게 |
| CI 사용 가능 여부 | | CI가 없으면 커밋 Hook이 유일한 자동 강제 수단이다 |
| 커밋 Hook 설치 여부 | | git Hook은 clone 시 따라오지 않는다 — 사람이 저장소당 1회 설치한다 |

## Environment Capabilities

| Capability | 상태 | Evidence | 선택 경로 | Verified |
|---|---|---|---|---|
| | present / absent / unknown | | | |

`unknown`은 해당 Capability에 의존하는 구현을 막습니다.

## Shared File Reverse Index

| Shared File | 사용하는 Feature | Risk | 필요한 Regression |
|---|---|---|---|
| | | | |

## Global Entry Points

- UI:
- API:
- Domain:
- Data:
- Tests:
- Validation:

## Routing Notes

-
