# Stack 전용 Agent Rule — DevExpress WinForms

이 File은 Root `AGENTS.md`와 `../csharp-winforms/AGENTS.stack.md`를 **함께** 확장합니다.
둘 중 어느 쪽도 반복하지 않습니다.

순수 WinForms 규칙을 먼저 읽습니다. Designer 소유권, UI Thread 경계, DPI 구성, Project
Format, Build 명령 분기는 여기서도 그대로 적용됩니다 — DevExpress Control도 여전히
Windows Forms Control입니다. 이 File은 DevExpress가 그 위에 더하는 것만 담습니다.

- Stack에 의존하는 구현을 시작하기 전에 `STACK-READINESS.json`을 읽습니다.
- Blocking Capability의 상태가 `unknown`이면 그에 의존하는 Pattern은 금지입니다.
  "조심해서 진행"이 아니라 금지입니다.
- 문서 조회는 `mcp/source-routing.md`를 통해 라우팅합니다. DevExpress에 대해서는 `dxdocs`가
  권위 있고, Windows Forms와 .NET에 대해서는 `microsoft-learn`이 권위 있으며 DevExpress에
  대해서는 어떤 권위도 없습니다.
- 기억 대신 `references/verified-facts.md`와 `references/pitfalls.md`를 사용합니다. 그 안의
  모든 항목은 어디서 확인했는지를 밝히고 있습니다.
- 선택한 Capability는 모두 Project Map에 기록하고 Gate Analysis에서 다시 언급합니다.

## Stack 금지 사항

- DevExpress API 질문에 `microsoft-learn`, 일반 Package 문서 Server, 또는 기억으로 답하지
  않습니다. Microsoft Learn은 서드파티 Control Library를 문서화하지 않으므로, 대신 가장
  비슷한 Windows Forms Type에 대해 답합니다 — 자신만만하게, 그리고 다른 Control에 대해서.
- DevExpress Type이 이름이 비슷한 `System.Windows.Forms` Type처럼 동작한다고 가정하지
  않습니다. 닮은 것은 이름뿐이고 Member 집합은 같지 않으며, 그대로 옮겨 온 가정은 무관해
  보이는 이유로 Compile되거나 실패합니다.
- 이번 Session에서 조회하지 않은 DevExpress Version 번호, Member 이름, Enumeration 값,
  Namespace를 쓰지 않습니다. 이 Kit이 막으려고 존재하는 바로 그 실패이며, Member가 수천 개인
  Control Library가 그 일이 가장 자주 일어나는 곳입니다.
- `GridControl`에 Grid 동작을 구성하지 않습니다. Control은 Data를 갖고 View가 Behaviour를
  갖습니다. 잘못된 Object를 대상으로 쓴 Code는 Compile되고 조용히 아무 일도 하지 않습니다.
- `LayoutControl`의 자식을 좌표로 배치하지 않습니다. 위치는 Layout Item이 소유하며, 그
  대입은 Error 없이 버려집니다.
- Skin이 적용된 Form에 색상이나 Font를 하드코딩하지 않습니다. 외관은 Skin이 결정하며,
  Control 수준의 재정의는 무시되거나 아니면 Application에서 혼자만 다른 Control 하나를
  만들어 냅니다.
- Designer가 생성한 Code를 수기 편집하지 않습니다. DevExpress Form은 그것을 더 적게가 아니라
  더 많이 생성하며, Designer는 그 전부를 다시 씁니다.
- 이 Stack을 v24.2 미만에 적용할 수 있다고 취급하지 않습니다. 경계가 거기 있는 이유는
  `README.md`에 있습니다.
- 명령과 Exit Code 없이 Validation이 통과했다고 보고하지 않습니다.
- Owner를 대신해 `STACK-INPUTS.md`의 행을 채우지 않습니다. 답변되지 않은 입력은 Blocked
  Stack이며, 그것은 올바른 상태입니다.
