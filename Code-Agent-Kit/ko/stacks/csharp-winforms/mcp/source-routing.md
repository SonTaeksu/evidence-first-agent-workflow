# Source Routing

## 공식 Source

- Windows Forms, C#, .NET Framework, MSBuild, 구성 Schema: Microsoft Learn.
- Version 민감 동작 변경에 대한 .NET Framework Release Notes.
- Build Machine에 설치된 SDK, Targeting Pack, Reference Assembly.

## MCP Server

- `System.Windows.Forms`, `System.Drawing`, `System.Configuration`, MSBuild Property, Framework Version 동작과 관련된 모든 것은 Microsoft Learn MCP.
- Windows Forms 질문을 일반 Package 문서 Server로 보내지 않습니다. Windows Forms는 Package가 아닙니다.

## 우선순위

1. 현재 Project Code, Project File, Generated Designer File.
2. 결정론적 Build, Test, Designer-tree Evidence.
3. MCP를 통한 Microsoft Learn.
4. 공식 Release Notes와 .NET Repository.
5. Model Memory.

## Version 민감 조회

기억하지 말고 항상 조회합니다:

- 어떤 Framework Version이 특정 API나 구성 Key를 도입했는지;
- 구성 Key나 Manifest 식별자의 정확한 철자;
- Property가 .NET SDK 소속인지 .NET Desktop SDK 소속인지;
- Framework Version 사이에 달라진 기본값.

## Fallback

Project의 Target Framework가 Source가 서술하는 Version과 다르면 **멈추고 불일치를 보고합니다**. 문서가 우연히 보여준 Version을 대상으로 구현하지 않습니다. 해결되지 않은 항목은 `⟨확인 필요: 무엇을 어떻게 확인할지⟩`로 기록합니다.
