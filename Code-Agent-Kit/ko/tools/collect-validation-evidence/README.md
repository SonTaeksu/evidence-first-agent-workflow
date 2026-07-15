# collect-validation-evidence

명령을 실행하고 표준 출력과 오류 출력을 함께 수집한 뒤 Markdown 및 JSON 증거 파일로 저장합니다. 도구는 원래 명령의 종료 코드를 그대로 반환합니다.

예제:

```bash
python tools/collect-validation-evidence/collect.py \
  --name frontend-build \
  --cwd samples/react-aspnetcore-taskflow/frontend \
  --output samples/react-aspnetcore-taskflow/docs/evidence/generated/frontend-build.md \
  -- npm run build
```

명령이 실패하면 증거 문서에도 FAIL과 원래 종료 코드가 기록되며, 호출한 Validation Script 역시 실패합니다.
