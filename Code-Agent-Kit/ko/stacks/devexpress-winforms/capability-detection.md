# Capability Detection — DevExpress WinForms

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이 확정적이지
않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다. 한 번의 잘못된 추측이
잠시 멈추는 것보다 비쌉니다.

순수 Windows Forms Capability는
[`../csharp-winforms/capability-detection.md`](../csharp-winforms/capability-detection.md)가
서술하는 대로 Detection합니다. Project Format, Package 관리, DPI, Data Access,
Authentication, Localization, Analyzer 정책입니다. 그것들이 여전히 Build 명령을 결정합니다.
아래 표는 DevExpress가 더하는 것입니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | Project File의 DevExpress Package 또는 Assembly 참조를 Lock 또는 Package File로 해석한 것 — 범위가 아님 — 을 Build하는 Machine에 설치된 것과 교차 확인 | 그 Release 안에서 답하고, 조회를 대응하는 고정 Endpoint로 라우팅 | DevExpress Project가 아님; `../csharp-winforms`만 사용 | Version에 민감한 DevExpress API 사용을 모두 차단하고, `dxdocs`와 `dxdocs24_2` Endpoint 중 선택하는 것을 차단 |
| grid-views | Designer File에서 생성되는 Grid Type, 그리고 각 Grid의 생성 Code가 어떤 View Type을 만드는지 | Control이 아니라 Designer가 만든 View에서 Behaviour를 변경 | Grid 없음; Grid 규칙은 적용되지 않음 | Grid Column, 편집, Behaviour 변경 차단 |
| command-surface | Designer File과 Entry Point에서 Ribbon 대 Bar-manager Component | 그 Component가 Item을 두는 곳에 Command 추가 | Form이 순수 Windows Forms Menu 표면을 사용함 | Command 추가, 이동, 삭제 차단 |
| layout-control | Designer File의 Layout-control Instance | Layout Item을 통해 배치 | 순수 Container Layout; 좌표가 적용됨 | Layout 및 위치 변경 차단 |
| skins-and-appearance | Entry Point의 Application 전역 외관 호출, 그리고 Project가 참조하는 Skin Assembly | 구성된 Skin을 유지하고 Control 수준에서 재정의하지 않음 | 기본 외관; 그 결정을 기록 | 외관, 색상, Theme 변경 차단 |
| license-file | Project의 `licenses.licx`, 그것이 Source Control에서 추적되는지, 그리고 Build Agent에 License가 있는지 | Project가 이미 Build하는 방식대로 Build | 재현 가능한 Build를 주장하기 전에 Agent가 어떻게 Compile하는지 확인 | Build가 다른 Machine에서도 재현된다는 주장 차단 |
| designer-generated-code | `InitializeComponent`를 담은 `*.Designer.cs` | Designer가 Layout을 소유하고 Behaviour는 Partial Class에 둠 | Code로 손수 만든 Layout; 그 결정을 기록 | 생성된 Layout의 수기 편집 차단 |
| ui-automation | Test Project의 Automation Harness 참조 | Runtime Evidence에 사용 | Runtime Evidence 경로 없음; Runtime은 사유와 함께 `PENDING`으로 유지 | Runtime Behaviour 주장 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서 다시
언급되어야 합니다. 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수 있어야 하기
때문입니다.

## devexpress-version이 첫 번째 분기인 이유

그것이 어떤 문서 Server가 답하는지를 결정하고, 따라서 이후의 모든 답이 어느 Version을
서술하는지를 결정합니다. Project의 Release 이후에 도입된 Member를 고정되지 않은 Endpoint는
사용 가능한 것으로 문서화하고, 그렇게 나온 Code는 존재하지 않는 것을 대상으로 Compile됩니다.
v24.2 미만에서는 Endpoint를 고정하는 것 자체가 불가능하며, 이 Profile이 거기에 경계를 긋는
이유가 그것입니다.

## Control과 View의 구분이 Detection 질문인 이유

"이 Project가 Grid를 쓰는가"는 쓸모 있는 질문이 아닙니다. "이 Grid의 Designer Code가 어떤
View Object를 만드는가"가 쓸모 있는 질문입니다. Behaviour 설정은 View에 살기 때문에, View
Type을 모른 채 한 변경은 잘못된 Object에 한 변경입니다 — 그리고 그 실패는 조용하며, 그것이
이것을 참고 사항이 아니라 Blocking Capability로 만든 이유입니다.

## license-file이 재현성 주장을 차단하는 이유

DevExpress Assembly는 SDK의 일부가 아니라 License가 걸린 것입니다. 개발자 Machine에서
성공한 Build는 Build Agent에 대해 아무것도 말해 주지 않으며, Licensing 실패는 Licensing
문제처럼 보이는 무언가가 아니라 Build Error나 Runtime Dialog로 나타납니다. 그 경로가
확인되기 전까지 "Build가 통과한다"는 것은 Machine 한 대에 관한 주장입니다.
