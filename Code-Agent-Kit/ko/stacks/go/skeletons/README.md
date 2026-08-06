# Skeletons — Go

이 Stack에는 Skeleton이 들어 있지 않습니다.

미뤄 둔 것이 아니라 일부러 넣지 않았습니다. 아무도 Build해 보지 않은 Skeleton은
부채입니다. 권위 있어 보이고, 복사되고, 결함은 첫 실제 사용에서 발견됩니다. 이
Profile을 작성한 환경에는 이 Stack의 Toolchain이 없어서, Skeleton이 Compile된다는
것을 확인할 방법이 없었습니다.

나중에 추가할 때는 그것을 만들어 낸 Build 명령과 exit code를 함께 가져와야 합니다.

## 여기 들어갈 Skeleton이 갖춰야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project File 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주
  틀리는 곳이기 때문입니다;
- 생성되는 File이 따라야 하는 각 관례의 예시 하나씩.

## 들어가면 안 되는 것

- 작성 시점에 최신이던 Version을 고정해 놓고 그것을 요구사항인 것처럼 제시하는 것;
- Project가 고르지 않은 Library. 그것이 들어가는 순간 Skeleton은 출발점이 아니라
  결정이 됩니다.
