# Verified Stack Extension Model

The core cannot invent stack-specific facts. A complete stack profile supplies both documentation and a machine-checked readiness manifest.

```text
stacks/<name>/
├─ README.md
├─ STACK.md
├─ STACK-INPUTS.md
├─ STACK-READINESS.json
├─ AGENTS.stack.md
├─ SKILL.md
├─ capability-detection.md
├─ feature-model.md
├─ artifact-contract.md
├─ communication-contract.md
├─ evidence-provenance.md
├─ references/
│  ├─ _index.md
│  ├─ pitfalls.md
│  └─ verified-facts.md
├─ skeletons/
│  └─ README.md
├─ mcp/
│  └─ source-routing.md
└─ validation/
   └─ validation-profile.md
```

## Responsibility split

### Core provides

- state and handoff model;
- mandatory Gate;
- capability-enforcement pattern;
- deterministic tool contracts;
- source-asset preprocessing;
- Git and document governance.

### Stack owner provides or confirms

- supported versions;
- primary sources and installed artifacts;
- feature boundary;
- artifact and communication contracts;
- capability branches;
- verified pitfalls and facts;
- skeletons;
- validation commands and failure patterns;
- confidentiality policy.

### Tools detect

- manifests, versions, imports, files, clients, generated code, and existing commands.

Automatic detection cannot replace owner confirmation of organizational intent.

## Readiness

```bash
python tools/check-stack-readiness/check_stack_readiness.py \
  --stack stacks/<name>
```

- `ready`: required inputs resolved
- `provisional`: only independent work may proceed
- `blocked`: a required input or capability is unknown

## Three-layer capability enforcement

1. Stack detection rules define the evidence and branch.
2. Project Map stores the project-specific result.
3. Gate Analysis repeats the selected path and stack rules prohibit unconfirmed APIs.

Internal names remain in private stack packs. The generic core keeps only the reusable pattern.
