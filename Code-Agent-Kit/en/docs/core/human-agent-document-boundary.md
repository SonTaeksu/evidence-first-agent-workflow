# Human and Agent Document Boundary

Human onboarding documents and agent operating rules serve different purposes.

## Agent-loaded documents

Keep these concise and normative:

- `AGENTS.md`
- nearest stack or sample AGENTS file
- active worklog
- current state
- Project Map
- design and validation profile
- task-specific official documentation

## Human-only documents

Examples:

- long developer onboarding guides;
- training narratives;
- screenshots and tutorial walkthroughs;
- organizational explanations;
- FAQ written for people.

Store them under `docs/human/` and exclude them through `.agentignore`. They may link to normative rules but must not silently redefine them.

## Reason

A large developer guide is useful to a person but wastes model context and can duplicate or conflict with the actual operating rules. The agent should follow the concise source of truth; the developer guide should teach the person how to use it.
