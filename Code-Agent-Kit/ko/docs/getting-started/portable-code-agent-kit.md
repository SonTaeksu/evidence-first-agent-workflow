# Portable Code Agent Kit 구조

`Code-Agent-Kit/en/`과 `Code-Agent-Kit/ko/`는 상대 경로가 같고 각각 독립적으로 복사할 수 있는 배포본입니다.

각 Mirror 포함 범위:

- 운영 Root File 및 Hidden Agent Adapter
- `docs/core`, `docs/architecture/decisions`, `docs/getting-started`, `docs/agents`, `docs/human`
- Prompt, Template, Stack, Tool, Script, Demo, Reference Asset, Agent Config, Sample, License

Portable Kit에서 제외:

- 과거 Design Review 및 Evaluation 보고서
- Repository Release Note, Changelog, Update Manifest, Citation Metadata
- 생성된 Validation Evidence
- 자동 활성화되는 `.github/workflows`

비활성 CI Sample은 `templates/ci/github/`에 둡니다.

Mirror는 상대 경로 완전 일치, `.md` 부재, 선택 언어 Root 밖으로 나가는 Link 부재를 검사합니다.
