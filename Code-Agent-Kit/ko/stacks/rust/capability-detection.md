# Capability Detection — Rust

Capability는 Repository에서 Detection하며 절대 가정하지 않습니다. Detection이 확정적이지
않을 때 적용되는 것이 Unknown Rule이고, 추측 대신 차단합니다. 한 번의 잘못된 추측이
잠시 멈추는 것보다 비쌉니다.

| Capability | Detection | Present 경로 | Absent 경로 | Unknown Rule |
|---|---|---|---|---|
| edition-and-msrv | `Cargo.toml`의 `edition`과 `rust-version`, 그리고 `rustc --version` | 그 범위 안에서 답변 | Owner에게 확인 | edition에 민감한 문법 요소 차단 |
| async-runtime | `Cargo.toml`의 Runtime Crate와 Code에 쓰인 그 Attribute Macro | 그것만 사용 | Owner에게 확인 | Async 작업 전면 차단 |
| web-framework | Framework Crate와 그 Router 연결 | 그것을 사용 | Owner에게 확인 | Framework 도입 차단 |
| error-model | Error Crate와 그 Crate의 공개 Error Type | 그것을 따름 | Owner에게 확인 | Error Model 혼용 차단 |
| data-access | Driver 또는 ORM Crate와 그 Migration | 그것을 사용 | Owner에게 확인 | Data 접근 방식을 지어내는 것 차단 |

Feature가 의존하는 모든 Capability는 Project Map에 나타나야 하고 Gate Analysis에서 다시
언급되어야 합니다. 나중에 읽는 사람이 어느 갈래를 왜 택했는지 볼 수 있어야 하기 때문입니다.
