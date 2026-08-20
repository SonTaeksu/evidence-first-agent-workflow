# Communication Contract — Vue.js

## 이 Stack이 노출하거나 소비하는 Interface

`⟨확인 필요: the contracts this project owns, and which of them have
consumers outside this repository⟩`

외부 Consumer의 존재 여부가 제자리 변경과 추가 변경 중 무엇을 써야 하는지를 결정합니다. Code만으로는
누구도 추론할 수 없습니다.

## 항상 성립하는 규칙

- Contract 변경은 그 Contract의 모든 Consumer 변경입니다. 한쪽만 재생성하면 Build 실패가 아니라
  Runtime 실패가 납니다.
- Generated Client는 재생성 대상이지 편집 대상이 아닙니다. 수정은 직접 작성한 Wrapper에 둡니다.
  다음 재생성이 편집을 조용히 지웁니다.
- 호출자가 분기할 것으로 기대되는 Error는 Contract의 일부여야 합니다. 선언되지 않은 Error는 뭉뚱그린
  형태로 도착해 처리할 수 없습니다.
