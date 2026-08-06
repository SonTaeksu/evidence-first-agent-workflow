# Communication Contract — Next.js

## 이 Stack이 노출하거나 소비하는 Interface

`⟨확인 필요: 이 Project가 소유한 Contract, 그리고 그중 Repository 밖에 Consumer가 있는
것이 무엇인지⟩`

외부 Consumer가 있는지 여부가 변경을 제자리에서 해도 되는지, 아니면 추가 방식으로만
해야 하는지를 결정합니다. 이것은 누구도 Code만 보고 추론할 수 없습니다.

## 항상 성립하는 규칙

- Contract를 바꾸는 것은 그 Contract의 모든 Consumer를 바꾸는 것입니다. 한쪽만 재생성하면
  Build 실패가 아니라 Runtime 실패가 납니다.
- Generated Client는 재생성하는 것이지 편집하는 것이 아닙니다. 조정은 손으로 쓴 Wrapper에
  두어야 합니다. 다음 재생성이 편집한 내용을 조용히 버리기 때문입니다.
- 호출자가 분기해서 처리해야 하는 Error는 Contract의 일부여야 합니다. 선언되지 않은 Error는
  일반적인 형태로 도착하고 처리할 수 없습니다.
