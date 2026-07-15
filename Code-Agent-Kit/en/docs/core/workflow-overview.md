# Core Workflow Overview

## Authority and state priority

```text
Code and generated artifacts
→ deterministic validation
→ feature current
→ Project Map
→ append-only history
→ active worklog as execution checkpoint
```

Worklog is not above current. It records unfinished execution, while feature current records verified present state.

## New work on an existing feature

```text
Request
→ Git baseline and Diff
→ Project Map
→ feature current
→ Related Files and Shared Dependencies
→ stack readiness and capabilities
→ new worklog
→ five-stage Gate
→ implementation and validation
→ current/history/Project Map synchronization
→ final Diff
→ DoD
```

## Resume unfinished work

```text
worklog header and Resume Point
→ Git baseline and Diff
→ Project Map
→ feature current
→ Related Files
→ full worklog
→ recorded Gate stage
```

## Knowledge routing

```text
Project Map
→ stack SKILL
→ task-specific verified reference
→ source inspection
→ search only when still needed
```

General tutorials are not loaded as a substitute for project evidence.

## Validation

Record applicable layers separately:

- Artifact / Compile
- Rendered Output
- Runtime Behavior
- Accessibility / Color

Model self-report is not evidence.

## Completion

Production completion requires:

- required deterministic gates pass;
- feature current records the verified commit;
- feature history is appended;
- Project Map and Shared File Reverse Index are updated;
- active worklog is closed or archived;
- final Git Diff is reviewed;
- unresolved items remain PENDING.

After one feature or coherent Task group passes DoD, begin the next feature in a fresh chat.
