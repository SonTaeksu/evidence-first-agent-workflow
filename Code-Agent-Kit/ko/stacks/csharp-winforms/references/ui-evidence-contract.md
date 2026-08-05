# UI Evidence Contract (C# Windows Forms)

## 이 문서가 해결하는 문제

Kit은 Validation Layer를 넷으로 나누며, 두 번째 — Rendered Output — 은 보통 Rendered Document를 읽습니다. Windows Forms는 그것을 만들지 않습니다. 대체물이 없으면 이 Layer는 조용히 "Build가 성공했다"로 무너지는데, 이는 정확히 `validation-layers.md`가 경고하는 실패 — 빈 화면인데 Compile은 통과하는 상황 — 입니다.

## 1. Build 전에 선언하기

Gate §1 Analysis 중에, 구현이 아니라 Source Asset으로부터 Screen Specification을 작성합니다. Form이 담아야 할 것을 나열합니다.

```json
{
  "form": "MainForm",
  "required_controls": [
    { "name": "panelInput", "type": "Panel", "parent": "MainForm" },
    { "name": "txtName", "type": "TextBox", "parent": "panelInput" },
    { "name": "btnGreet", "type": "Button", "parent": "MainForm" }
  ]
}
```

Form이 이미 존재한 뒤에 Specification을 작성하는 것은 아무것도 증명하지 못합니다 — 만들어진 그대로를 서술할 뿐입니다.

## 2. 눈으로 읽지 말고 Extract하기

```bash
python stacks/csharp-winforms/tools/extract_designer_tree.py \
  --designer src/MainForm.Designer.cs \
  --output docs/worklogs/evidence/mainform.tree.json
```

Extractor는 일치시키기 전에 주석을 제거하고, 그 과정에서 문자열 Literal은 보존합니다. 주석 안에만 나오는 Control은 Tree에 들어가지 않고, Literal 안의 `//`는 줄을 자르지 않습니다.

Control은 Field로 선언되고 `new`로 생성될 때만 인정됩니다. 이는 `this.ClientSize = new System.Drawing.Size(...)` 같은 Form Property 대입을 제외합니다 — 이런 것은 Control이 아닙니다.

## 3. 비교 — 이것이 Gate이다

```bash
python stacks/csharp-winforms/tools/check_designer_spec.py \
  --tree docs/worklogs/evidence/mainform.tree.json \
  --spec docs/worklogs/evidence/mainform.spec.json
```

| Finding | Verdict | 이유 |
|---|---|---|
| 필수 Control 없음 | FAIL | 선언된 것을 화면이 담고 있지 않다 |
| 필수 Control의 Type이 틀림 | FAIL | TextBox가 선언된 곳에 Label이 있으면 그 화면이 아니다 |
| 필수 Control의 부모가 틀림 | FAIL | 선언된 Container 밖의 Control은 잘못 배치된 것이다 |
| Form 이름이 다름 | FAIL | Tree가 다른 Form을 서술한다 |
| 자식 없는 Container | WARN | Container는 Runtime에 정당하게 채워질 수 있다 |

빈-Container 경우는 의도적으로 경고입니다. 이를 차단하면 Runtime에 Panel을 채우는 올바른 Code가 실패하고, False Positive 하나가 운영자에게 Gate를 우회하는 법을 가르칩니다.

## 4. 이것이 증명하지 않는 것

Control Tree는 선언이지 Rendering이 아닙니다. 위치, 색, Runtime의 Contrast나 Focus 순서를 확립하지 않으며, Form이 실제로 열린다는 것도 증명하지 않습니다. 이 Layer들은 따로 기록합니다:

| Layer | 이 Stack에서의 Evidence |
|---|---|
| Artifact / compile | MSBuild Exit Code |
| Rendered output | Designer-tree 비교 |
| Runtime behaviour | Capability가 확인되면 UI Automation; 아니면 사유와 함께 `PENDING` |
| Accessibility / colour | 가능하면 Screenshot이나 Automation Evidence; 아니면 사유와 함께 `PENDING` |

Tree가 일치했다는 이유로 Runtime Behaviour를 `PASS`로 보고하는 것은 거짓 주장입니다. Automation Capability가 확인되지 않으면 정직한 기록은 `PENDING`과 그 사유입니다.
