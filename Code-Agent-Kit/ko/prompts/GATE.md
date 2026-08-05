# 필수 실행 Gate

File을 만드는 모든 작업은 아래 다섯 Header를 **이름을 바꾸거나 생략하지 않고** 사용합니다. 필수 Section이 비어 있으면 구현을 시작하거나 완료를 주장할 수 없습니다.

```text
1 Analysis
→ 2 Task
→ 3 Todo와 Micro-Verify
→ 4 Checklist
→ 5 Verification
```

## 실패 Routing

- 가정이 유효한 Local 구현/Test 실패 → 실패한 Todo만 반복
- 잘못된 가정, Unknown Capability, Source 충돌, Scope 불일치 → Analysis 복귀
- 실행하지 않은 Validation → `PASS`가 아니라 `PENDING`

## 0. Analysis 이전 Evidence

해당하는 경우:

- Image → Reference Image Manifest
- SPA → Rendered DOM Screen Specification
- Static HTML → 원본 보존과 제한된 구간 검사
- Stack Fact → 1차 Source Provenance
- 큰 MCP 결과 → 필요한 Fact와 Provenance만 요약하고 불필요한 Retrieval Text 폐기

## 1. Analysis

아래 구조를 복사하고 채웁니다.

```markdown
## 1. Analysis

- Git 기준점과 Incoming Change:
- Project Map Route:
- Feature Current:
- Related Files:
- Shared File 영향:
- Source Evidence:
- 공식 또는 1차 Source Provenance:
- 가정:
- 미확인:
- `⟨확인 필요⟩` 항목:

### Environment Capability Decision

| Capability | 상태 | Evidence | 선택 경로 |
|---|---|---|---|
```

Analysis 중 구현하지 않습니다.

Capability 강제:

1. Project Map Capability 결과를 읽습니다.
2. 이 Section에 결정을 다시 기록합니다.
3. Stack 금지 Rule을 따릅니다.

`unknown`이면 해당 Capability에 의존하는 구현을 막습니다.

## 2. Task

```markdown
## 2. Task

- 목표:
- Acceptance Criteria:
- 제외 범위:
- Validation 명령:

### Expected Files

- [ ]

### 인정된 예상 밖 File

- [ ] path — 이유, 영향, 필요한 Regression
```

Expected Files는 추정입니다. 예상 밖 File은 명시적으로 인정해야 합니다.

## 3. Todo와 Micro-Verify

```markdown
## 3. Todo and Micro-Verify

**진행률:** 0 / N

- [ ] Todo
  - 변경:
  - Micro-Verify:
  - 결과:
  - 실패 처리: Todo 반복 / Analysis 복귀
```

### 기본 자동 분할 기준

다음 중 하나라도 해당하면 Code 전에 Block 목록을 만듭니다.

- Grid 또는 Data Collection 2개 이상
- 사용자 Action 3개 이상
- Dashboard, KPI, Card, Chart, Matrix, Table Block 다수
- Frontend와 Backend Contract 동시 변경
- Deployable Artifact 2개 이상
- Stack Profile이 더 엄격한 기준을 정의

## 4. Checklist

```markdown
## 4. Checklist

- [ ] Architecture와 Naming
- [ ] Contract 동기화
- [ ] Source 충실도
- [ ] Capability Decision 강제
- [ ] Artifact, Rendered Output, Runtime 별도 확인
- [ ] 필수 Visual Block이 비어 있지 않음
- [ ] Error, Loading, Empty, Placeholder State
- [ ] Color 및 Accessibility Evidence
- [ ] Security 및 Trust Boundary
- [ ] Shared File Reverse 영향
- [ ] 무관한 변경 없음
- [ ] State 문서 동기화 준비
```

## 5. Verification

```markdown
## 5. Verification

| Layer 또는 Gate | 명령 | Exit | 결과 | Evidence |
|---|---|---:|---|---|
| Artifact / Compile | | | | |
| Unit / Integration | | | | |
| Rendered Output | | | | |
| Runtime Behavior / E2E | | | | |
| Screen Spec 완전성 | | | | |
| Color / Accessibility | | | | |
| Git Scope | | | | |
| Document Sync | | | | |
```

## 완료

Production Feature 작업은 다음이 필요합니다.

- 필수 Validation PASS
- Feature Current에 `code-verified` 기록
- 가능한 경우 Commit과 PR을 포함한 Append-only Feature History
- Project Map과 Shared File Reverse Index 갱신
- Worklog 종료 또는 Archive
- 최종 Git Diff 검토

격리 Demo는 Production으로 승격하기 전까지 Production Current/History 갱신이 면제됩니다. 자체 README와 명시된 Validation은 필요합니다.

## 부록 — 실패한 완료는 이렇게 생겼다

둘 다 실제 관측입니다. 그때 둘 다 실패로 보고되지 않았습니다.

**빈 상자로 납품된 대시보드.** 원본 목업에는 KPI 6종, 담당 카드 5개, 5×6 매트릭스, 차단 항목 테이블이 있었습니다. 나온 것은 제목, KPI 라벨 몇 개, 그리고 **테두리만 있는 빈 컨테이너**였습니다. 원인 둘: 목업이 Context 한도를 넘어 데이터 구조를 아예 읽지 않았고(나눠 읽거나 검색하지 않음 — `docs/core/source-assets-guide.md` 위반), Build가 통과한 것을 작업이 끝난 것으로 착각했습니다. **빈 화면도 Compile은 통과합니다.**

**빈 컨테이너 3개로 납품된 그리드 3개.** Reference 이미지에는 컬럼명과 행 데이터를 가진 Grid 3개가 있었습니다. 나온 것은 테두리 사각형 3개였습니다. 원인: 작업 Prompt는 따랐지만 그 안의 추출 단계를 건너뛰어, 이미지를 Block·Column·Row로 분해하지 않았습니다. **표는 크기만 맞는 빈 컨테이너가 아니라, 행이 들어 있는 Dataset에 Binding된 Grid입니다.**

둘 다 막는 방법이 이 문서에 이미 있고, 두 실행 모두 그것을 건너뛰었습니다.

- §1은 Analysis를 쓰기 **전에** Source Evidence를 추출할 것을 요구합니다. 대충 훑는 것이 아닙니다
- §3은 화면에 데이터 Block이 여럿이면 Todo Block 목록을 요구합니다 — Block 하나당 Todo 하나, 각각 자기 Micro-Verify를 가집니다
- §4는 `필수 Visual Block이 비어 있지 않음`을 Source와 Block 단위로 대조할 것을 요구합니다
- §5는 Rendered Output을 Compile과 **별도 Layer**로 기록합니다. 빈 화면에서 Compile이 통과하기 때문입니다

Verification 표에 `Artifact PASS`만 있고 나머지가 비어 있으면, 그 작업은 끝난 것이 아니라 **검증되지 않은 것**입니다.
