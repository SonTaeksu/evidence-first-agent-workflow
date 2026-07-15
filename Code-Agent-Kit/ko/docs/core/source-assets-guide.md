# Source Asset 처리 Guide

## Asset 유형별 우선순위

UI 구조와 동작 기준:

```text
Rendering된 HTML 또는 SPA
→ Reference Image
→ Text 설명
```

이미지 자체의 정확한 색상은 원본 이미지 파일과 Manifest가 기준입니다.

서로 충돌하면 조용히 섞지 말고 충돌 사실을 보고합니다.

## 공통 규칙

- 원본 파일을 변경하지 않고 보존합니다.
- 모델에 넣기 전에 Hash를 기록합니다.
- 읽지 못한 원본을 모델이 만든 요약으로 대체하지 않습니다.
- 추출과 구현을 분리합니다.
- 추출 Evidence를 Worklog에 저장합니다.
- Evidence를 고정한 뒤 큰 원본을 반복해서 읽지 않습니다.

## Static HTML

- DOM, CSS, 표시 Text, Script를 Evidence로 보존합니다.
- 큰 파일은 제한된 구간으로 나누어 읽습니다.
- Style, Data, Table, Form, Script 위치를 먼저 검색합니다.
- 확인 목적으로 원본 전체를 다시 작성하지 않습니다.
- UI 구조는 유지하고 Mock Data를 명시적인 Binding 지점으로 바꿉니다.

## SPA HTML

SPA 원본 Source에는 빈 Mount Element만 있을 수 있습니다.

필수 절차:

1. SPA 실행 또는 열기
2. 유용한 UI가 Rendering될 때까지 대기
3. 가능한 경우 Rendered DOM 저장
4. `tools/spa-screen-extractor/extract_spa.py` 실행
5. Screen Spec Markdown과 JSON 저장
6. Block, Grid, Column, Row, Control, Button을 Worklog에 기록
7. 전체 SPA Source를 일상적인 모델 Context에서 제거
8. 구현 Application도 추출하고 `check_screen_spec.py` 실행

Console 및 PowerShell 대체 방식은 Tool README에 있습니다.

## 이미지

필수 절차:

1. 정확한 원본 Byte 보존
2. Reference Image Manifest 생성
3. ICC, EXIF Orientation, File Hash, Decoded Pixel Hash, Palette, Grid Sample, 이름 있는 영역 보존
4. 플랫폼 Preview보다 먼저 Manifest와 무손실 정규화 PNG 제공
5. 정확한 색상이 중요하면 Runtime Computed Color와 ΔE00 비교

Code Agent Kit Palette Script는 백업으로만 유지합니다.

## 보안

고객의 비공개 Asset을 공개 저장소에 Commit하지 않습니다. 생성 Evidence에도 원본 Text와 Color가 포함될 수 있으므로 같은 보안 규칙을 적용합니다.
