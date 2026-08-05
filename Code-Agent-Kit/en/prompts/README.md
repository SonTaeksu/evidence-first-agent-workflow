# Operational Prompt Router

These prompts turn the workflow documentation into repeatable task entry points.

| Situation | Prompt |
|---|---|
| Every task start | `0-sync-and-orient.md` |
| Analyze an existing project | `1-analyze-existing-project.md` |
| Bootstrap a new project | `2-bootstrap-new-project.md` |
| Add a feature | `3-new-feature.md` |
| Modify a feature | `4-modify-feature.md` |
| Create an isolated demo | `5-demo-sample.md` |
| Debug a faulty implementation | `6-debug-fix.md` |
| Update the kit in a project already using it | `7-update-the-kit.md` |
| Fill in or add a tech stack | `8-fill-stack.md` |

Every prompt uses `GATE.md`.

A continuing task reads only the worklog header and Resume Point to identify the feature, then reads Git, Project Map, and feature current before loading the full worklog and resuming.
