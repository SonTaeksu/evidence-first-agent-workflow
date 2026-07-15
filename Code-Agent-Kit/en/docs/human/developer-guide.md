# Developer Guide

## Mental model

The agent does not replace engineering responsibility.

The agent:

- follows a task entry prompt;
- reads small routing documents first;
- gathers evidence;
- implements bounded changes;
- runs deterministic gates;
- updates state for the next session.

The developer:

- chooses direction;
- resolves unknown requirements;
- reviews security and product behavior;
- approves reference assets and visual baselines;
- reviews the final Diff and evidence.

## Standard path

```text
Sync and orient
→ Analysis
→ Task
→ Todo and Micro-Verify
→ Checklist
→ Verification
→ State update
→ Review and commit
```

## Situation router

| Situation | Start with |
|---|---|
| New feature | `prompts/3-new-feature.md` |
| Modify feature | `prompts/4-modify-feature.md` |
| Debug failure | `prompts/6-debug-fix.md` |
| Isolated experiment | `prompts/5-demo-sample.md` |
| Continue in a new chat | active worklog Resume Point |

Every situation starts with `prompts/0-sync-and-orient.md`.

## Source-driven UI work

```text
Image
→ Reference Image Manifest
→ named regions and color evidence

SPA HTML
→ rendered DOM
→ screen specification
→ block and data checklist

Implementation
→ rendered screen specification
→ completeness comparison
→ accessibility and color gates
```

A successful build with empty or missing UI blocks is not complete.

## Reading map

1. Root README
2. Getting Started
3. Core Workflow
4. Prompt Router
5. Stack Profile
6. Sample
7. Pre-commit Validation

This guide explains how to work. It does not override the normative documents.
