# Reference Image Manifest

멀티모달 변환 전에 참조 스크린샷을 색/구조 **증거**로 만든다. 상호보완 도구 두 개 — 둘 다 실행:

- **`extract_palette.py`** — 역할 매핑 팔레트: 어떤 hex가 배경/서피스/라인/텍스트/액센트인지, 상태색은 R/Y/G 규약. `--regions`로 특정 컨트롤 색(헤더·주 버튼) 정밀 샘플. **UI 토큰에 바인딩**할 대상. (`.ps1` 래퍼: `extract_palette_A.ps1`, `extract_palette_B.ps1`.)
- **`extract_reference_image.py`** — 정밀 증거: 원본/디코드 해시, ICC, EXIF, dominant color, 명명 영역, 정규화 무손실 PNG. **ΔE 증거** 기반.
- **`compare_manifest_to_runtime.py`** — 런타임 computed color vs 참조 팔레트 ΔE00 비교(색 검증 게이트).

흐름: 참조에 두 추출기 실행 → `extract_palette` 역할을 CSS 변수 토큰에 바인딩 →
`compare_manifest_to_runtime.py`로 렌더 결과 검증.

바인딩 규칙과 하드 색 게이트는 `stacks/react-aspnetcore/references/color-contract.md` 참고.
