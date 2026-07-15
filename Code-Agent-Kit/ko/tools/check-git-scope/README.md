# check-git-scope

최종 변경 파일을 Design 및 Worklog 범위와 비교합니다.

Code Agent Kit에서 반영한 개선:

- `origin/main` → `main` → `master` 기준점 Fallback
- Commit된 변경과 Working Tree 변경을 함께 검사
- Expected File 목록 직접 입력
- 이유가 기록된 예상 밖 파일 인정
- Git이 없을 때 Artifact 존재 검사로 Fallback
- 예상했지만 변경되지 않은 파일을 Strict Mode에서 실패 처리

Design 사용:

```bash
python tools/check-git-scope/check_git_scope.py \
  --design docs/designs/feature.md \
  --scope samples/application
```

Worklog 목록 사용:

```bash
python tools/check-git-scope/check_git_scope.py \
  --expected-file expected-files.txt \
  --ack-file acknowledged-files.txt
```

인정 파일은 조용히 무시하지 않습니다. 이유와 영향을 Design 또는 Worklog에 기록해야 합니다.
