---
name: devexpress-aspnetcore
description: DevExpress for ASP.NET Core Stack에서 작업을 구현하거나 Validation할 때, Web에 Hosting되는 DevExpress Reporting을 포함해 이 Skill을 사용합니다.
---

# Stack Skill Router — DevExpress for ASP.NET Core

가장 작은 관련 문서로 라우팅합니다. Core Workflow는 여기서 되풀이하지 않습니다.

## 항상 읽을 것

- `STACK.md`
- `AGENTS.stack.md`
- `mcp/source-routing.md`
- `validation/validation-profile.md`

## 작업 라우팅

| 작업 | 읽을 문서 |
|---|---|
| 새 Feature | `feature-model.md`, 그다음 `capability-detection.md` |
| DevExpress Component 추가 또는 변경 | `capability-detection.md`를 먼저 — Server-side Control인지 Client-side Widget인지는 사소한 사항이 아닙니다 |
| Report Hosting, Viewer, Designer에 관한 모든 것 | `capability-detection.md`, 그다음 `dxdocs`로 조회 — Reporting에는 `AspNetCore` 하나가 아니라 `technologies: ["AspNetCore", "XtraReports"]`가 필요합니다 |
| Report Storage, Report 열기 또는 저장 | `references/pitfalls.md`, 그다음 `communication-contract.md` |
| Package Restore 또는 Feed 실패 | `STACK.md`의 "Package Source" 항목, 그다음 `validation/validation-profile.md` |
| 평범한 ASP.NET Core, EF Core, .NET 질문 | `mcp/source-routing.md` — 이것은 `dxdocs`가 아니라 `microsoft-learn`으로 갑니다 |
| Contract 또는 Interface 변경 | `communication-contract.md`, `artifact-contract.md` |
| Version에 민감한 모든 것 | `references/verified-facts.md`, 그다음 `dxdocs`로 조회 |
| Debugging | `references/pitfalls.md` — 이 Stack의 실패는 대부분 조용합니다 |
| 결과 보고 | `evidence-provenance.md` |
