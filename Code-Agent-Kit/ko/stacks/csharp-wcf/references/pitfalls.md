# Pitfall — WCF (.NET Framework 4.7.2+)

여기 있는 것들은 모두 기술 자체의 속성이고 어떤 Project와도 무관하게 확인할 수
있습니다. 한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, 오류
Message가 원인이 아닌 다른 것을 가리킨다는 점입니다.** 실패가 스스로를 알리는
Stack이라면 이런 목록이 필요 없습니다.

## binding 구성은 이름으로 해석된다

endpoint의 `bindingConfiguration`은 이름으로 대응됩니다. 오타가 나도 오류가 아니라 그 binding 종류의 기본 binding이 대신 쓰이고, Timeout과 Message 크기와 보안이 조용히 바뀝니다.

## 재생성은 수기 편집을 덮어쓴다

Generated Proxy에 가한 수정은 다음 재생성 때까지만 살아 있다가 사라집니다. 조정은 손으로 쓴 Wrapper에 두고, Generated Code에는 절대 두지 않습니다.

## 선언되지 않은 Fault는 Detail을 잃는다

Caller에게는 Typed Detail이 없는 `FaultException`만 보이므로 그 실패를 특정해서 처리할 수 없습니다. Caller가 분기할 것으로 기대되는 모든 Fault에 `[FaultContract]`를 선언합니다.

## MaxReceivedMessageSize 기본값

기본값이 작습니다. Payload가 그 값을 넘어서면 전송 단계에서 실패하는데, Message는 크기가 원인이라는 것을 알려 주지 않습니다.

## Serializer 선택

`DataContractSerializer`와 `XmlSerializer`는 같은 Type에 대해 서로 다른 Wire Format을 만듭니다. 어느 쪽이 적용되는지는 Attribute에 달려 있으니 가정하지 않습니다.
