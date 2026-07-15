# check-document-sync

다음을 검사합니다.

- 코드가 변경됐지만 상태 문서가 하나도 갱신되지 않은 경우
- 필수 상태 파일이 없는 경우
- Project Map이 저장소에 존재하지 않는 경로를 참조하는 경우

예제:

```bash
python tools/check-document-sync/check_document_sync.py \
  --base main \
  --scope samples/react-aspnetcore-taskflow \
  --current docs/current.md \
  --history docs/history.md \
  --project-map docs/project-map.md
```
