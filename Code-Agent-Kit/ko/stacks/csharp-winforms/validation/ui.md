# UI Validation

Windows Forms는 Rendered Document를 만들지 않으므로, Rendered-output Layer는 대신 Designer Control Tree를 읽습니다. 전체 근거는 [`../references/ui-evidence-contract.md`](../references/ui-evidence-contract.md)에 있습니다.

## 필수

```bash
python stacks/csharp-winforms/tools/extract_designer_tree.py \
  --designer {FORM}.Designer.cs \
  --output {EVIDENCE}/tree.json

python stacks/csharp-winforms/tools/check_designer_spec.py \
  --tree {EVIDENCE}/tree.json \
  --spec {EVIDENCE}/spec.json
```

Specification은 Form이 존재하기 전, Gate §1 Analysis 중에 Source Asset으로부터 작성합니다. 나중에 작성된 Specification은 만들어진 것을 서술할 뿐 아무것도 증명하지 않습니다.

## Evidence

- Worklog와 함께 Commit되는 Specification File;
- Worklog와 함께 Commit되는 Extract된 Tree;
- 비교 명령과 그 Exit Code;
- 비어 있다고 보고된 각 Container에 대한 사유가 명시된 모든 Warning.

## 순서

```text
source asset
→ screen specification (§1 Analysis)
→ implementation
→ designer-tree extraction
→ comparison (§5 Verification)
```

## Runtime, Accessibility, Colour

이 Layer들은 실행 중인 창이 필요합니다. 확인된 `ui-automation` Capability가 없으면 이를 관찰할 결정론적 방법이 없고, 기록은 `PASS`가 아니라 사유와 함께 `PENDING`입니다.

Automation Harness가 확인되면 그 명령을 여기에 추가하고 각 명령이 어떤 Layer를 다루는지 명시합니다. 하나의 Harness 호출이 세 Layer 전부를 대신하게 두지 않습니다.

## 수동 점검

사람이 찍은 Screenshot은 유용한 보조 자료이지 Evidence가 아닙니다. Exit Code로 재현할 수 없으며 통과한 Gate로 기록되지 않습니다.
