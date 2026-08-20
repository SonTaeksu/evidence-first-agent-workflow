# Communication Contract — Go

## 이 Stack이 제공하거나 사용하는 Interface

`⟨확인 필요: 이 Project가 소유한 Contract, 그리고 그중 이 Repository
바깥에 Consumer가 있는 것⟩`

외부 Consumer의 존재 여부가 변경을 제자리에서 해도 되는지, 아니면 추가 방식으로만
해야 하는지를 결정합니다. 이것은 코드만 봐서는 누구도 알 수 없습니다.

## 언제나 성립하는 규칙

- Contract를 바꾸는 것은 그 Contract의 모든 Consumer를 바꾸는 일입니다. 한쪽만
  다시 생성하고 다른 쪽을 두면 Build 실패가 아니라 Runtime 실패가 납니다.
- Generated Client는 다시 생성하는 것이지 손으로 고치는 것이 아닙니다. 다음 재생성
  때 수정이 조용히 사라지므로, 적응 코드는 직접 작성한 Wrapper에 둡니다.
- Caller가 분기해서 처리해야 하는 Error는 Contract의 일부여야 합니다. 선언되지 않은
  Error는 뭉뚱그려진 형태로 도착해서 처리할 수 없습니다.
