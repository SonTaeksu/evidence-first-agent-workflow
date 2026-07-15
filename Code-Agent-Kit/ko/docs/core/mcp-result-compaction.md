# MCP 및 Retrieval 결과 압축

MCP는 Search 비용을 줄이지만 Context Limit를 없애지는 않습니다.

Retrieval 후:

1. Task에 필요한 Fact만 추출
2. Source, Version, Verification Method 기록
3. 압축 Fact를 Worklog 또는 Stack Provenance에 저장
4. 허용되는 경우 Link 또는 Identifier 유지
5. Retrieval 전체를 Current State에 복사하지 않기
6. 다음 Session에 전체 결과를 다시 넣지 않기

Current State는 검증된 Decision을 기록하고 Retrieval Transcript를 기록하지 않습니다.
