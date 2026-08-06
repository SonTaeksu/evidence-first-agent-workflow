# Stack Profile — ASMX Web Service 2.0 (.NET Framework 4+)

.NET Framework 4 이상에서 동작하는 Legacy ASP.NET Web Service(`.asmx`)입니다. Microsoft는 ASMX를 Legacy 기술로 문서화하고 있으며, 여기 있는 이유도 신규 작업을 위해서가 아니라 이미 있는 것을 유지하기 위해서입니다.

## Runtime과 Framework Version

`⟨확인 필요: 정확한 Version. 이 Project의 Manifest와 Validation을 실행하는
Machine의 Toolchain에서 읽을 것⟩`

지원 범위는 Version이 아닙니다. `STACK-INPUTS.md`를 참고하십시오.

## 디렉터리 구조

- `*.asmx` + `*.asmx.cs` — `[WebMethod]` Member를 가진 `[WebService]` Class.
- `Web.config` — ASP.NET Pipeline. Protocol 지원은 여기서 구성합니다.
- Generated Proxy — `wsdl.exe`로 만들거나 'Add Web Reference'로 만든, `SoapHttpClientProtocol`을 상속하는 Proxy.

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

이것들은 기술 자체의 속성이며 Project와 무관하게 성립합니다.

- 직렬화는 `DataContractSerializer`가 아니라 `XmlSerializer`입니다. Type에는 Public 무인자 생성자와 Public Setter를 가진 Member가 필요하고, Private State는 왕복하지 못합니다.
- Contract는 Interface가 아니라 Class입니다. WCF에서와 같은 Interface 기반 Contract는 없습니다.
- Nullable 값 Type에는 `XxxSpecified` 짝 Property Pattern이 필요합니다. 그것이 없으면 값이 없는 것과 기본값을 구별할 수 없습니다.
- WSDL은 Code에서 생성되므로, Signature 변경이 곧 Contract 변경이며 따로 검토할 Artifact가 없습니다.
- SOAP 1.1과 1.2 지원 여부는 구성의 문제이고, Client가 보내야 하는 Request를 바꿉니다.
