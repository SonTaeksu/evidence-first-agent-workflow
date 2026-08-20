# Communication Contract — DevExpress for ASP.NET Core

## 이 Stack이 노출하거나 소비하는 Interface

`⟨확인 필요: 이 Project가 소유한 Contract, 그리고 그중 어떤 것이 이 Repository 밖에
Consumer를 가지는지⟩`

외부 Consumer가 존재하는지 여부가 변경을 제자리에서 할 수 있는지 추가 방식으로 해야
하는지를 결정합니다. 그것은 Code에서 아무도 추론할 수 없습니다.

이 Stack의 세 가지 Contract는 API처럼 보이지 않기 때문에 놓치기 쉽습니다.

- **Report Storage 주소 지정 체계.** `ReportStorageWebExtension`은 Designer와 Report가
  있는 곳 사이의 Contract입니다. 그것이 내주는 식별자는 링크, 저장된 문서, 사용자
  북마크에 박히므로, Report의 주소 지정 방식을 바꾸는 것은 앞에 Compiler가 없는 파괴적
  변경입니다. `⟨확인 필요: 이 Project의 체계, 그리고 그것에 의존하는 다른 대상⟩`
- **Viewer와 Designer가 제공되는 Endpoint.** 이것들은 Project가 작성하지 않은 Client-side
  Code가 호출합니다. 하나를 옮기거나 이름을 바꾸면 브라우저와의 Contract가 바뀝니다.
  `⟨확인 필요: 이 Project의 Route⟩`
- **Report가 Binding하는 Data.** Report 정의는 Field 이름을 지정합니다. 열 이름을 바꾸거나
  결과 형태를 바꾸면 Report는 Build 시점이 아니라 Rendering 시점에 깨지고, 그 Report는
  보통 Schema 변경과 같은 Review에 있지 않습니다.

## 무관하게 성립하는 규칙

- Contract의 변경은 그 모든 Consumer의 변경입니다. 한쪽만 재생성하고 다른 쪽을 두면
  Build 실패가 아니라 Runtime 실패가 생깁니다.
- Generated Client는 재생성하는 것이지 편집하는 것이 아닙니다. 다음 재생성이 편집을
  조용히 버리므로, 적응은 손으로 쓴 Wrapper에 둡니다.
- 호출자가 분기해야 하는 Error는 Contract의 일부여야 합니다. 선언되지 않은 Error는
  일반적인 무언가로 도착하고 처리할 수 없습니다.
- 브라우저만 소비하는 Contract도 Contract입니다. Build의 어떤 것도 그것을 확인하지
  않으므로, 적어 두는 일이 덜 중요한 것이 아니라 더 중요해집니다.
