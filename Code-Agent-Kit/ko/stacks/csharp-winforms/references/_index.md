# C# Windows Forms Reference Index

Task별로 경로를 정합니다. 모든 Reference를 미리 로드하지 않습니다.

| Task 또는 Component | Reference | 필요한 이유 |
|---|---|---|
| Stack 도입 | `../STACK-INPUTS.md`, `../capability-detection.md` | Build 명령이 Project Format에 달려 있습니다 |
| Feature 경계 | `../feature-model.md` | 두 화면이 공유하는 `UserControl`은 공유 의존성입니다 |
| Artifact 생성 | `../artifact-contract.md`, `../skeletons/README.md` | 어떤 File을 Designer가 소유하는지 |
| Layout Evidence | `ui-evidence-contract.md` | Windows Forms에는 Rendered Document가 없습니다 |
| Threading과 Background 작업 | `../communication-contract.md`, `pitfalls.md` | Cross-thread 접근은 Compile Time이 아니라 Runtime에 발생합니다 |
| Scaling과 DPI | `verified-facts.md`, `pitfalls.md` | Manifest 설정이 `App.config`를 무시합니다 |
| 알려진 실패 | `pitfalls.md` | 검증된 실패 양상과 각 실패가 드러나는 단계 |
| Version Fact | `verified-facts.md` | 무엇이 언제 검증되었는지 |
| Build와 Packaging | `../validation/build.md` | Package 관리에 따라 Restore가 다릅니다 |
| UI Gate | `../validation/ui.md` | 여기서 무엇이 Rendered-output Evidence로 인정되는지 |
