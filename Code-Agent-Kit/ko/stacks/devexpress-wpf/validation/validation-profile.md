# Validation Profile — DevExpress WPF (v24.2+)

## 명령

`⟨확인 필요: 이 Project의 정확한 명령⟩`

이 Stack에서 그 명령이 갖는 형태. 첫 항목이 `../../csharp-wpf`와 구별되는 지점입니다:

- **복원.** DevExpress Package는 Build Machine이 인증을 마쳐야 하는, Licence가 걸린
  Feed에서 옵니다. 여기서의 복원 실패는 다시 시도해 넘어갈 Network 문제가 아닙니다.
  Build가 아무것도 만들지 못했다는 뜻이고, 그 뒤에 나오는 "Build 성공"은 낡은 출력
  디렉터리를 서술하고 있을 뿐입니다.
- Build: Project 자체의 Target Framework를 대상으로 하는 MSBuild. 판정은 Exit Code이며,
  Exit가 0이 아닌데 나오는 `Build succeeded` 줄은 판정이 아닙니다.
- Test: Project에 구성된 Runner. 명령과 Exit Code를 기록합니다.
- UI: 화면 명세를 Rendering된 창과 비교합니다. 비교할 대상이 없는 Screenshot은 Evidence가
  아닙니다.
- **Publish된 출력**: 선택한 Theme이 요구하는 Theme Assembly를, Build가 만들어 낸 출력에서
  나열합니다. Pipeline의 다른 어느 것도 이것을 검사하지 않습니다. 다른 어느 것도 그것이
  필요하다는 사실을 모르기 때문입니다.

## 합격 기준

모든 경우에 **Exit Code**입니다. Exit가 0이 아닌데 성공 Message가 나오면 그것은
실패이고, 그 Message를 판정으로 받아들이는 것이 바로 이 Kit이 막으려고 만들어진
잘못입니다.

## Long-running Process

개발 Server나 Test 대상 Service는 `tools/run-managed-service/run_service.py`(또는
그 PowerShell 짝)로 시작하고 중지합니다. 이 도구는 PID와 시작 시각으로 Process를
추적하며 그 Process Tree만 중지합니다.

이미지 이름으로 Process를 중지하지 마십시오. `Get-Process node | Stop-Process`와
`pkill -f node`는 Agent 자신이 의존하는 MCP Server와 사용자의 무관한 작업까지 함께
죽입니다.

## 결과 기록하기

명령, Exit Code, 그 Machine의 Toolchain Version, **그리고 복원이 해석한 DevExpress
Version**. 마지막 것이 없으면 그 결과를 나중의 무엇과도 비교할 수 없습니다. 그 동작이
속해 있던 Version이 바로 그것이기 때문입니다.
