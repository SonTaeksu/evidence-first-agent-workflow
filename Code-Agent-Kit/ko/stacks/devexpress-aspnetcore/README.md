# DevExpress for ASP.NET Core

ASP.NET Core MVC와 Razor Pages 위의 DevExpress Component, 그리고 Web에 Hosting되는
DevExpress Reporting(XtraReports)입니다. **v24.2 이상만 해당합니다.**

**Blazor는 범위 밖입니다.** DevExpress는 자체 등록·Rendering·수명주기 규칙을 가진 별도의
Blazor Component 제품군을 제공합니다. 이 Profile의 어떤 내용도 그것을 위해 쓰이지
않았으므로, 여기 있는 어떤 서술도 Blazor Project를 다룬다고 취급하지 않습니다.

이것은 **평범한 ASP.NET Core Profile의 대체가 아니라 동반 문서**입니다. Hosting Model,
Routing, Dependency Injection, Configuration, Entity Framework Core 질문은 평범한
ASP.NET Core 질문이며 평범한 ASP.NET Core Source에서 답합니다. 이 Profile이 더하는 것은
평범하지 않은 부분입니다. Private Package Feed, 서로 다른 두 형태로 존재하는 Component
라이브러리, 그리고 무엇이든 Rendering하기 전에 Service 등록과 Client Asset 제공이 필요한
Reporting Stack입니다.

Reporting은 Desktop과 Web에 걸쳐 있습니다. **이 Profile은 Report의 Web Hosting만
다룹니다.** WinForms나 WPF Report Host는 답이 다른 별개의 질문이고, 여기서 답해서는 안
됩니다.

**상태: `blocked`.** 고장 난 것이 아니라 대기 중입니다. `STACK-INPUTS.md`의 Owner 입력이
답변되지 않아 `check-stack-readiness`가 `blocked`를 도출하고, `tools/check-last`는 그
상태의 Stack을 의도적으로 건너뜁니다. Placeholder 때문에 매 실행마다 거짓 경보가 나지
않도록 하기 위해서입니다.

이미 들어 있고 쓸모 있는 것:

- `references/pitfalls.md` — 이 Stack에서 Error Message 없이 일어나는 실패;
- `capability-detection.md` — 이 Project가 실제로 무엇을 쓰는지 알아내는 방법. Server-side
  Control을 쓰는지 Client-side Widget을 쓰는지부터 시작합니다;
- `mcp/source-routing.md` — 어떤 문서 Source가 권위 있고, 어떤 것을 참조하면 안 되며,
  DevExpress MCP Server에 대해 무엇이 확인되었고 무엇이 확인되지 않았는지.

`ready`에 도달하려면 실제로 존재하는 Evidence로 `STACK-INPUTS.md`를 채웁니다. Evidence는
선언하는 것이 아니라 측정하는 것입니다:

```bash
python ../../tools/check-stack-readiness/check_stack_readiness.py --stack .
```
