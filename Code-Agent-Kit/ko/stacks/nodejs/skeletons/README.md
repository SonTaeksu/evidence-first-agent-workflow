# Skeletons — Node.js

이 Stack에는 Skeleton이 함께 제공되지 않습니다.

미뤄 둔 것이 아니라 의도한 것입니다. 아무도 빌드해 본 적 없는 Skeleton은 부채입니다.
권위 있어 보이고, 복사되고, 그 결함은 첫 실사용에서 발견됩니다. 이 Profile을 작성한
환경에는 이 Stack의 Toolchain이 없었고, 따라서 Skeleton이 Compile된다는 것을 확인할
방법이 없었습니다.

나중에 추가한다면 그것을 만들어 낸 Build 명령과 Exit Code를 함께 가져와야 합니다.

## 여기 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version 민감 설정이 사는 곳이자 가장 자주 틀리는 곳이기
  때문입니다;
- 생성될 File이 따라야 하는 관례마다 예시 하나씩.

## 담으면 안 되는 것

- 작성 당시 최신이었다는 이유로 고정된 Version을 요구 사항인 것처럼 제시하는 것;
- Project가 선택하지 않은 Library. 그러면 Skeleton이 출발점이 아니라 결정이 됩니다.
