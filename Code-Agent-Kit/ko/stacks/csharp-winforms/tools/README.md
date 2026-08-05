# csharp-winforms Stack Tools

Rendered Document가 없는 UI Framework의 Rendered-output Layer를 위한 결정론적 Evidence.

```bash
python tools/extract_designer_tree.py --designer {FORM}.Designer.cs --output tree.json
python tools/check_designer_spec.py --tree tree.json --spec spec.json
python tools/self_test.py
```

## extract_designer_tree.py

`InitializeComponent`를 Parsing해 Control Tree를 만듭니다: 이름, Type, 부모, Text, Container 여부, 자식 개수.

주석은 일치시키기 전에 같은 길이로 지워지므로 Offset과 줄 번호는 그대로 유지되고, 문자열 Literal은 보존됩니다. 주석에만 언급된 Control은 Tree에 들어가지 않고, Literal 안의 `//`는 줄을 자르지 않습니다.

이름은 Field로 선언되고 `new`로 생성될 때만 Control로 인정됩니다. 이는 `this.ClientSize = new System.Drawing.Size(...)` 같은 Form Property 대입을 제외합니다.

Exit Code: `0` Tree가 생성됨, `2` Form을 찾지 못함, `1` Tool 오류.

## check_designer_spec.py

Gate §1 Analysis 중에 작성된 Specification과 Tree를 비교합니다.

| Finding | Verdict |
|---|---|
| 필수 Control이 없거나, Type이 틀리거나, 부모가 틀림 | FAIL |
| Form 이름이 선언과 다름 | FAIL |
| 자식 없는 Container | WARN |

빈-Container 경우는 경고인데, Container가 Runtime에 정당하게 채워질 수 있기 때문입니다. 이를 차단하면 올바른 Code가 실패하고, False Positive 하나가 운영자에게 Gate를 우회하는 법을 가르칩니다 — [`../../../docs/core/gate-design-principles.md`](../../../docs/core/gate-design-principles.md) §1을 참조하십시오.

Exit Code: `0` 충족, `2` 필수 Control이 없거나 Type이 틀림, `1` Tool 오류.

## self_test.py

열네 개의 Case. 절반은 무언가가 제거된다고 확인하고, 절반은 무언가가 유지된다고 확인하는데, 문자열 Literal 안의 `//`, 길이와 줄 보존, 그리고 배포된 Skeleton이 정확히 다섯 개의 Control로 Parsing되는 것을 포함합니다. 유지 Case가 더 중요합니다 — Literal을 먹어치우는 Stripper는 올바른 Code를 망가뜨립니다.
