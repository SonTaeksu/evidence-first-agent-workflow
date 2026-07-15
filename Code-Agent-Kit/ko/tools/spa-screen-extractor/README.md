# SPA 화면 추출기

빈 SPA Mount Source가 아니라 **Rendering된 DOM**을 읽습니다.

## 추출 Evidence

- Grid, Column, Sample Row, 대략적 Row 수
- Form 및 Input Control
- Button 및 Tab
- KPI, Card, Chart, Matrix, Panel Block
- Text/Value/Media/Control 존재 여부
- 빈 Visual Block 상태
- Source File 및 Rendered DOM SHA-256
- Rendering 방식 및 대기 시간

## 추출

설치된 Edge, Chrome, Chromium:

```powershell
python tools/spa-screen-extractor/extract_spa.py `
  --browser "C:\reference\mockup.html" `
  --wait 3000 `
  --json "reference-assets/evidence/mockup/screen-spec.json" `
  --out "reference-assets/evidence/mockup/screen-spec.md" `
  --save-dom "reference-assets/evidence/mockup/rendered.html"
```

이미 저장한 Rendered HTML:

```bash
python tools/spa-screen-extractor/extract_spa.py \
  --from-file rendered.html \
  --json screen-spec.json \
  --out screen-spec.md
```

다른 지원 경로:

- `--render`: Playwright 사용 후 설치 Browser Fallback
- `--crawl`: 제한된 Local HTML Link 순회
- `extract_screen.js`: Browser Console Fallback
- `extract_screen.ps1`: 가벼운 PowerShell Fallback

## 완전성 비교

```bash
python tools/spa-screen-extractor/check_screen_spec.py \
  --reference reference-screen-spec.json \
  --implementation implementation-screen-spec.json \
  --require-rows \
  --strict-controls \
  --strict-visual-blocks \
  --reject-empty-visual-blocks \
  --output comparison.json
```

Grid, Column, Row, Control, Button, Visual Block 누락, Type 불일치, Reference는 채워졌지만 구현 Block이 빈 경우 Exit Code `2`를 반환합니다.

## 역할 경계

구조 Evidence는 Heuristic이며 Stack 비종속입니다. Stack Validator는 Binding, Generated File, Runtime 전용 검사를 추가할 수 있습니다. 정확한 Color Evidence는 Reference Image Manifest와 UI Color Gate가 담당합니다.

## 자체 검사

```bash
python tools/spa-screen-extractor/self_test.py
```

Self-test에는 의도적 Column 누락과 빈 Visual Block 실패가 포함됩니다.
