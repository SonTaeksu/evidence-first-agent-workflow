# Portable Code Agent Kit — 한국어

> **처음이세요? [QUICKSTART.md](QUICKSTART.md)부터 보세요 — 한 페이지, 3단계로 결과.**

이 디렉터리는 독립적으로 사용할 수 있는 완전한 한국어 Mirror입니다. **이 디렉터리의 내용 전체**를 대상 Repository에 복사하거나 Installer를 실행합니다.

## 가장 빠른 사용

```powershell
.\install-kit.ps1 -Target C:\path	o\project -Mode full
```

Python:

```bash
python install-kit.py --target /path/to/project --mode full
```

Core와 선택 Stack만 설치:

```powershell
.\install-kit.ps1 -Target C:\path	o\project -Mode core -Stack react-aspnetcore
```

## 포함 내용

- Root Agent Rule과 Adapter
- Prompt 및 필수 Gate
- Agent용 Core 문서와 Architecture Decision
- `.agentignore`로 일반 Indexing에서 제외되는 사람용 Onboarding 문서
- State, Worklog, Project Map, Stack Template
- Stack Profile 및 Readiness 검사
- 결정론적 Tool과 Script
- Demo 및 Demo Template
- Image, SPA HTML, 생성 Evidence용 Reference Asset Directory
- 선택형 Sample Application과 비활성 CI Template
- License 원문과 Manifest

## 시작 순서

1. `AGENTS.md` 읽기
2. `docs/getting-started/README.md` 읽기
3. 선택 Stack의 `STACK-INPUTS.md` 작성 또는 확인
4. Stack Readiness 실행
5. `prompts/0-sync-and-ori