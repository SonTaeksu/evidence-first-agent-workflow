# Pitfall — ASMX Web Service 2.0 (.NET Framework 4+)

여기 있는 것은 모두 기술 자체의 속성이며 어떤 Project와도 무관하게 검증할 수 있습니다.
한 가지 공통점 때문에 모아 두었습니다. **실패가 조용하거나, Error Message가 원인이 아닌
다른 것을 가리킨다는 점입니다.** 실패가 스스로 드러나는 Stack에는 이런 목록이 필요 없습니다.

## XmlSerializer는 Member를 조용히 빠뜨린다

Public Setter가 없는 Member나 무인자 생성자가 없는 Type은 아무런 오류 없이 전송 형식에서 빠집니다. 그 Field는 기본값으로 도착하고, 정상적인 Data처럼 보입니다.

## Interface와 Generic은 직렬화되지 않는다

`interface` Type이거나 열린 Generic인 Member는 Schema로 표현할 수 없습니다. 이것은 Build 시점이 아니라 첫 호출 때 Runtime 직렬화 Exception으로 드러납니다.

## Nullable 값 Type

`Specified` Pattern이 없으면 `0`과 '보내지 않음'이 같은 Message입니다. 값의 부재로 분기하는 Logic은 모두 틀립니다.

## Proxy 재생성

다시 생성한 Proxy는 수정을 덮어씁니다. WCF와 똑같습니다. 조정은 Wrapper에서 합니다.

## Legacy라는 상태는 제약이지 가치 판단이 아니다

새 API와 Framework 기능은 ASMX에 추가되지 않습니다. 더 최신 Stack의 Pattern을 그대로 가져와 지원된다고 넘겨짚지 말고, 조회해서 확인하십시오.
