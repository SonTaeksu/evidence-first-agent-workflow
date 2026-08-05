# C# Windows Forms Feature Model

- **Feature Unit**: 사용자에게 보이는 화면 하나 — Form 또는 Modal Dialog — 그리고 그 Service 경계, Designer File, Test.
- 같은 화면 State를 공유하는 Action은 한 Feature에 둡니다: load, filter, edit, validate, save, cancel.
- 화면이 독립적으로 실행되거나, Service 경계가 다르거나, Deployment Artifact가 다르거나, 보안 경계가 다를 때는 별도 Feature가 필요합니다.
- 재사용 가능한 `UserControl`은 Behaviour를 소유하고 둘 이상의 화면에서 소비될 때 Feature입니다. 공유 의존성이므로, 변경 시 영향받는 화면을 나열합니다.
- Feature State는 `docs/features/<feature>.current.md`와 그 History, 그리고 활성 Worklog 아래에 존재합니다.

## 선언해야 할 공유 의존성

다음 중 하나의 변경은 영향받는 화면과 실행할 Regression 검사를 나열해야 합니다:

- 둘 이상의 Form에서 사용되는 `UserControl`;
- Form이 호출하는 Service Interface;
- 공통 Base Form 또는 공유 Designer Partial;
- `App.config` 안의 Application 전역 구성;
- 공유 `.resx` 또는 Theme Resource.

## 분해 임계값

Core Gate는 작업이 복잡도 임계값을 넘을 때 Code 이전에 Todo Block List를 요구합니다. 이 Stack에서는 다음 중 하나에 해당하면 Block List를 만듭니다:

- 한 Form에 Data-bound Grid나 List가 둘 이상;
- 영속 State를 바꾸는 사용자 Action이 셋 이상;
- 새 Form에 더해 기존 Service Contract 변경;
- 단일 Control이 아니라 Container 계층을 건드리는 Layout 변경.
