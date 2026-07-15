# SPA HTML Reference

원본 SPA Package는 비공개 Project Repository에만 둡니다. 공개 Workflow Repository에서는 고객 비공개 Asset을 Git 밖에 보관합니다.

## 처리 순서

1. 원본 Package 보존
2. Source File Hash 기록
3. 설치 Browser 또는 Playwright로 Rendering
4. 정책상 가능하면 Rendered DOM 저장
5. `tools/spa-screen-extractor/extract_spa.py` 실행
6. `screen-spec.md`, `screen-spec.json` 저장
7. 추출한 Block, Grid, Column, Sample Row, Form, Button을 Active Worklog에 기록
8. 전체 SPA Source를 일상적인 모델 Context에서 제거
9. 완료 전에 구현 화면도 추출하여 Specification 비교

PowerShell:

```powershell
./scripts/create-spa-screen-spec.ps1 `
  -Source "C:\reference\mockup.html" `
  -Wait 3000
```

Headless 실행이 차단되면 Browser Console의 `extract_screen.js`를 사용합니다.
