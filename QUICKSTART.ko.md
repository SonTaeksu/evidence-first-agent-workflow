# 빠른 시작

이 저장소는 킷을 **독립적으로 복사 가능한 폴더 두 개**로 제공합니다. 쓸 언어를 골라 그
폴더만 쓰면 됩니다 — 규칙·프롬프트·도구·게이트·샘플이 전부 그 안에 있습니다.

| 언어 | 폴더 | 시작 파일 |
|---|---|---|
| 한국어 | [`Code-Agent-Kit/ko/`](Code-Agent-Kit/ko/) | [`Code-Agent-Kit/ko/QUICKSTART.md`](Code-Agent-Kit/ko/QUICKSTART.md) |
| English | [`Code-Agent-Kit/en/`](Code-Agent-Kit/en/) | [`Code-Agent-Kit/en/QUICKSTART.md`](Code-Agent-Kit/en/QUICKSTART.md) |

## 요약

1. `Code-Agent-Kit/ko`(또는 `en`) 폴더의 내용을 프로젝트에 복사.
2. 프로젝트(git 저장소)에서 커밋 게이트 켜기 — 스크립트 없이 한 줄:
   `git config core.hooksPath tools/enforce-agent-gates`
3. AI 에이전트에게: **"AGENTS.md 따라서 `<원하는 기능>` 추가해줘."**

전체 설명 — **첫 프로젝트 초기화(신규 vs 기존)**, **Windows 첫 실행**, 검증 절차, **`git commit --no-verify` 우회** — 은 각 폴더의 `QUICKSTART.md`에 있습니다. 큰 그림은
[README.ko.md](README.ko.md), [DESIGN-CONCEPTS.ko.md](DESIGN-CONCEPTS.ko.md) 참고.
