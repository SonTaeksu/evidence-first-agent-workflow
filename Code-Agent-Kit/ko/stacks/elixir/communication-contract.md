# Communication Contract — Elixir

## 이 Stack이 노출하거나 소비하는 Interface

`⟨확인 필요: 이 Project가 소유한 Contract, 그리고 그중 이 Repository 밖에
Consumer가 있는 것⟩`

외부 Consumer의 존재 여부가 변경을 그 자리에서 해도 되는지 아니면 추가 방식으로만
해야 하는지를 결정합니다. 이것은 Code만 봐서는 누구도 알 수 없습니다.

## 항상 성립하는 Rule

- Contract를 바꾸는 것은 그 Contract의 모든 Consumer를 바꾸는 것입니다. 한쪽만
  다시 생성하면 Build 실패가 아니라 Runtime 실패가 납니다.
- Generated Client는 다시 생성하는 것이지 수정하는 것이 아닙니다. 조정이 필요하면
  손으로 쓴 Wrapper에 둡니다. 다음 재생성이 수정을 조용히 지워 버리기 때문입니다.
- Caller가 분기할 것으로 기대되는 Error는 Contract의 일부여야 합니다. 선언되지 않은
  Error는 일반적인 형태로 도착해서 처리할 수 없습니다.
