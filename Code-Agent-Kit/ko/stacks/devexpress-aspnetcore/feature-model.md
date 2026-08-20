# Feature Model — DevExpress for ASP.NET Core

## 하나의 Feature란 무엇인가

`⟨확인 필요: 이 Codebase에서 Owner가 정의하는 Feature 경계⟩`

Kit은 이것을 도출할 수 없습니다. 추측된 Feature 경계는 아무것도 서술하지 못하는 State
문서를 만들고, Project Map은 쓸모없어집니다.

이 Stack에는 Owner가 명시적으로 답해야 하는 경계 질문이 하나 있습니다. 잘못 추측하면
비싸기 때문입니다. **Report 정의는 Feature의 일부인가, 자체 수명주기를 가진 Artifact인가?**
Runtime에 Report Designer로 업무 사용자가 편집하는 Report는 Source Code가 아니며 Feature
Branch와 함께 움직이지 않습니다. Assembly에 Compile되어 들어가는 Report는 함께 움직입니다.
Project는 둘 다 하며, 때로는 같은 Repository 안에서 그렇습니다.

`⟨확인 필요: 이 Project가 둘 중 무엇을 하는지, 그리고 그 사이 경계가 어디에 있는지⟩`

## Feature가 건드릴 수 있는 것

경계가 확인되기 전까지 다음을 작업 규칙으로 삼고, 여기서 벗어나는 모든 경우를 기록합니다.

- 하나의 Feature는 자기 디렉터리 또는 Module을 소유하고, 이미 존재하는 Interface를 통해
  서만 공유합니다;
- 두 Feature가 공유하는 것에 대한 변경은 공유 파일 변경이며 Project Map의 Reverse
  Index에 기록됩니다;
- **Application 시작은 공유됩니다.** Reporting 등록, 정적 파일 설정, Asset 전달이 모두
  거기에 있으므로, Reporting Host나 새 Component를 추가하는 Feature는 공유 영역을 건드리는
  것이며 그 사실을 밝힙니다;
- **Report Storage는 공유됩니다.** Report의 주소 지정이나 저장 방식을 바꾸면 작업 중인
  하나가 아니라 모든 Report에 영향을 줍니다;
- Capability 결정은 그것을 처음 필요로 한 Feature에 속하며, 되풀이하지 않고 기록합니다.

## 이름과 파일 관례

`⟨확인 필요: 이 Project 자체의 관례. Report 정의의 이름을 짓는 방식과 Storage 구현이
그것의 주소를 지정하는 방식 포함⟩`
