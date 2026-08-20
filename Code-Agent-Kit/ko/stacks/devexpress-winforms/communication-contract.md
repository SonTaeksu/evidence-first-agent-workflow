# Communication Contract — DevExpress WinForms

## 이 Stack이 노출하거나 소비하는 Interface

`⟨확인 필요: 이 Project가 소유한 Contract, 그리고 그중 Repository 밖에 Consumer가 있는
것이 무엇인지⟩`

외부 Consumer가 있는지 여부가 변경을 제자리에서 해도 되는지, 아니면 추가 방식으로만 해야
하는지를 결정합니다. 이것은 누구도 Code만 보고 추론할 수 없습니다.

## UI Thread 경계는 상속되며, 다시 적지 않습니다

[`../csharp-winforms/communication-contract.md`](../csharp-winforms/communication-contract.md)에
규칙과 그 근거가 있습니다. Control은 자신을 만든 Thread에 속하고, Background 작업은
`Invoke`나 `BeginInvoke`로 Marshal하며, `InvokeRequired`가 `false`를 반환한다고 그 자체로
허가가 되지는 않습니다. DevExpress Control도 Windows Forms Control이므로 그중 어느 것도
달라지지 않고, 여기서 반복하지도 않습니다.

## DevExpress가 더하는 것

- **Data는 Control을 통해 화면에 도달하고, Behaviour는 View에 구성됩니다.** Data Source를
  Binding하는 것과 그것이 어떻게 표시되는지를 구성하는 것은 서로 다른 두 Object에 대한 두
  가지 작업입니다. Form에 Data Source를 건네는 경계는 그것으로 외관에 관해 아무것도 구성한
  것이 아닙니다.
- **Service는 Data를 반환하며, Control이나 View나 Form을 반환하지 않습니다.** 표시를 위한
  Formatting은 Form 쪽에서 일어납니다. 구성이 끝난 Grid View를 반환하는 Service는 UI를
  Service Layer로 옮긴 것이고, 같은 Data가 필요한 다음 화면은 첫 화면의 표현을 물려받습니다.
- **공유된 외관 또는 Skin 결정은 Contract입니다.** 모든 화면이 그것을 소비하므로, 그것을
  바꾸는 것은 모든 화면을 바꾸는 것이고, 그 변경은 화면 목록을 함께 제시합니다.
- **Error Contract**: Service는 Type이 있는 Exception을 발생시키거나 결과 값을 반환하고,
  사용자에게 무엇을 보일지는 Form이 결정합니다. Grid를 비워 둔 채 삼켜진 Exception은 빈
  결과와 구별되지 않으며, 이 결함 중 가장 오래 살아남는 형태가 바로 그것입니다.

## 항상 성립하는 규칙

- Contract를 바꾸는 것은 그 Contract의 모든 Consumer를 바꾸는 것입니다. 한쪽만 재생성하면
  Build 실패가 아니라 Runtime 실패가 납니다.
- Generated Client는 재생성하는 것이지 편집하는 것이 아닙니다. 조정은 손으로 쓴 Wrapper에
  두어야 합니다. 다음 재생성이 편집한 내용을 조용히 버리기 때문입니다.
- 호출자가 분기해서 처리해야 하는 Error는 Contract의 일부여야 합니다. 선언되지 않은 Error는
  일반적인 형태로 도착하고 처리할 수 없습니다.
