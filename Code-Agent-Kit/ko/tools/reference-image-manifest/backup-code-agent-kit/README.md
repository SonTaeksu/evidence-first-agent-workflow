# Code Agent Kit Palette Tool — 백업

사용자가 제공한 Code Agent Kit의 색상 추출 도구를 대체 수단으로 보존했습니다.

## 기본 도구

먼저 `tools/reference-image-manifest/`를 사용합니다. 다음 증거를 더 넓게 보존합니다.

- 원본 파일 SHA-256
- Decoded Pixel SHA-256
- ICC Profile
- EXIF Orientation
- 무손실 정규화 PNG
- Palette와 정확한 Pixel Grid
- 이름 있는 영역
- Runtime ΔE00 비교

## 백업 도구

- `extract_palette.py`: Pillow 기반 Palette 및 영역 Sample
- `extract_palette_A.ps1`: Windows `System.Drawing` 기반 가벼운 영역 Sample
- `extract_palette_B.ps1`: Windows `System.Drawing` 기반 자동 Palette와 영역 Sample

폐쇄망 Windows에서 Python 또는 Pillow를 설치할 수 없을 때 PowerShell판을 사용합니다. 기본 Manifest를 대체하지 않고 비상용·교차검증용으로 사용합니다.
