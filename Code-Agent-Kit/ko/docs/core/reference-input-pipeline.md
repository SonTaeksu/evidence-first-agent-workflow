# Reference 입력 Pipeline

## 이미지 입력

```text
원본 파일
→ Byte Hash와 Metadata
→ EXIF 방향 정규화
→ ICC 및 Decoded Pixel Hash
→ Palette, Pixel Grid, 이름 있는 영역
→ 무손실 정규화 PNG
→ LLM 입력
```

멀티모달 Preview는 편의를 위한 화면이지 진실 원천이 아닙니다.

## 구현 화면

```text
Browser DOM
→ Computed Color 증거
→ axe Contrast 결과
→ 선택형 Pixel Baseline
→ Reference 영역 비교
```

## SPA HTML 입력

```text
원본 SPA Package
→ Source File Hash
→ 설치 Browser 또는 Playwright Rendering
→ Rendered DOM Hash
→ Grid, Column, Sample Row, Form, Button
→ Worklog Screen Specification
→ 구현 화면 추출
→ 결정론적 완전성 비교
```

`tools/spa-screen-extractor/`를 사용합니다. Specification을 고정한 뒤 전체 SPA Source는 일상적인 모델 Context에서 제외합니다.
