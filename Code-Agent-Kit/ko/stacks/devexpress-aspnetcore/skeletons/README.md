# Skeletons — DevExpress for ASP.NET Core

이 Stack에는 Skeleton이 제공되지 않습니다.

그것은 보류가 아니라 의도이며, 여기서는 불가피하기도 합니다. 아무도 만들어 보지 않은
Skeleton은 부채입니다. 권위 있어 보이고, 복사되며, 그 첫 실제 사용처가 결함이 발견되는
곳이 됩니다. DevExpress Package는 **자격 증명이 필요한 Private Feed**에서 오므로, 이
Stack의 Skeleton은 이 Kit이 가지고 있지도 않고 배포할 수도 없는 사용 권한 없이는 만들 수도
— 읽는 사람이 확인할 수도 — 없습니다.

Restore된 적도, Compile된 적도, Rendering된 적도 없는 Skeleton은 이 Kit이 막으려고 존재하는
바로 그 지어낸 자료가 될 것입니다.

하나가 추가될 때는 그것을 만들어 낸 Build 명령과 Exit Code, 그리고 그것이 대상으로 삼은
DevExpress Version과 함께 와야 합니다.

## 여기의 Skeleton이 담아야 하는 것

- Build되고 실행되는 가장 작은 것;
- Project File. Target Framework와 DevExpress Package Version이 사는 곳이며, 가장 자주
  틀리는 곳이기 때문입니다;
- Feed 설정. 자격 증명은 박아 넣지 않고 참조합니다;
- Skeleton의 범위에 Reporting이 있다면 Reporting에 필요한 Service 등록 — 그것을 빠뜨리는
  것이 동작하는 참조물을 망가진 것으로 만드는 가장 흔한 방법이기 때문입니다;
- 같은 이유로 Asset 전달;
- 생성되는 파일이 따라야 하는 각 관례의 예시 하나씩.

## 담아서는 안 되는 것

- 라이선스 키, 자격 증명, 또는 그것을 담고 있는 Feed URL;
- 작성 당시 현행이던 Version에 고정된 값을 요구 사항인 것처럼 제시하는 것;
- Server-side와 Client-side 제품군의 Component를 섞은 것. 그것은 Skeleton을
  `references/pitfalls.md`가 첫머리에 말하는 바로 그 혼동의 근원으로 만듭니다;
- Project가 선택하지 않은 라이브러리. 그것은 Skeleton을 출발점이 아니라 결정으로 만듭니다.
