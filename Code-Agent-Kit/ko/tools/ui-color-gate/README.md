# UI 색상 게이트

작은 모델이 Screenshot을 보고 색상이 맞는지 추측하지 않도록 UI 색상 판단을 외부 도구로 분리합니다.

## 포함 검사

### 1. 색상 대비 게이트

`@axe-core/playwright`가 실제 렌더링된 화면에 `color-contrast` 규칙을 실행합니다.

```bash
cd samples/react-aspnetcore-taskflow/frontend
npm run e2e:color
```

색상 대비 위반이 발견되면 종료 코드가 실패합니다.

### 2. 실제 적용 색상 증거 추출

같은 Test에서 다음 Computed Style을 JSON으로 추출합니다.

- `color`
- `background-color`
- `border-color`
- Font Size
- Font Weight
- 짧은 Text Sample
- Selector 힌트

작은 LLM에 Screenshot만 주고 색을 추측하게 하지 않고, 이 JSON 증거를 입력으로 제공할 수 있습니다.

### 3. 선택적 Visual Baseline 게이트

```bash
npm run e2e:visual
```

Playwright가 Desktop 및 좁은 화면 Screenshot을 승인된 기준 이미지와 비교합니다. 기준 이미지는 커밋 전에 사람이 검토해야 합니다. OS와 Browser Version에 따라 Pixel 차이가 생길 수 있으므로 CI에서는 Playwright Browser 환경을 고정하는 것이 좋습니다.

## 한계

자동 Contrast Test만으로 모든 접근성·디자인 결함을 찾을 수는 없습니다. Contrast가 PASS여도 디자이너가 의도한 정확한 색상이라는 의미는 아닙니다. 정확한 외형은 Visual Baseline을 사용하고 Brand 판단은 사람이 검토합니다.
