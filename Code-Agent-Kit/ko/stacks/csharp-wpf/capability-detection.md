# Capability Detection — WPF (.NET Framework 4.7.2+)

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결론에 이르지 못할 때 적용되는 것이 Unknown Rule이고, 이 Rule은 추측하는 대신
차단합니다. 잘못된 추측 하나가 멈춰 서는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| mvvm-framework | Project File에 있는 알려진 MVVM Package 참조 | 그 Base Class와 Command를 사용 | 직접 구현한 INotifyPropertyChanged와 승인된 Command Type | Project가 이미 쓰지 않는 Pattern의 도입 차단 |
| dependency-injection | `App.xaml.cs` 또는 Bootstrapper의 Container 등록 | Container를 통해 해석 | Composition Root에서 명시적으로 생성 | Container 도입 차단 |
| ui-automation | XAML의 AutomationProperties 또는 UI Test Project | Automation id로 Assert | View Model로만 Assert | UI 동작을 확인했다는 주장 차단 |
| localization | `*.resx` Satellite Resource 또는 `x:Uid` Markup | 기존 Resource Set에 문자열 추가 | 사유를 기록한 채 Literal 유지 | Localization 방식을 새로 만드는 것 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서
다시 밝혀야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 택했고 왜 그랬는지 알 수
있습니다.
