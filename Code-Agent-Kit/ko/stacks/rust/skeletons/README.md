# Skeleton — Rust

이 Stack에는 Skeleton이 들어 있지 않습니다.

미뤄 둔 것이 아니라 의도한 것입니다. 아무도 Build해 본 적 없는 Skeleton은 부채입니다.
권위 있어 보이고, 복사되고, 결함은 첫 실사용에서야 드러납니다. 이 Profile을 쓴
환경에는 이 Stack의 Toolchain이 없었으므로, Skeleton이 Compile된다는 것을 확인할
방법이 없었습니다.

Skeleton을 추가할 때는 그것을 만들어 낸 Build 명령과 Exit Code를 함께 가져와야
합니다.

## 여기 들어갈 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주
  틀리는 곳이기 때문입니다;
- 생성될 File이 따라야 하는 각 관례의 예시 하나씩.

## 담아서는 안 되는 것

- 작성 당시 최신이었을 뿐인 Version을 고정해 놓고 그것을 요구 사항처럼 제시하는 것;
- Project가 선택하지 않은 Library. 그러면 Skeleton이 출발점이 아니라 결정이 됩니다.
