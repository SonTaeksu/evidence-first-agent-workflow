# Capability Detection — DevExpress WPF (v24.2+)

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이
결론에 이르지 못할 때 적용되는 것이 Unknown Rule이고, 이 Rule은 추측하는 대신
차단합니다. 잘못된 추측 하나가 멈춰 서는 것보다 비쌉니다.

`../csharp-wpf/capability-detection.md`의 평범한 WPF Capability도 함께 Detection하며
여기서 반복하지 않습니다. 이 표는 DevExpress 쪽을 더합니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| devexpress-version | Build가 해석한 DevExpress Version — 설치된 제품 목록이 아니라 복원 출력에서 | 그 Version 안에서 답하고, 문서 Server를 그 Version에 고정 | Owner에게 확인 | 모든 DevExpress API 답변 차단, dxdocs와 dxdocs24_2 중 하나를 고르는 것도 차단 |
| mvvm-source | View Model이 어떤 MVVM Base Type을 상속하는지, 그리고 제3자 MVVM Package도 함께 참조되는지 | 이미 쓰고 있는 Framework를 따름 | 도입하기 전에 Owner에게 확인 | 두 번째 MVVM Framework 도입 차단 |
| binding-dialect | 대상 XAML이 DevExpress Binding 및 Command Markup Extension을 쓰는지, 아니면 평범한 Binding과 ICommand를 쓰는지 | 그 File이 이미 쓰는 방언을 유지 | 평범한 WPF Binding 유지 | 한 View 안에서 방언을 섞는 것 차단 |
| theme-deployment | 시작 시 어떤 Theme이 적용되는지, 그것이 어디서 일어나는지, 그리고 Publish된 출력에 어떤 Theme Assembly가 있는지 | 이미 쓰는 Theme을 배포하고 설정 | 기본값을 가정하지 말고 Application에 Theme이 없다고 보고 | Theme 변경 차단, Theme Assembly를 덜어 내는 것도 차단 |
| grid-view | 대상 XAML의 각 GridControl 안에 선언된 View Element | 그 View Type에서 동작을 구성 | Grid가 관여하지 않는 곳에서는 해당 없음 | 다른 View Type을 위해 쓰인 답을 적용하는 것 차단 |
| docking | DevExpress.Xpf.Docking 참조, 그리고 시작 시 저장된 Layout이 복원되는지 | Docking Layout을 통해 Layout을 바꾸고 복원되는 Layout까지 고려 | ../csharp-wpf에 따른 평범한 WPF Layout | 저장 여부에 관한 질문이 답해질 때까지 Layout 변경 차단 |

이 가운데 둘은 Detection을 *왜* 그렇게 썼는지 짚어 둘 만합니다.

`devexpress-version`은 설치된 것이 아니라 Build가 해석한 것에서 읽습니다. 개발자 Machine에는
대개 DevExpress Version이 하나 이상 있고, 설치된 집합은 Build가 쓴 집합이 아닙니다.

`theme-deployment`은 Project File이 아니라 Publish된 출력에서 읽습니다. Theme Assembly는
Runtime에 값으로 적재되고 Compile된 Code의 어느 것도 그것을 참조하지 않기 때문입니다.
Project File이 완전히 옳은 채로 출력에서는 그것이 빠져 있을 수 있고, 그래도 Application은
시작됩니다.

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서
다시 밝혀야 합니다. 그래야 나중에 읽는 사람이 어느 갈래를 택했고 왜 그랬는지 알 수
있습니다.
