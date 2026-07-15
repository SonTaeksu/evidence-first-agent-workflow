# 색·테마 계약 (React + ASP.NET Core)

목표: **참조 스크린샷**(예: WinForms ERP 화면)을 React로 충실히 재현한다. 참조가
**진실 기준**이다 — 테마를 지어내지 말고, 프레임워크 기본 팔레트로 도망가지 말 것
(부트스트랩 파랑·Tailwind 기본 서피스 금지).

## 1. 추출한다 (눈대중 금지)

참조 이미지에 **두 도구 모두** 실행(비전 모델은 전처리된 이미지를 보므로 손으로 고른
hex는 신뢰 불가):

```bash
# 역할 매핑 팔레트 (어떤 색이 배경/라인/텍스트/액센트/상태색인지)
python tools/reference-image-manifest/extract_palette.py <ref.png> --colors 16 \
  --regions "x,y,w,h=header; x,y,w,h=primaryButton"

# 정밀 증거: 해시·ICC·dominant color·정규화 PNG (ΔE 비교용)
python tools/reference-image-manifest/extract_reference_image.py --image <ref.png> ...
```

`extract_palette`는 UI에 바인딩할 **역할 매핑**을, `extract_reference_image`는 검증할
**ΔE 증거**를 줍니다. 둘 다 씁니다.

## 2. 추출한 색을 토큰에 바인딩

추출한 hex를 **CSS 변수**(토큰 파일 하나, 예: `src/styles/tokens.css`의 `:root { --color-... }`)에
기록한다. 컴포넌트는 **토큰만** 참조 — 임의 hex 금지, 테마 대상 서피스에 프레임워크 기본
테마 금지.

| 역할 | 토큰 | 출처 |
|---|---|---|
| 페이지 배경 | `--bg` | 팔레트 무채(밝음) |
| 서피스/패널 | `--surface` | 팔레트 무채 |
| 테두리/그리드 라인 | `--line` | 팔레트 무채(회색) |
| 텍스트/보조 텍스트 | `--text` / `--text-muted` | 팔레트 무채 |
| 액센트/주색 | `--accent` | 팔레트 유채(채도 높은 지배색) |
| 상태색 | `--status-red/-yellow/-green` | 상태색 규약(R/Y/G) |

## 3. 검증 — 하드 게이트 (불일치 시 완료 차단)

- **ΔE 참조 대조:** `python tools/reference-image-manifest/compare_manifest_to_runtime.py` — 렌더된 computed color vs 참조 팔레트; ΔE00이 임계 초과면 실패.
- **런타임 색 게이트:** Playwright `e2e/color-gate.spec.ts`가 핵심 요소(헤더·주 버튼·그리드 라인·상태 칩)가 허용 오차 내에서 **토큰** 색으로 해석되는지 단언.
- **기본 테마 가드:** 테마 서피스가 토큰 대신 프레임워크 기본색을 쓰면 플래그.

컴파일 성공·화면 렌더는 **색 충실도가 아니다** — 별개 레이어(`docs/core/validation-layers.md`).
색 레이어는 따로 기록한다.
