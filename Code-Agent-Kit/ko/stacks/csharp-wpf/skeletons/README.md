# Skeleton — WPF (.NET Framework 4.7.2+)

이 디렉터리 아래에 최소 Skeleton이 들어 있습니다.

**아직 Compile해 본 적은 없습니다.** 이것을 작성한 환경에는 MSBuild도 .NET Framework
Targeting Pack도 없었으므로, 정직하게 할 수 있는 진술은 File이 존재하고 서로 앞뒤가
맞는다는 것뿐입니다. Toolchain이 있는 Machine에서 한 번 Build하고 그 명령과 Exit Code를
`STACK-INPUTS.md`에 기록하십시오. 그러면 이것은 주장에서 Evidence가 됩니다.

## 여기 들어갈 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project 또는 Manifest File. Version에 민감한 설정이 사는 곳이자 가장 자주
  틀리는 곳이기 때문입니다;
- 생성될 File이 따라야 하는 각 관례의 예시 하나씩.

## 담아서는 안 되는 것

- 작성 당시 최신이었을 뿐인 Version을 고정해 놓고 그것을 요구 사항처럼 제시하는 것;
- Project가 선택하지 않은 Library. 그러면 Skeleton이 출발점이 아니라 결정이 됩니다.
