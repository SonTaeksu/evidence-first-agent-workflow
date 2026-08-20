# Skeleton — DevExpress WinForms

이 Stack에는 Skeleton을 제공하지 않습니다.

미뤄 둔 것이 아니라 의도한 것이고, 여기서는 그 이유가 구체적입니다. DevExpress Assembly는
License가 걸린 의존성이고 이 Profile을 작성한 환경에서는 쓸 수 없었으므로, Skeleton이
Compile된다는 것을 확인할 방법이 없었습니다. 아무도 Build해 보지 않은 Skeleton은
부채입니다. 권위 있어 보이고, 복사되고, 결함은 처음 실제로 쓰일 때 발견됩니다.

[`../../csharp-winforms/skeletons/MinimalApp/`](../../csharp-winforms/skeletons/)의 순수
Windows Forms Skeleton은 실재하며 실제로 Compile됩니다. DevExpress Project에서 DevExpress가
아닌 부분 — Project File, Runtime 구성, Manifest, Entry Point, 그리고 Behaviour와 Designer가
생성한 Layout의 분리 — 의 올바른 출발점입니다.

DevExpress Skeleton을 추가할 때는 그것을 만들어 낸 Build 명령과 Exit Code, 그리고 어떤
DevExpress Release를 대상으로 Build했는지를 함께 가져와야 합니다.

## 여기 들어갈 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주 틀리는 곳이기
  때문입니다;
- 범위가 아니라 해석된 Version을 가진 DevExpress 참조;
- Build가 실제로 요구한 Licensing Artifact가 무엇이든 그것, 그리고 License가 그 Machine에
  어떻게 도달했는지에 대한 설명;
- 생성되는 File이 따라야 하는 관례마다 예시 하나씩.

## 담으면 안 되는 것

- 작성 시점에 최신이었던 DevExpress Version을 고정해 놓고 그것을 요구 사항처럼 제시하는 것;
- Project가 선택하지 않은 Control. 그러면 Skeleton은 출발점이 아니라 결정이 됩니다;
- License Key, License File의 내용, 그 밖에 Kit의 자료가 아니라 조직의 사용 권한에 속하는
  모든 것.
