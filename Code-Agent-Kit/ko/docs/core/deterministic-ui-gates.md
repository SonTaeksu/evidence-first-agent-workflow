# 결정론적 UI 게이트

UI Validation을 세 단계로 분리합니다.

1. **구조와 동작**: Playwright Locator, Status Transition, Scroll, Viewport 검사
2. **색상과 접근성**: axe `color-contrast`와 Computed Color 증거
3. **정확한 외형**: 승인된 Playwright Screenshot Baseline

두 번째 단계는 작은 모델에서 특히 중요합니다. 모델에게 CSS 색상을 눈으로 판단시키지 않고, 실제 렌더링된 구조화 증거와 PASS/FAIL 결과를 제공합니다.

실행:

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm run e2e:color
```

색상, Theme, Badge, Button, Typography, Background를 변경한 작업은 이 게이트를 통과하기 전에는 DoD를 통과할 수 없습니다.
