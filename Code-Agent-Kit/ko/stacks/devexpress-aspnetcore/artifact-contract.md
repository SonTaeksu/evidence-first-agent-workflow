# Artifact Contract — DevExpress for ASP.NET Core

이 Stack이 무엇을 만들어 내는지, 그리고 그것이 만들어졌다는 Evidence로 무엇이 인정되는지.

## Build 출력

`⟨확인 필요: 이 Project의 Build가 만드는 Artifact와 그 위치 — Compile된 Application,
방출되거나 복사되는 정적 Asset, 그리고 Report 정의가 출력물에 포함되는지 다른 곳에
저장되는지⟩`

이 Stack이 만들어 내는 것 중 Artifact 목록에서 빠뜨리기 쉬운 두 가지:

- Component가 필요로 하는 **Client-side Asset**. 배포되어야 할 것의 일부이며, 이것을
  빠뜨린 배포는 Component 없이 그리고 Error 없이 Rendering되는 페이지를 만듭니다;
- 이 Project가 Assembly 밖에 Report를 저장한다면 **Report 정의**. 그 경우 그것은 Build
  출력이 전혀 아니며, 출력인 것처럼 다루는 것이 배포가 조용히 지난달 Report를 내보내는
  방식입니다.

## Evidence로 인정되는 것

- Build 또는 Test의 **Exit Code**와 그것을 만든 명령. Exit Code가 0이 아닌데 성공이라고
  말하는 Log 줄은 Evidence가 아니라, 이 Kit이 잡아내려고 존재하는 실패 양상입니다.
- DevExpress Package와 관련된 모든 것에 대해 **Feed에 도달한 Restore**. 전부 로컬
  Cache에서 제공된 Restore는 Cache가 그 Package를 가지고 있다는 것을 증명하며, 그것은
  다른 주장입니다.
- 명시된 경로에 실제로 존재하는 파일. `check-stack-readiness`가 Evidence 경로를
  해석하므로, 존재하지 않는 인용 경로는 없는 것으로 취급됩니다.
- 시각적인 것에 대해서는 **실행이 실제로 만들어 낸 Rendering된 문서나 페이지**, 그리고
  기록된 그 실행.

## Evidence가 아닌 것

- 명령 없는 자기 보고.
- 개발 Server의 출력. 개발 Mode의 성공은 Production Build가 동작함을 확립하지 않으며, 이
  Stack에서는 특히 Bundling된 Asset이 Production이 제공하는 방식으로 제공됨을 확립하지
  않습니다.
- 로딩된 페이지. 초기화에 실패한 DevExpress Component는 로딩되는 페이지를 남깁니다.
- 비교할 대상이 없는 Screenshot.
