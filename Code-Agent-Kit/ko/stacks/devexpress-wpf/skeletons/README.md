# Skeleton — DevExpress WPF (v24.2+)

이 Stack에는 Skeleton이 함께 들어 있지 않습니다.

그것은 보류가 아니라 의도이며, 여기서는 Licence의 결과이기도 합니다. DevExpress Assembly는
Licence가 걸린 Feed에서 복원되므로, 이 Profile을 작성한 환경에서는 Skeleton을 Build할 수
없었고 설령 Build했더라도 Kit과 함께 배포할 수 없었습니다. 아무도 Compile해 보지 않은
Skeleton은 부채입니다. 권위 있어 보이고, 복사되고, 그 첫 실제 사용처에서 결함이 발견됩니다.

`../../csharp-wpf/skeletons/`에 평범한 WPF Skeleton이 들어 있습니다. Application에서
DevExpress가 아닌 부분의 출발점으로 알맞고, 같은 단서가 붙습니다. 그것 역시 Compile해 본
적이 없습니다.

여기에 Skeleton을 더할 때는 그것을 만들어 낸 Build 명령과 Exit Code, 그리고 복원된
DevExpress Version과 함께 들어와야 합니다.

## 여기 들어갈 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주 틀리는
  곳이기 때문입니다;
- 생성될 File이 따라야 하는 각 관례의 예시 하나씩;
- Theme을 적용하는 지점, 그리고 Theme Assembly가 존재함을 보여 주는 Publish된 출력.
  그것이 없으면 Skeleton은 자기가 막아야 할 실패를 오히려 시연하게 됩니다.

## 담아서는 안 되는 것

- 작성 당시 최신이었을 뿐인 Version을 고정해 놓고 그것을 요구 사항처럼 제시하는 것;
- Project가 선택하지 않은 Library. 그러면 Skeleton이 출발점이 아니라 결정이 됩니다. 이
  Stack에서는 DevExpress MVVM Framework와 제3자 Framework 중 무엇을 쓸지에 대한 선택이
  거기 포함됩니다.
