---
name: devexpress-winforms
description: DevExpress WinForms Control 작업을 구현하거나 검증할 때 이 Skill을 사용합니다. v24.2 이상이 대상입니다. csharp-winforms Skill의 대체가 아니라 그것에 동반하는 Skill입니다.
---

# Stack Skill Router — DevExpress WinForms

가장 관련 있는 최소 문서로 라우팅합니다. Core Workflow는 여기서 반복하지 않고, 순수
Windows Forms Profile도 반복하지 않습니다.

## 항상 읽기

- `../csharp-winforms/STACK.md`와 `../csharp-winforms/AGENTS.stack.md` — 이 Stack이 그
  위에 얹히는 기반 규칙
- `STACK.md`
- `AGENTS.stack.md`
- `mcp/source-routing.md`
- `validation/validation-profile.md`

## Task Routing

| Task | 읽을 것 |
|---|---|
| 새 Feature | `feature-model.md`, 그다음 `capability-detection.md` |
| Grid 작업 | `references/pitfalls.md`, 그다음 `dxdocs`로 Member 조회 |
| Ribbon, Bar 등 모든 Command 표면 | `capability-detection.md`, 그다음 `dxdocs` |
| Layout 변경 | `references/pitfalls.md`, `artifact-contract.md` |
| Skin, Theme, 외관 | `references/pitfalls.md`, 그다음 `dxdocs` |
| Threading 또는 Background 작업 | `../csharp-winforms/communication-contract.md` |
| Contract 또는 Interface 변경 | `communication-contract.md`, `artifact-contract.md` |
| Version에 민감한 모든 것 | `references/verified-facts.md`, 그다음 `dxdocs24_2`로 조회 |
| Licensing 또는 Agent에서만 실패하는 Build | `capability-detection.md`, `validation/validation-profile.md` |
| Debugging | `references/pitfalls.md` — 이 Stack의 실패는 대부분 조용합니다 |
| 결과 보고 | `evidence-provenance.md` |
