# Artifact Contract — DevExpress WinForms

이 Stack이 무엇을 만들어 내는지, 그리고 그것이 만들어졌다는 Evidence로 무엇을 인정하는지.
[`../csharp-winforms/artifact-contract.md`](../csharp-winforms/artifact-contract.md)의 순수
Windows Forms Artifact 규칙은 그대로 적용되며, 이 문서는 DevExpress가 거기에 더하는 것을
기록합니다.

## Build 산출물

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact, 그것이 쓰이는 위치, 그리고 함께 배포되는
DevExpress Assembly⟩`

DevExpress Application은 Component Assembly를 함께 배포합니다. 어떤 것을 배포하는지, 그리고
License가 그것을 허용하는지는 Owner의 Fact입니다 — `licensing` 입력을 참고합니다.

## 소유권

- **Layout은 생성됩니다.** Designer가 `*.Designer.cs`를 소유하고 다시 씁니다. DevExpress
  Form은 순수 Form보다 그 File을 더 적게가 아니라 더 많이 생성하므로, 수기 편집의 유혹은
  더 크고 손실은 똑같습니다.
- **Behaviour는 손으로 씁니다.** Form의 Partial Class에 둡니다.
- **`licenses.licx`는 Source Code가 아니라 Build 입력입니다.** Tooling이 생성하고
  관리합니다. Build를 통과시키려고 손으로 편집하는 것은 Licensing Artifact를 바꾸는 일이며,
  그것은 수정이 아니라 Owner의 결정에 속합니다.
- **Skin 및 외관 구성은 Application 전역입니다.** 그것이 Entry Point에 있는지, 공유 Base
  Form에 있는지, 시작 Module에 있는지는 Project의 Fact이며 `⟨확인 필요: 이 Project가 그것을
  어디서 적용하는지⟩` — 어디에 있든 그곳의 변경은 모든 화면에 영향을 주고, 그 변경은 영향
  받는 화면 목록을 함께 제시합니다.

## Evidence인 것

- 그것을 만들어 낸 명령과 함께 제시된 Build 또는 Test **Exit Code**. Exit Code가 0이 아닌데
  성공했다고 적힌 Log 한 줄은 Evidence가 아니라, 이 Kit이 잡으려고 존재하는 바로 그 실패
  방식입니다.
- 명시된 경로에 실제로 존재하는 File. `check-stack-readiness`가 Evidence 경로를 해석하므로,
  존재하지 않는 경로를 인용하면 없는 것으로 간주됩니다.
- 화면 내용에 대해서는 실행 중인 창이 아니라 Designer Control Tree. Windows Forms에는
  Rendering된 문서가 없고, DevExpress를 더해도 생기지 않습니다. DevExpress Designer File에
  적용되는 한 가지 단서는 `validation/validation-profile.md`를 참고합니다.

## Evidence가 아닌 것

- 명령이 없는 자기 보고.
- 개발자 Machine에서 성공한 Build를 Build Agent도 성공하리라는 증거로 내미는 것. 차이는
  License이고, 그것은 Source에 보이지 않습니다.
- 선언되었지만 부모의 Control Collection에 추가되지 않은 Control. Code에는 있고 화면에는
  없습니다.
- 비교 대상이 없는 Screenshot.
