# 빠른 시작

[English](QUICKSTART.md) | **한국어**

> 이 프로젝트가 뭔지 아직 모르시겠다면 [README.ko.md](README.ko.md)를 먼저 보세요. 2분이면 됩니다.

## 폴더 고르기

킷은 **서로 독립된 폴더 두 개**로 들어 있습니다. 쓸 언어를 골라 그 폴더만 쓰면 됩니다. 규칙, 절차, 검사, 샘플이 전부 그 안에 있어서 다른 폴더는 볼 일이 없습니다.

| 언어 | 폴더 | 자세한 안내 |
|---|---|---|
| 한국어 | [`Code-Agent-Kit/ko/`](Code-Agent-Kit/ko/) | [`Code-Agent-Kit/ko/QUICKSTART.md`](Code-Agent-Kit/ko/QUICKSTART.md) |
| English | [`Code-Agent-Kit/en/`](Code-Agent-Kit/en/) | [`Code-Agent-Kit/en/QUICKSTART.md`](Code-Agent-Kit/en/QUICKSTART.md) |

## 세 단계

**1. 폴더 내용을 프로젝트에 복사합니다.**

```bash
cp -r Code-Agent-Kit/ko/* your-project/
```

**2. 커밋 검사를 켭니다.** 프로젝트가 git 저장소여야 합니다.

```bash
cd your-project
git config core.hooksPath tools/enforce-agent-gates
```

**Python 3.11 이상** 또는 **PowerShell**, 둘 중 하나만 있으면 됩니다. 모든 검사가 두
언어로 있고 훅은 있는 쪽을 씁니다. 둘 다 없으면 통과시키지 않고 커밋을 거부합니다.

**3. 에이전트에게 시킵니다.**

> AGENTS.md를 따르세요. 사용자 목록 화면을 추가해 주세요.

## 그다음엔?

에이전트는 코드보다 계획을 먼저 쓰고, 잘게 나눠 작업하고, 각 단계를 확인하려고 실행한 명령을 기록합니다. 그 기록 없이 커밋하려 하면 커밋이 거부됩니다.

거부되는 걸 한 번 직접 보는 데 5분이면 됩니다. 그래야 믿게 됩니다 — [gate-test-guide.md](gate-test-guide.md)를 따라 해 보세요.

## 자주 걸리는 두 가지

**"첫 커밋부터 막혀요."** 이미 있던 코드를 들여올 때는 정상입니다. 그 코드에는 작업 기록이 없으니까요. 그 한 번만 `git commit --no-verify`로 넘기고, 이후로는 켜 두세요.

**"내 기술 스택은 어떻게 추가하나요?"** 스택 12개가 이미 들어 있으니 `stacks/`를 먼저
보십시오 — 여러분 것이 절반쯤 되어 있을 수 있습니다. 없으면 `stacks/_template`을 복사해서
채우고, 킷에게 준비됐는지 물어보면 됩니다. [README의 스택 절](README.ko.md)에 요약이 있고, [다른 스택 사용하기](Code-Agent-Kit/ko/docs/getting-started/using-another-stack.md)에 복사해서 쓸 수 있는 프롬프트까지 담긴 전체 안내가 있습니다.

## 더 긴 안내

각 폴더 안의 `QUICKSTART.md`에는 이 문서에 없는 내용이 있습니다. 새 프로젝트와 기존 프로젝트의 차이, Windows에서의 첫 실행, 검증 기록이 실제로 어떻게 생겼는지, 그리고 검사를 우회하는 게 옳은 상황은 언제인지.

전체 그림은 [README.ko.md](README.ko.md), 전체 참조는 [OVERVIEW.ko.md](OVERVIEW.ko.md), 왜 이렇게 만들었는지는 [DESIGN-CONCEPTS.ko.md](DESIGN-CONCEPTS.ko.md)를 보세요.
