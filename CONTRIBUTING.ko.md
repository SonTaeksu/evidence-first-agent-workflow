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

`templates/stack-profile/`이 아니라 `stacks/_template/`을 복사하고, Readiness Validator가 요구하는 문서를 전부 채웁니다.

```text
STACK.md                          references/_index.md
STACK-INPUTS.md                   references/pitfalls.md
AGENTS.stack.md                   references/verified-facts.md
SKILL.md                          skeletons/README.md
capability-detection.md           validation/validation-profile.md
feature-model.md
artifact-contract.md              STACK-READINESS.json
communication-contract.md
evidence-provenance.md
```

14개 문서가 전부 존재하고 비어 있지 않아야 합니다. 누락되거나 빈 문서는 경고가 아니라 실패입니다.

```bash
python tools/check-stack-readiness/check_stack_readiness.py --stack stacks/<name>
```

이 명령이 exit 0을 낼 때만 `ready`로 제출합니다. `provisional`과 `blocked`도 정당한 상태이므로, 어느 상태로 제출하는지와 그 이유를 적어 주세요.

자주 걸리는 두 가지:

- **Evidence는 비울 수 없습니다.** 해결된 Input이나 Capability에 Evidence가 없으면 Validation이 실패합니다. 의도한 설계입니다 — 모델 기억으로 채운 Fact를 확인된 것처럼 넘길 수 없게 합니다.
- **`declared_state`가 실제와 맞아야 합니다.** 도출 결과가 `blocked`인 Stack에 `ready`를 선언하는 것 자체가 실패입니다.

첫 Pull Request에서 샘플 애플리케이션은 선택 사항이지만, 가능하면 함께 제공하는 것을 권장합니다.

## 새 검사 추가

결정적 검사는 [`docs/core/gate-design-principles.md`](Code-Agent-Kit/ko/docs/core/gate-design-principles.md)를 만족한 뒤에야 `docs/core/enforcement-matrix.md`에 자리를 얻습니다.

- 산문이 지켜내지 못해서 프로그램으로 옮긴 Rule이다
- 판정이 결정적이고 문구·File 명명에 좌우되지 않는다
- 알려진 정상 산출물을 돌려 발견 0건을 확인했다
- **침묵** 실패는 BLOCK하고, 시끄러운 실패는 WARN이어도 된다
- 면제 경로가 사람이 적은 명시적 Marker이고, 정황에 의한 암묵 면제가 없다
- Tool이 실패 시 자기 Rule ID를 출력한다 — 모델에게 태깅을 시키지 않는다
- 판정 근거가 모델 판단이 아니라 Project 문서다
- 흔한 경우에 Runner가 인자를 요구하지 않는다
- `self_test.py`가 통과 Fixture와 의도적 실패 Fixture를 모두 덮는다
- Runner가 필요한 인자를 실제로 넘기는 것을 실행해서 확인했다
- Exit Code는 통과 `0`, Validation 실패 `2`, Tool 오류 `1`
- 이 검사가 여전히 못 잡는 것을 빼지 말고 ADVISORY 구간에 적었다

`BLOCK`은 오탐 0을 관측한 뒤에만 주장합니다. 거짓 경보가 한 번 나면 운영자는 `--no-verify`를 쓰기 시작하고, 그 뒤로는 Hook 전체가 무력합니다.

표를 좋아 보이게 하려고 ADVISORY 행을 지우지 마세요. ADVISORY 구간은 커버리지 구멍의 목록이고, 그것은 Roadmap과 같은 것입니다.

## 두 언어 Mirror

`Code-Agent-Kit/en/`과 `Code-Agent-Kit/ko/`는 같은 상대 경로를 가집니다. 번역되는 것은 산문뿐이고 Script는 Byte 동일합니다. Pull Request를 열기 전에 확인하세요.

```bash
python Code-Agent-Kit/en/tools/check-mirror-parity/check_mirror_parity.py --root Code-Agent-Kit
python Code-Agent-Kit/en/tools/check-kit-selfcheck/check_kit_selfcheck.py --root Code-Agent-Kit/ko
```

## 피드백은 라이선스 의무가 아닙니다

프로젝트가 아직 검증 단계이므로 피드백을 요청합니다. 이 요청은 라이선스에 별도 의무를 추가하지 않습니다.
