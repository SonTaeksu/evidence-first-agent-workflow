# 프런트엔드 Validation

필수:

```bash
npm run lint
npm run test
npm run build
```

UI 동작:

```bash
npm run e2e
```

증거:

- 실행 명령과 종료 코드
- Test 요약
- Production Build 결과
- Layout 변경 시 Screenshot 또는 Playwright 결과
- 최종 Frontend Diff

## 결정론적 색상 게이트

```bash
npm run e2e:color
```

색상, Background, Typography, Badge, Button, Theme 변경 후 필수입니다.
