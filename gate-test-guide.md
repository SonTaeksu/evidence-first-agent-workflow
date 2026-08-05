# Commit Gate — Test Guide / 게이트 테스트 가이드

How to verify the evidence-first commit gate actually blocks a bad commit.
Evidence-First 커밋 게이트가 실제로 잘못된 커밋을 막는지 확인하는 방법.

---

## EN

### 0. Install the hook (once, in the project root)

```bash
git config core.hooksPath tools/enforce-agent-gates
chmod +x tools/enforce-agent-gates/pre-commit
```

### 1. Block test — commit source with no workflow (must FAIL)

```bash
echo "export const x = 1;" > app.ts
git add app.ts
git commit -m "add feature"
```

Expected — the commit is rejected (exit code 1):

```
Evidence-First enforcement gate
  result         : BLOCKED
  FAIL  [gate] project source changed but no worklog under docs/worklogs/ was produced.
  FAIL  [state] source changed but no feature '*.current.md' was updated.
  FAIL  [state] source changed but no feature '*.history.md' append was made.
```

If it commits anyway, the hook is not installed — recheck step 0.

### 2. Pass test — provide the workflow artifacts (must SUCCEED)

Create `docs/worklogs/<feat>.worklog.md` with the 5 GATE sections, and in **§5 Verification**
paste a real command, its `exit code: 0`, and an output marker. Update the feature's
`*.current.md` and `*.history.md`. Stage all of it together, then commit.

```bash
git add app.ts docs/worklogs/ docs/state/ docs/project-map.md
git commit -m "add feature x with evidence"   # passes
```

### 3. Manual override (explicit human decision)

```bash
git commit -m "hotfix" --no-verify
```

### 4. Run the gate directly (no commit)

```bash
git add -A
python tools/enforce-agent-gates/enforce_gates.py --staged    # exit 0 = pass, 2 = blocked
```

### 5. CI / PR check (diff against a base ref)

```bash
python tools/enforce-agent-gates/enforce_gates.py --base origin/main
```

**Key point:** the gate only fires when a **source file** (`.ts .cs .py .js .go` …) is staged.
Staging docs only will not trigger it — always include a source-extension file when testing.

---

## KO / 한국어

### 0. 훅 설치 (프로젝트 루트에서 한 번)

```bash
git config core.hooksPath tools/enforce-agent-gates
chmod +x tools/enforce-agent-gates/pre-commit
```

### 1. 차단 테스트 — 절차 없이 소스만 커밋 (막혀야 정상)

```bash
echo "export const x = 1;" > app.ts
git add app.ts
git commit -m "add feature"
```

기대 결과 — 커밋 거부(exit code 1):

```
Evidence-First enforcement gate
  result         : BLOCKED
  FAIL  [gate] project source changed but no worklog under docs/worklogs/ was produced.
  FAIL  [state] source changed but no feature '*.current.md' was updated.
  FAIL  [state] source changed but no feature '*.history.md' append was made.
```

그냥 커밋되면 훅이 설치 안 된 것 — 0단계 다시 확인.

### 2. 통과 테스트 — 절차 산출물 갖추면 커밋됨

`docs/worklogs/<feat>.worklog.md`에 GATE 5단계를 적고, **§5 Verification**에 실제 명령 +
`exit code: 0` + 출력 마커를 붙입니다. 해당 feature의 `*.current.md`·`*.history.md`도 갱신.
전부 함께 스테이징한 뒤 커밋합니다.

```bash
git add app.ts docs/worklogs/ docs/state/ docs/project-map.md
git commit -m "add feature x with evidence"   # 통과
```

### 3. 수동 우회 (사람이 명시적으로 결정)

```bash
git commit -m "hotfix" --no-verify
```

### 4. 게이트만 단독 실행 (커밋 없이)

```bash
git add -A
python tools/enforce-agent-gates/enforce_gates.py --staged    # exit 0=통과, 2=차단
```

### 5. CI / PR 검사 (base ref와 diff)

```bash
python tools/enforce-agent-gates/enforce_gates.py --base origin/main
```

**핵심:** 게이트는 **소스 파일**(`.ts .cs .py .js .go` …)을 스테이징해야 발동합니다.
문서만 바꾸면 발동 안 하니, 테스트할 땐 반드시 소스 확장자 파일을 하나 넣으세요.
