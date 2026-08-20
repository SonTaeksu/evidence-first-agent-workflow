# Stack Profile — WCF (.NET Framework 4.7.2+)

WCF 위에서 동작하는 SOAP 및 net.tcp Service이며, .NET Framework 4.7.2 이상을
Target합니다.

## Runtime 및 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는 Machine의
Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

- `I*.cs` — Service Contract. `[OperationContract]` Member를 가진 `[ServiceContract]`입니다.
- `*.svc` / Host Project — IIS Hosting이냐 Self-hosting이냐에 따라 구성이 어디서 오는지가 달라집니다.
- `App.config` / `Web.config` — `<system.serviceModel>`: binding, behavior, endpoint. 동작은 Code가 아니라 여기에 있습니다.
- Generated Client — `svcutil` 또는 Visual Studio Service Reference. 다시 생성하면 수정한 내용을 덮어씁니다.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

기술 자체의 속성이며 Project와 무관하게 성립합니다.

- Contract 변경은 Wire Format 변경입니다. 양쪽 모두를 다시 생성해야 하며, 다시 생성하지 않은 Client는 Build가 아니라 Runtime에 실패합니다.
- `DataContractSerializer`는 `[DataMember]`에 `Order`를 지정하지 않으면 Member를 알파벳순으로 배치합니다. 순서는 Contract의 일부입니다.
- `[FaultContract]`로 선언되지 않은 Exception은 Client에 아무 Detail도 없는 일반 Fault로 도착합니다.
- `InstanceContextMode`, `ConcurrencyMode`, Session 지원은 서로 얽혀 있습니다. 하나만 바꾸면 간헐적으로만 나타나는 동작이 생깁니다.
- Metadata(MEX) 노출은 보안 결과를 동반하는 구성 결정입니다.
