# Skeleton — ASMX Web Service 2.0 (.NET Framework 4+)

이 Stack에는 Skeleton을 제공하지 않습니다.

미뤄 둔 것이 아니라 의도한 것입니다. 아무도 Build해 보지 않은 Skeleton은 부채입니다.
권위 있어 보이고, 복사되고, 결함은 처음 실제로 쓰일 때 발견됩니다. 이 Profile을 작성한
환경에서는 이 Stack의 Toolchain을 쓸 수 없었고, 따라서 Skeleton이 Compile된다는 것을
확인할 방법이 없었습니다.

Skeleton을 추가할 때는 그것을 만들어 낸 Build 명령과 Exit Code를 함께 가져와야 합니다.

## 여기 들어갈 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주 틀리는 곳이기
  때문입니다;
- 생성되는 File이 따라야 하는 관례마다 예시 하나씩.

## 담으면 안 되는 것

- 작성 시점에 최신이었던 Version을 고정해 놓고 그것을 요구 사항처럼 제시하는 것;
- Project가 선택하지 않은 Library. 그러면 Skeleton은 출발점이 아니라 결정이 됩니다.
