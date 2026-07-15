# 기여 안내

[English](CONTRIBUTING.md) | **한국어**

다음과 같은 기여를 환영합니다.

- 실패한 도입 사례
- 결정론적 게이트 개선
- 프로젝트 상태 처리 방식의 수정
- 새로운 스택 프로필
- 대조군/적용군 비교 결과
- 번역

## Pull Request를 열기 전에

1. 핵심 워크플로우가 특정 기술 스택에 종속되지 않도록 합니다.
2. 스택 전용 규칙은 `stacks/<stack-name>/` 아래에 둡니다.
3. 고객, 회사, 고용주, 비공개 프로젝트 정보를 포함하지 않습니다.
4. Validation 증거를 첨부합니다.
5. 샘플을 수정했다면 `current.md`, `history.md`, Project Map을 갱신합니다.
6. 최종 Git Diff에서 예상하지 못한 파일이 변경됐다면 그 이유를 설명합니다.

## 새로운 스택 프로필 규격

새 스택 프로필은 다음 파일을 제공해야 합니다.

```text
STACK.md
AGENTS.stack.md
mcp/source-routing.md
validation/validation-profile.md
```

첫 Pull Request에서 샘플 애플리케이션은 선택 사항이지만, 가능하면 함께 제공하는 것을 권장합니다.

## 피드백은 라이선스 의무가 아닙니다

프로젝트가 아직 검증 단계이므로 피드백을 요청합니다. 이 요청은 라이선스에 별도 의무를 추가하지 않습니다.
