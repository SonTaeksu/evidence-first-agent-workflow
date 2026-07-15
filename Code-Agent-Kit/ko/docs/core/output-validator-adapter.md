# Output Validator Adapter Contract

Core는 Generic Screen 및 Build Log 검사를 제공합니다. Stack Pack은 Framework 고유 Generated File, Binding, Log, Runtime Artifact Validator를 추가할 수 있습니다.

Stack Validator 요구사항:

- 명시적 Input Path
- 가능한 경우 Machine-readable Evidence
- PASS `0`, Validation 실패 `2`, Tool Error `1`
- Compile, Rendered Output, Runtime 실패 구분
- 검사 Artifact를 수정하지 않음
- 정상 1개와 의도적 실패 1개의 Self-test

예:

- Generator Log Error Scan
- 필수 XML/Project Node 검사
- Data Binding 존재
- 빈 Grid/Card 검사
- Generated Client Freshness
- DTO/Data Model 동기화
