# Stack Profile — DevExpress for ASP.NET Core

ASP.NET Core MVC와 Razor Pages 위의 DevExpress Component, 그리고 Web에 Hosting되는
DevExpress Reporting입니다. v24.2 이상. Blazor는 범위 밖이며 `README.md`를 참고합니다.

## Runtime과 Framework Version

`⟨확인 필요: 정확한 .NET Target Framework, Validation을 수행하는 머신의 .NET SDK,
그리고 정확한 DevExpress Package Version — 이 Project의 Project File과 Restore 출력에서
읽을 것⟩`

지원 범위는 Version이 아니며, "v24.2 이상"은 범위입니다. DevExpress Version은 어떤
Component가 존재하는지, 그중 무엇이 현행이고 무엇이 대체되었는지를 결정하고, 그와는
별개로 `mcp/source-routing.md`의 문서 Endpoint를 고정할 수 있는지 자체를 결정합니다.
`STACK-INPUTS.md`를 참고합니다.

## 디렉터리 구조

아래 형태는 ASP.NET Core의 형태입니다. Service가 등록되는 곳을 제외하면 여기서
DevExpress 고유인 것은 없습니다.

- Application 진입점, Service가 등록되는 곳 — Report Designer와 Document Viewer는 명시적
  등록 없이는 동작하지 않으므로, 이 파일은 모든 Reporting 변경에서 핵심을 지탱합니다;
- `Controllers/`와 `Views/`, 또는 `Pages/`, 또는 둘 다 — 이 Project가 어느 쪽을 쓰는지는
  가정이 아니라 Detection된 Capability입니다;
- Layout과 Bundling 또는 Asset 설정 — DevExpress Component는 Client-side Asset이
  전달되어야 하고, 그 메커니즘은 Project마다 다릅니다;
- Report 정의가 있는 위치. 그 위치는 Project의 결정이며,
  `ReportStorageWebExtension`이 그것을 대상으로 작성됩니다.

`⟨확인 필요: 이 Project의 실제 구성. Report 정의가 어디에 저장되는지, 그리고 그것이
Compile되어 들어가는지 Disk에 있는지 Database에 있는지 포함⟩`

## Package Source

DevExpress Package는 **자격 증명이 필요한 Private NuGet Feed**에서 옵니다. 이것은 특정
Project가 아니라 제품의 성질입니다.

여기서 따라 나오는 것, 그리고 Project가 가정하지 말고 확인해야 하는 것:

- 이 Project가 어느 Feed URL에서 Restore하는지;
- 개발자 머신에서 자격 증명이 어디서 오는지, 그리고 별개로 Build Agent에서는 어디서
  오는지 — 보통 같은 메커니즘이 아닙니다;
- 따뜻한 Package Cache 없는 깨끗한 Restore가 실제로 성공하는지.

`⟨확인 필요: Validation을 실행하는 머신에서 위 세 가지 모두⟩`

## Build 명령

`⟨확인 필요: 이 Project 자체의 Build 명령과 그 통과 기준⟩`

무엇이든 간에, 전부 Cache에서 Restore한 Build는 Feed를 검증하지 않았습니다. 이것이 CI에
가장 먼저 도달하는 실패이기 때문에 말할 가치가 있습니다.

## Test 명령

`⟨확인 필요: 이 Project 자체의 Test 명령과 그 통과 기준⟩`

## 알려진 제약

이것들은 기술 자체의 성질이며 Project와 무관하게 성립합니다.

- **DevExpress for ASP.NET Core는 두 가지 형태로 존재합니다.** Server에서 Rendering되고
  설정되는 tag helper를 가진 Server-side Control이 있고, 브라우저에서 JavaScript로
  설정되는 DevExtreme의 Client-side Widget이 있습니다. 설정 표면도 문서도 다른 별개의
  제품입니다. Project가 어느 쪽을 쓰는지는 Detection해야 할 사실이며, 한 Project가 두
  가지를 다른 곳에서 함께 쓸 수도 있습니다.
- **Report Designer와 Document Viewer는 명시적 Service 등록이 필요합니다.** Package를
  참조한다고 활성화되지 않습니다. 등록을 빠뜨린 Host는 보통 Build 시점이 아니라 요청
  시점에 실패합니다.
- **또한 Client-side Asset이 전달되어야 합니다.** Viewer와 Designer는 브라우저
  Component입니다. 필요한 정적 또는 Bundling된 리소스가 제공되지 않으면 페이지는 그것들
  없이 Rendering되고 Server는 아무것도 보고하지 않습니다.
- **Report Storage는 Project가 구현하는 것입니다.** `ReportStorageWebExtension`은
  확장점이지 동작하는 기본값이 아닙니다. Project가 하나를 제공하기 전까지 Designer는
  Report를 열 곳도 저장할 곳도 없습니다.
- **Reporting은 Desktop과 Web에 걸쳐 있습니다.** 이 Profile은 Web Host를 다룹니다.
  WinForms나 WPF Host는 같은 질문에 다르게 답하며 여기서 답해서는 안 됩니다.
- **DevExpress API는 Version이 있고 이 Profile은 조회의 대체물이 아닙니다.** Component
  이름, Property 이름, 등록 호출을 기억으로 서술하지 않습니다. `mcp/source-routing.md`를
  통해 라우팅합니다.
